#!/usr/bin/env python3
"""castmate: hand a prompt to other AI coding CLIs, one or several in parallel.

    castmate.py list [--json]
    castmate.py test CASTMATE [CASTMATE ...]
    castmate.py run -c CASTMATES -f PROMPT_FILE [--write] [--timeout S] [--out DIR] [--cwd DIR] [--json]

CASTMATES is a comma list of castmate aliases, group names, bare tool ids
(`codex`), or `tool:model[@effort]` for any model the CLI accepts
(`codex:gpt-5.7@high`). Repeat a name to run it twice.

Adapters and aliases ship in ../references/tools.json. Personal overrides go in
${MAKERSKILLS_CONFIG:-~/.config/makerskills}/castmate/config.json (same shape,
merged on top). Stdlib only, Python 3.9+.
"""
import argparse
import json
import os
import re
import secrets
import shlex
import shutil
import signal
import subprocess
import sys
import tempfile
import threading
import time
from concurrent.futures import ThreadPoolExecutor, wait
from datetime import datetime
from pathlib import Path

SKILL_DIR = Path(__file__).resolve().parents[1]
REFS = SKILL_DIR / "references"
CONFIG_DIR = Path(os.environ.get("MAKERSKILLS_CONFIG") or Path.home() / ".config" / "makerskills") / "castmate"

KILL_GRACE_S = 15
HEARTBEAT_S = 30
ENV_DENYLIST = {
    "NODE_OPTIONS", "NODE_EXTRA_CA_CERTS", "LD_PRELOAD", "LD_LIBRARY_PATH", "LD_AUDIT", "ELECTRON_RUN_AS_NODE",
    "PYTHONPATH", "PYTHONSTARTUP", "RUBYOPT", "PERL5OPT", "BASH_ENV", "ENV", "GIT_SSH_COMMAND", "GIT_EXTERNAL_DIFF",
}
ANSI_RE = re.compile(r"\x1b\[[0-9;?]*[ -/]*[@-~]|\x1b\][^\x07\x1b]*(?:\x07|\x1b\\)")
PLACEHOLDER_RE = re.compile(r"\{(\w+)\}")
RESERVED_LABELS = {"prompt", "run"}
OK_RE = re.compile(r"[`*\"']*OK[.!]?[`*\"']*")

_active = {}
_active_lock = threading.Lock()
_abort = threading.Event()
_stop_signal = [signal.SIGINT]


class CastmateError(Exception):
    pass


def load_registry():
    data = json.loads((REFS / "tools.json").read_text())
    user_file = CONFIG_DIR / "config.json"
    if user_file.exists():
        try:
            user = json.loads(user_file.read_text())
        except json.JSONDecodeError as exc:
            raise CastmateError(f"{user_file} is not valid JSON: {exc}")
        for key, tool in user.get("tools", {}).items():
            base = data["tools"].get(key, {})
            merged = {**base, **tool}
            for mode in ("readOnly", "write"):
                if isinstance(base.get(mode), dict) and isinstance(tool.get(mode), dict):
                    merged[mode] = {**base[mode], **tool[mode]}
            data["tools"][key] = merged
        for section in ("castmates", "groups"):
            data[section].update(user.get(section, {}))
        data["defaults"].update(user.get("defaults", {}))
    for key, tool in data["tools"].items():
        if "binary" not in tool:
            raise CastmateError(f"tool '{key}' in {user_file} needs a \"binary\"")
        tool.setdefault("name", key)
    return data


def parse_spec(spec, reg):
    """Turn one castmate spec into a dict with tool/model/effort."""
    if spec in reg["castmates"]:
        return {"castmate": spec, **reg["castmates"][spec]}
    if spec in reg["tools"]:
        return {"castmate": spec, "tool": spec}
    if ":" in spec:
        tool, _, rest = spec.partition(":")
        model, _, effort = rest.partition("@")
        if tool not in reg["tools"]:
            raise CastmateError(f"unknown tool '{tool}' in '{spec}'")
        cm = {"castmate": spec, "tool": tool, "model": model}
        if effort:
            cm["effort"] = effort
        return cm
    raise CastmateError(f"unknown castmate '{spec}' (run `castmate.py list`)")


def expand(specs, reg):
    out = []
    for spec in [s.strip() for s in specs.split(",") if s.strip()]:
        if spec in reg["groups"]:
            out.extend(parse_spec(s, reg) for s in reg["groups"][spec])
        else:
            out.append(parse_spec(spec, reg))
    if not out:
        raise CastmateError("no castmates given")
    return out


def read_only_level(tool):
    return tool.get("readOnly", {}).get("level", "none")


def label_castmates(castmates):
    used = set()
    for cm in castmates:
        base = re.sub(r"[^A-Za-z0-9._-]", "_", cm["castmate"])
        if base in RESERVED_LABELS:
            base += "_castmate"
        label, n = base, 1
        while label in used:
            n += 1
            label = f"{base}-{n}"
        used.add(label)
        cm["label"] = label
    return castmates


def safe_env(extra):
    env = {k: v for k, v in os.environ.items() if k not in ENV_DENYLIST and not k.startswith("DYLD_")}
    env.update(extra)
    env.pop("FORCE_COLOR", None)
    env.pop("CLICOLOR_FORCE", None)
    env["NO_COLOR"] = "1"
    return env


def substitute(template, values):
    def repl(match):
        key = match.group(1)
        return str(values[key]) if key in values else match.group(0)
    return PLACEHOLDER_RE.sub(repl, template)


def build_invocation(reg, cm, prompt, out_dir, write, cwd, timeout):
    tool = reg["tools"][cm["tool"]]
    binary = shutil.which(tool["binary"])
    if not binary:
        raise CastmateError(f"{cm['castmate']}: `{tool['binary']}` not found on PATH (install: {tool.get('install', '?')})")
    mode = tool.get("write") if write else tool.get("readOnly")
    if mode is not None and not write and mode.get("level") not in ("enforced", "best-effort"):
        raise CastmateError(f"{cm['castmate']}: {tool['name']} read-only level is '{mode.get('level')}'; set it to enforced or best-effort")
    if mode is None:
        raise CastmateError(f"{cm['castmate']}: {tool['name']} has no {'write' if write else 'read-only'} mode configured")

    text = prompt + tool.get("promptSuffix", "")
    values = {
        "model": cm.get("model", ""),
        "effort": cm.get("effort", ""),
        "prompt": text,
        "last_message": str(out_dir / f"{cm['label']}.last.md"),
        "cwd": cwd,
        "refs": str(REFS),
        "timeout_plus": timeout + 60,
    }

    args = list(tool.get("args", []))
    for key in ("model", "effort"):
        if cm.get(key):
            if key not in tool:
                raise CastmateError(f"{cm['castmate']}: {tool['name']} has no {key} flag configured")
            args += tool[key]
    args += mode.get("args", [])
    args += cm.get("extraArgs", [])
    args += tool.get("argsAfter", [])
    args = [substitute(a, values) for a in args]
    env = {k: substitute(v, values) for k, v in mode.get("env", {}).items()}

    shown = [binary] + ["<prompt>" if a == text else a for a in args]
    return {
        "argv": [binary] + args,
        "stdin": text if tool.get("prompt", "stdin") == "stdin" else None,
        "env": safe_env(env),
        "cwd": cwd,
        "command": " ".join(shlex.quote(a) for a in shown),
        "last_message": values["last_message"] if tool.get("output") == "last_message" else None,
    }


def kill_group(proc, sig):
    try:
        os.killpg(proc.pid, sig)
    except (ProcessLookupError, PermissionError, AttributeError):
        try:
            proc.send_signal(sig)
        except ProcessLookupError:
            pass


def terminate(proc):
    kill_group(proc, signal.SIGTERM)
    try:
        proc.wait(timeout=KILL_GRACE_S)
    except subprocess.TimeoutExpired:
        kill_group(proc, signal.SIGKILL)
        proc.wait()


def execute(inv, out_dir, label, timeout):
    raw_path = out_dir / f"{label}.raw"
    err_path = out_dir / f"{label}.stderr"
    start = time.monotonic()
    timed_out = False
    with open(raw_path, "wb") as out, open(err_path, "wb") as err:
        # Check-and-spawn under the lock so an interrupt can't miss a castmate
        # that starts between the abort and the kill sweep.
        with _active_lock:
            if _abort.is_set():
                raw_path.unlink()
                err_path.unlink()
                return {"status": "aborted"}
            proc = subprocess.Popen(
                inv["argv"],
                cwd=inv["cwd"],
                env=inv["env"],
                stdin=subprocess.PIPE if inv["stdin"] is not None else subprocess.DEVNULL,
                stdout=out,
                stderr=err,
                start_new_session=True,
            )
            _active[label] = (proc, start)
        print(f"castmate: started {label} (pid {proc.pid})", file=sys.stderr, flush=True)
        if inv["stdin"] is not None:
            def feed():
                try:
                    proc.stdin.write(inv["stdin"].encode())
                    proc.stdin.close()
                except (BrokenPipeError, OSError):
                    pass
            threading.Thread(target=feed, daemon=True).start()
        try:
            proc.wait(timeout=timeout)
        except subprocess.TimeoutExpired:
            timed_out = True
            terminate(proc)
        kill_group(proc, signal.SIGTERM)  # reap anything the CLI left behind
        with _active_lock:
            _active.pop(label, None)

    output = ANSI_RE.sub("", raw_path.read_text(errors="replace"))
    last = Path(inv["last_message"]) if inv["last_message"] else None
    if last and last.exists():
        last_text = ANSI_RE.sub("", last.read_text(errors="replace"))
        last.unlink()
        if last_text.strip():
            output = last_text
    if timed_out:
        output += f"\n\n[castmate: timed out after {timeout}s; output above is partial]\n"
    raw_path.unlink()
    stderr_text = ANSI_RE.sub("", err_path.read_text(errors="replace"))
    err_path.write_text(stderr_text)

    output_file = out_dir / f"{label}.md"
    output_file.write_text(output)

    if timed_out:
        status = "timeout"
    elif _abort.is_set() and proc.returncode != 0:
        status = "aborted"
    elif proc.returncode != 0:
        status = "error"
    elif not output.strip():
        status = "empty"
    else:
        status = "success"
    return {
        "status": status,
        "exitCode": proc.returncode,
        "pid": proc.pid,
        "durationS": round(time.monotonic() - start, 1),
        "words": len(output.split()),
        "outputFile": str(output_file),
        "stderrFile": str(err_path),
    }


def heartbeat_loop(stop):
    while not stop.wait(HEARTBEAT_S):
        with _active_lock:
            running = [f"{label} (pid {p.pid}, {int(time.monotonic() - s)}s)" for label, (p, s) in _active.items()]
        if running:
            print("castmate: still running: " + ", ".join(running), file=sys.stderr, flush=True)


def slugify(text):
    slug = re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")[:40].strip("-")
    return slug or "untitled"


def dispatch(reg, castmates, prompt, out_dir, write, cwd, timeout):
    invocations = {cm["label"]: build_invocation(reg, cm, prompt, out_dir, write, cwd, timeout) for cm in castmates}
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "prompt.md").write_text(prompt)

    reports = []
    stop = threading.Event()
    threading.Thread(target=heartbeat_loop, args=(stop,), daemon=True).start()
    pool = ThreadPoolExecutor(max_workers=int(reg["defaults"].get("maxParallel", 4)))
    futures = {pool.submit(execute, invocations[cm["label"]], out_dir, cm["label"], timeout): cm for cm in castmates}
    aborted = False
    try:
        pending = set(futures)
        while pending:
            _, pending = wait(pending, timeout=1)
    except KeyboardInterrupt:
        aborted = True
        print("castmate: interrupted, stopping castmates", file=sys.stderr, flush=True)
        with _active_lock:
            _abort.set()
            procs = [p for p, _ in _active.values()]
        for proc in procs:
            kill_group(proc, signal.SIGTERM)
        try:
            wait(futures, timeout=KILL_GRACE_S)
        except KeyboardInterrupt:
            pass
        with _active_lock:
            for proc, _ in _active.values():
                kill_group(proc, signal.SIGKILL)
    finally:
        stop.set()
        pool.shutdown(wait=True, cancel_futures=True)

    for future, cm in futures.items():
        tool = reg["tools"][cm["tool"]]
        report = {
            "label": cm["label"],
            "castmate": cm["castmate"],
            "tool": cm["tool"],
            "model": cm.get("model"),
            "effort": cm.get("effort"),
            "access": "write" if write else read_only_level(tool),
            "verified": tool.get("verified", False),
            "command": invocations[cm["label"]]["command"],
        }
        if future.done() and not future.cancelled() and future.exception() is None:
            report.update(future.result())
        else:
            exc = future.exception() if future.done() and not future.cancelled() else None
            report.update(status="aborted" if exc is None else "error", error=str(exc) if exc else None)
        reports.append(report)

    manifest = {
        "finished": datetime.now().isoformat(timespec="seconds"),
        "cwd": cwd,
        "mode": "write" if write else "read-only",
        "aborted": aborted,
        "outDir": str(out_dir),
        "promptFile": str(out_dir / "prompt.md"),
        "castmates": reports,
    }
    (out_dir / "run.json").write_text(json.dumps(manifest, indent=2) + "\n")
    return manifest


def cmd_list(reg, as_json):
    rows = []
    for name, cm in reg["castmates"].items():
        tool = reg["tools"].get(cm["tool"], {})
        rows.append({
            "castmate": name,
            "tool": cm["tool"],
            "model": cm.get("model"),
            "effort": cm.get("effort"),
            "installed": bool(tool and shutil.which(tool["binary"])),
            "readOnly": read_only_level(tool),
            "write": "write" in tool,
            "verified": tool.get("verified", False),
            "note": cm.get("note", ""),
        })
    if as_json:
        print(json.dumps({"castmates": rows, "groups": reg["groups"], "tools": sorted(reg["tools"])}, indent=2))
        return 0
    for r in rows:
        flags = [("installed" if r["installed"] else "missing"), f"read-only:{r['readOnly']}"]
        if not r["verified"]:
            flags.append("unverified")
        print(f"{r['castmate']:<18} {r['note']:<38} {' '.join(flags)}")
    print("\nGroups:")
    for name, members in reg["groups"].items():
        print(f"  {name:<10} {', '.join(members)}")
    print("\nAny tool also works bare or as tool:model[@effort]: " + ", ".join(sorted(reg["tools"])))
    return 0


def cmd_test(reg, specs):
    castmates = label_castmates(expand(specs, reg))
    with tempfile.TemporaryDirectory(prefix="castmate-test-") as tmp:
        work = Path(tmp) / "work"
        work.mkdir()
        manifest = dispatch(reg, castmates, "Reply with exactly: OK", Path(tmp) / "out", False, str(work), 120)
        failed = 0
        for r in manifest["castmates"]:
            text = Path(r["outputFile"]).read_text() if r.get("outputFile") else ""
            ok = r["status"] == "success" and OK_RE.fullmatch(text.strip()) is not None
            if not ok:
                failed += 1
                err = Path(r["stderrFile"]).read_text().strip()[:300] if r.get("stderrFile") else r.get("error", "")
                print(f"FAIL {r['label']}: {r['status']} {err}")
            else:
                print(f"ok   {r['label']} ({r['durationS']}s)")
    return 1 if failed else 0


def cmd_run(reg, args):
    castmates = label_castmates(expand(args.castmates, reg))
    try:
        prompt = Path(args.file).read_text() if args.file != "-" else sys.stdin.read()
    except (OSError, UnicodeDecodeError) as exc:
        raise CastmateError(f"can't read prompt file {args.file}: {exc}")
    if not prompt.strip():
        raise CastmateError("prompt is empty")
    if args.write and len(castmates) > 1:
        raise CastmateError("--write runs one castmate at a time (parallel writers would collide in one tree)")
    for cm in castmates:
        tool = reg["tools"][cm["tool"]]
        if not tool.get("verified", False):
            print(f"castmate: warning: {tool['name']} adapter is unverified", file=sys.stderr)
        if not args.write and read_only_level(tool) != "enforced":
            print(f"castmate: warning: {tool['name']} read-only is {read_only_level(tool)}, not enforced", file=sys.stderr)

    timeout = args.timeout or int(reg["defaults"].get("timeout", 540))
    cwd = Path(args.cwd).expanduser().resolve() if args.cwd else Path.cwd()
    if not cwd.is_dir():
        raise CastmateError(f"--cwd {cwd} is not a directory")
    if args.out:
        out_dir = Path(args.out).expanduser().resolve()
        if out_dir.exists() and (not out_dir.is_dir() or any(out_dir.iterdir())):
            raise CastmateError(f"--out {out_dir} must be a new or empty directory")
        if not args.write and (out_dir == cwd or cwd in out_dir.parents):
            raise CastmateError("--out is inside --cwd; a read-only run must not write into the tree it reviews")
    else:
        stamp = datetime.now().strftime("%Y%m%d-%H%M%S")
        out_dir = CONFIG_DIR / "runs" / f"{stamp}-{slugify(prompt.strip().splitlines()[0])}-{secrets.token_hex(3)}"
    cwd = str(cwd)

    manifest = dispatch(reg, castmates, prompt, out_dir, args.write, cwd, timeout)
    if args.json:
        print(json.dumps(manifest, indent=2))
    else:
        for r in manifest["castmates"]:
            print(f"{r['status']:<8} {r['label']:<20} {r.get('durationS', '-')}s  {r.get('outputFile', r.get('error', ''))}")
        print(f"\nmanifest: {out_dir / 'run.json'}")
    if manifest["aborted"]:
        return 128 + int(_stop_signal[0])
    return 0 if any(r["status"] == "success" for r in manifest["castmates"]) else 1


def main(argv=None):
    parser = argparse.ArgumentParser(prog="castmate", description="Hand a prompt to other AI coding CLIs.")
    sub = parser.add_subparsers(dest="command", required=True)
    p_list = sub.add_parser("list", help="show castmates, groups, and install status")
    p_list.add_argument("--json", action="store_true")
    p_test = sub.add_parser("test", help="check castmates answer 'OK'")
    p_test.add_argument("castmates", nargs="+")
    p_run = sub.add_parser("run", help="dispatch a prompt")
    p_run.add_argument("-c", "--castmates", required=True)
    p_run.add_argument("-f", "--file", required=True, help="prompt file, or - for stdin")
    p_run.add_argument("--write", action="store_true", help="let one castmate edit files in --cwd")
    p_run.add_argument("--timeout", type=int, help="seconds per castmate (default 540)")
    p_run.add_argument("--out", help="output dir (default $MAKERSKILLS_CONFIG/castmate/runs/<stamp>-<slug>)")
    p_run.add_argument("--cwd", help="directory the castmates work in (default: current)")
    p_run.add_argument("--json", action="store_true", help="print the manifest as JSON")
    args = parser.parse_args(argv)

    def on_signal(signum, _frame):
        _stop_signal[0] = signum
        raise KeyboardInterrupt
    for sig in (signal.SIGTERM, signal.SIGHUP):
        signal.signal(sig, on_signal)

    try:
        reg = load_registry()
        if args.command == "list":
            return cmd_list(reg, args.json)
        if args.command == "test":
            return cmd_test(reg, ",".join(args.castmates))
        return cmd_run(reg, args)
    except CastmateError as exc:
        print(f"castmate: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
