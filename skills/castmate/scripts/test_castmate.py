#!/usr/bin/env python3
"""Process-handling tests for castmate.py, using fake CLIs. Run: python3 test_castmate.py"""
import json
import os
import shutil
import signal
import subprocess
import sys
import tempfile
import time
import unittest
from pathlib import Path

SCRIPT = Path(__file__).resolve().parent / "castmate.py"
sys.dont_write_bytecode = True

FAKE_CLI = r'''#!/usr/bin/env python3
import os, subprocess, sys, time
mode = sys.argv[1]
if mode == "echo":
    sys.stdout.write("args=" + " ".join(sys.argv[2:]) + "\n" + sys.stdin.read())
elif mode == "hang":
    print("partial line", flush=True)
    child = subprocess.Popen([sys.executable, "-c", "import time; time.sleep(120)"])
    open(os.environ["FAKE_PIDFILE"], "w").write(str(child.pid))
    time.sleep(120)
elif mode == "fail":
    sys.stderr.write("boom\n")
    sys.exit(3)
'''


class CastmateTest(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp(prefix="castmate-unit-"))
        fake = self.tmp / "fakecli"
        fake.write_text(FAKE_CLI)
        fake.chmod(0o755)
        self.pidfile = self.tmp / "grandchild.pid"
        tool = {"name": "Fake", "binary": str(fake), "verified": True, "prompt": "stdin",
                "model": ["--model", "{model}"], "readOnly": {"level": "enforced", "args": ["--ro"]},
                "write": {"args": ["--rw"]}}
        config = {
            "tools": {
                "echo": {**tool, "args": ["echo"]},
                "hang": {**tool, "args": ["hang"]},
                "fail": {**tool, "args": ["fail"]},
                "nowrite": {**{k: v for k, v in tool.items() if k != "write"}, "args": ["echo"]},
                "writeonly": {"binary": str(fake), "args": ["echo"], "write": {"args": ["--rw"]}},
            },
            "castmates": {"e": {"tool": "echo"}, "prompt": {"tool": "echo"}},
            "groups": {},
            "defaults": {"maxParallel": 1},
        }
        (self.tmp / "castmate").mkdir()
        (self.tmp / "castmate" / "config.json").write_text(json.dumps(config))
        self.prompt = self.tmp / "prompt.md"
        self.prompt.write_text("hello castmate\n")

    def tearDown(self):
        shutil.rmtree(self.tmp, ignore_errors=True)

    def run_cli(self, *args):
        env = {**os.environ, "MAKERSKILLS_CONFIG": str(self.tmp), "FAKE_PIDFILE": str(self.pidfile)}
        return subprocess.run([sys.executable, str(SCRIPT), *args], env=env, capture_output=True, text=True, timeout=120)

    def run_json(self, *args):
        proc = self.run_cli("run", "-f", str(self.prompt), "--out", str(self.tmp / "out"), "--json", *args)
        return proc, json.loads(proc.stdout) if proc.stdout.strip().startswith("{") else None

    def test_prompt_arrives_on_stdin_with_read_only_args(self):
        proc, manifest = self.run_json("-c", "e")
        self.assertEqual(proc.returncode, 0, proc.stderr)
        report = manifest["castmates"][0]
        self.assertEqual(report["status"], "success")
        text = Path(report["outputFile"]).read_text()
        self.assertIn("hello castmate", text)
        self.assertIn("--ro", text)

    def test_duplicates_get_distinct_outputs(self):
        _, manifest = self.run_json("-c", "e,e")
        labels = [r["label"] for r in manifest["castmates"]]
        self.assertEqual(labels, ["e", "e-2"])
        self.assertNotEqual(manifest["castmates"][0]["outputFile"], manifest["castmates"][1]["outputFile"])

    def test_labels_stay_unique_when_a_name_looks_like_a_suffix(self):
        sys.path.insert(0, str(SCRIPT.parent))
        import castmate
        labels = [c["label"] for c in castmate.label_castmates([{"castmate": "x"}, {"castmate": "x-2"}, {"castmate": "x"}])]
        self.assertEqual(len(set(labels)), 3, labels)

    def test_raw_tool_model_passthrough(self):
        _, manifest = self.run_json("-c", "echo:brand-new-model")
        text = Path(manifest["castmates"][0]["outputFile"]).read_text()
        self.assertIn("--model brand-new-model", text)

    def test_timeout_keeps_partial_output_and_kills_grandchild(self):
        _, manifest = self.run_json("-c", "hang", "--timeout", "2")
        report = manifest["castmates"][0]
        self.assertEqual(report["status"], "timeout")
        text = Path(report["outputFile"]).read_text()
        self.assertIn("partial line", text)
        self.assertIn("timed out", text)
        grandchild = int(self.pidfile.read_text())
        time.sleep(0.5)
        with self.assertRaises(ProcessLookupError):
            os.kill(grandchild, 0)

    def test_failure_reports_error_and_stderr(self):
        proc, manifest = self.run_json("-c", "fail")
        self.assertEqual(proc.returncode, 1)
        report = manifest["castmates"][0]
        self.assertEqual(report["status"], "error")
        self.assertIn("boom", Path(report["stderrFile"]).read_text())

    def test_write_refuses_parallel_and_missing_write_mode(self):
        proc = self.run_cli("run", "-c", "e,e", "-f", str(self.prompt), "--write")
        self.assertEqual(proc.returncode, 2)
        self.assertIn("one castmate at a time", proc.stderr)
        proc = self.run_cli("run", "-c", "nowrite", "-f", str(self.prompt), "--write", "--out", str(self.tmp / "o2"))
        self.assertEqual(proc.returncode, 2)
        self.assertIn("no write mode", proc.stderr)

    def test_reserved_label_does_not_overwrite_prompt(self):
        _, manifest = self.run_json("-c", "prompt")
        self.assertEqual(manifest["castmates"][0]["label"], "prompt_castmate")
        self.assertEqual((self.tmp / "out" / "prompt.md").read_text(), "hello castmate\n")

    def test_minimal_user_adapter_without_read_only(self):
        proc = self.run_cli("run", "-c", "writeonly", "-f", str(self.prompt), "--out", str(self.tmp / "o3"))
        self.assertEqual(proc.returncode, 2)
        self.assertIn("no read-only mode", proc.stderr)
        self.assertNotIn("Traceback", proc.stderr)
        self.assertFalse((self.tmp / "o3").exists())
        _, manifest = self.run_json("-c", "writeonly", "--write")
        self.assertEqual(manifest["castmates"][0]["status"], "success")

    def start_background(self, *args):
        env = {**os.environ, "MAKERSKILLS_CONFIG": str(self.tmp), "FAKE_PIDFILE": str(self.pidfile)}
        proc = subprocess.Popen([sys.executable, str(SCRIPT), "run", "-f", str(self.prompt), "--out", str(self.tmp / "out"), *args],
                                env=env, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        deadline = time.time() + 20
        while not self.pidfile.exists() and time.time() < deadline:
            time.sleep(0.1)
        self.assertTrue(self.pidfile.exists(), "castmate never started")
        time.sleep(0.3)
        return proc

    def assert_dead(self, pid):
        for _ in range(50):
            try:
                os.kill(pid, 0)
            except ProcessLookupError:
                return
            time.sleep(0.1)
        self.fail(f"pid {pid} still alive")

    def test_sigterm_reaps_castmates_and_exits_143(self):
        proc = self.start_background("-c", "hang", "--timeout", "60")
        grandchild = int(self.pidfile.read_text())
        proc.send_signal(signal.SIGTERM)
        proc.communicate(timeout=30)
        self.assertEqual(proc.returncode, 143)
        self.assert_dead(grandchild)
        manifest = json.loads((self.tmp / "out" / "run.json").read_text())
        self.assertTrue(manifest["aborted"])
        self.assertEqual(manifest["castmates"][0]["status"], "aborted")
        self.assertIn("partial line", Path(manifest["castmates"][0]["outputFile"]).read_text())

    def test_interrupt_does_not_start_queued_castmates(self):
        proc = self.start_background("-c", "hang,e", "--timeout", "60")
        proc.send_signal(signal.SIGINT)
        proc.communicate(timeout=30)
        self.assertEqual(proc.returncode, 130)
        reports = json.loads((self.tmp / "out" / "run.json").read_text())["castmates"]
        self.assertEqual([r["status"] for r in reports], ["aborted", "aborted"])
        self.assertNotIn("pid", reports[1])
        self.assertFalse((self.tmp / "out" / "e.raw").exists())

    def test_partial_read_only_override_keeps_shipped_args(self):
        config = json.loads((self.tmp / "castmate" / "config.json").read_text())
        config["tools"]["echo"]["readOnly"] = {"env": {"EXTRA": "1"}}
        (self.tmp / "castmate" / "config.json").write_text(json.dumps(config))
        sys.path.insert(0, str(SCRIPT.parent))
        import importlib, castmate
        os.environ["MAKERSKILLS_CONFIG"] = str(self.tmp)
        try:
            castmate = importlib.reload(castmate)
            castmate.REFS = self.tmp / "refs"
            (self.tmp / "refs").mkdir()
            shipped = {"tools": {"echo": {"binary": "x", "readOnly": {"level": "enforced", "args": ["--ro"]}}},
                       "castmates": {}, "groups": {}, "defaults": {}}
            (self.tmp / "refs" / "tools.json").write_text(json.dumps(shipped))
            ro = castmate.load_registry()["tools"]["echo"]["readOnly"]
        finally:
            del os.environ["MAKERSKILLS_CONFIG"]
        self.assertEqual(ro["args"], ["--ro"])
        self.assertEqual(ro["level"], "enforced")
        self.assertEqual(ro["env"], {"EXTRA": "1"})

    def test_test_command_rejects_answers_that_only_contain_ok(self):
        proc = self.run_cli("test", "e")
        self.assertEqual(proc.returncode, 1)
        self.assertIn("FAIL e", proc.stdout)

    def test_run_paths_are_validated_before_dispatch(self):
        cases = [
            (["-f", str(self.tmp / "missing.md")], "can't read prompt file"),
            (["-f", str(self.prompt), "--cwd", str(self.tmp / "nope")], "is not a directory"),
            (["-f", str(self.prompt), "--out", str(self.tmp)], "new or empty directory"),
            (["-f", str(self.prompt), "--cwd", str(self.tmp), "--out", str(self.tmp / "inside")], "inside --cwd"),
        ]
        for extra, message in cases:
            proc = self.run_cli("run", "-c", "e", *extra)
            self.assertEqual(proc.returncode, 2, extra)
            self.assertIn(message, proc.stderr)
            self.assertNotIn("Traceback", proc.stderr)

    def test_write_mode_uses_write_args(self):
        _, manifest = self.run_json("-c", "e", "--write")
        text = Path(manifest["castmates"][0]["outputFile"]).read_text()
        self.assertIn("--rw", text)
        self.assertNotIn("--ro", text)


if __name__ == "__main__":
    unittest.main()
