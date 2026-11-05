#!/usr/bin/env python3
"""Measure GitHub Actions usage for the ci-audit skill. Mechanics only: the SKILL.md interprets.

    python3 ci_audit.py inventory <owner> [--days 60]      repos with Actions runs, private/public, run counts
    python3 ci_audit.py month <owner/repo> [--days 30]      billable minutes by workflow (per-job rounding, macOS x10)
    python3 ci_audit.py jobs <owner/repo> [--runs 150]      queue / setup / run per job, failures, runner labels
    python3 ci_audit.py steps <owner/repo> <run-id>         per-step seconds for one run
    python3 ci_audit.py schedules <owner/repo>              every cron in the default branch, as runs per month

Needs the GitHub CLI (`gh`) logged in. Standard library only, Python 3.9+.
"""
import argparse
import collections
import datetime as dt
import json
import math
import re
import subprocess
import sys

SETUP_WORDS = ("checkout", "set up", "setup", "install", "cache", "restore", "bundle", "pnpm", "npm ci", "yarn", "dependencies")
# Billing multipliers for private repos on GitHub-hosted runners.
MULTIPLIER = (("macos", 10), ("windows", 2))


def gh(path):
    out = subprocess.run(["gh", "api", path], capture_output=True, text=True)
    if out.returncode != 0:
        sys.exit(f"gh api {path} failed: {out.stderr.strip()}")
    return json.loads(out.stdout or "{}")


def ts(s):
    return dt.datetime.fromisoformat(s.replace("Z", "+00:00")) if s else None


def since(days):
    return (dt.datetime.now(dt.timezone.utc) - dt.timedelta(days=days)).strftime("%Y-%m-%d")


def runs_since(repo, days, cap=None):
    runs, page = [], 1
    while True:
        batch = gh(f"repos/{repo}/actions/runs?per_page=100&page={page}&created=>{since(days)}").get("workflow_runs", [])
        runs += batch
        if len(batch) < 100 or (cap and len(runs) >= cap):
            return runs[:cap] if cap else runs
        page += 1


def finished_jobs(repo, run_id):
    for j in gh(f"repos/{repo}/actions/runs/{run_id}/jobs?per_page=100").get("jobs", []):
        if j.get("conclusion") == "skipped" or not j.get("started_at") or not j.get("completed_at"):
            continue
        secs = (ts(j["completed_at"]) - ts(j["started_at"])).total_seconds()
        if secs > 0:
            yield j, secs


def multiplier(labels):
    joined = ",".join(labels or []).lower()
    return next((m for word, m in MULTIPLIER if word in joined), 1)


def cmd_inventory(a):
    repos = json.loads(subprocess.run(
        ["gh", "repo", "list", a.owner, "--limit", "500", "--json", "nameWithOwner,isPrivate,pushedAt"],
        capture_output=True, text=True, check=True).stdout)
    cutoff = since(a.days)
    rows = []
    for r in repos:
        if r["pushedAt"][:10] < cutoff:
            continue
        n = gh(f"repos/{r['nameWithOwner']}/actions/runs?per_page=1&created=>{cutoff}").get("total_count", 0)
        if n:
            rows.append((n, r["nameWithOwner"], "private" if r["isPrivate"] else "public"))
    print(f"Repos with Actions runs in the last {a.days} days (public repos run free on standard runners):")
    for n, name, vis in sorted(rows, reverse=True):
        print(f"  {n:6} runs  {vis:7}  {name}")


def cmd_month(a):
    by = collections.Counter()
    total = mac = actual = 0
    runs = runs_since(a.repo, a.days)
    for r in runs:
        for j, secs in finished_jobs(a.repo, r["id"]):
            m = multiplier(j.get("labels"))
            billed = math.ceil(secs / 60) * m
            by[r["name"]] += billed
            total += billed
            actual += secs / 60 * m
            if m == 10:
                mac += billed
    print(f"{a.repo}: {len(runs)} runs in {a.days} days, about {total} billable min "
          f"({total - actual:.0f} of it rounding waste){f', macOS {mac}' if mac else ''}")
    for name, m in by.most_common():
        print(f"  {m:6}  {name}")


def cmd_jobs(a):
    agg = collections.defaultdict(lambda: dict(n=0, queue=0.0, setup=0.0, run=0.0, billed=0, fail=0, labels=set()))
    runs = runs_since(a.repo, a.days, cap=a.runs)
    for r in runs:
        for j, secs in finished_jobs(a.repo, r["id"]):
            setup = 0.0
            for st in j.get("steps") or []:
                if st.get("started_at") and st.get("completed_at") and any(w in st["name"].lower() for w in SETUP_WORDS):
                    setup += (ts(st["completed_at"]) - ts(st["started_at"])).total_seconds()
            row = agg[f"{r['name']} / {j['name']}"]
            row["n"] += 1
            row["queue"] += max(0.0, (ts(j["started_at"]) - ts(j["created_at"])).total_seconds())
            row["setup"] += setup
            row["run"] += secs - setup
            row["billed"] += math.ceil(secs / 60) * multiplier(j.get("labels"))
            row["fail"] += j["conclusion"] == "failure"
            row["labels"].update(j.get("labels") or [])
    print(f"{a.repo}: last {len(runs)} runs. Seconds are per-job averages; setup is a step-name guess, confirm with `steps`.")
    print(f"  {'workflow / job':58} {'n':>4} {'queue':>6} {'setup':>6} {'run':>6} {'billed':>7} {'fail':>5}  runner")
    for k, r in sorted(agg.items(), key=lambda kv: -kv[1]["billed"]):
        n = r["n"]
        print(f"  {k[:58]:58} {n:4} {r['queue'] / n:6.0f} {r['setup'] / n:6.0f} {r['run'] / n:6.0f} "
              f"{r['billed']:7} {r['fail']:5}  {','.join(sorted(r['labels']))}")


def cmd_steps(a):
    for j in gh(f"repos/{a.repo}/actions/runs/{a.run_id}/jobs?per_page=100").get("jobs", []):
        print(f"{j['name']} ({j.get('conclusion')})")
        for st in j.get("steps") or []:
            if st.get("started_at") and st.get("completed_at"):
                secs = (ts(st["completed_at"]) - ts(st["started_at"])).total_seconds()
                print(f"  {secs:6.0f}s  {st['name']}")


def cron_field(spec, lo, hi):
    values = set()
    for part in spec.split(","):
        step = 1
        if "/" in part:
            part, step = part.split("/")
            step = int(step)
        if part == "*":
            start, end = lo, hi
        elif "-" in part:
            start, end = map(int, part.split("-"))
        else:
            start = end = int(part)
            if step > 1:
                end = hi
        values.update(range(start, end + 1, step))
    return values


def runs_per_month(expr):
    minute, hour, dom, month, dow = expr.split()
    mins, hours = cron_field(minute, 0, 59), cron_field(hour, 0, 23)
    doms, months = cron_field(dom, 1, 31), cron_field(month, 1, 12)
    dows = {d % 7 for d in cron_field(dow, 0, 6 if dow == "*" else 7)}  # 7 and 0 are both Sunday
    count, day = 0, dt.date(2025, 1, 1)
    for _ in range(365):
        dom_ok, dow_ok = day.day in doms, (day.isoweekday() % 7) in dows
        # Cron ORs day-of-month and day-of-week when both are restricted.
        both = dom != "*" and dow != "*"
        if day.month in months and ((dom_ok or dow_ok) if both else (dom_ok and dow_ok)):
            count += len(mins) * len(hours)
        day += dt.timedelta(days=1)
    return count / 12


def cmd_schedules(a):
    default = gh(f"repos/{a.repo}").get("default_branch", "main")
    files = gh(f"repos/{a.repo}/contents/.github/workflows?ref={default}")
    print(f"{a.repo}: schedules on {default} (scheduled workflows only ever run from the default branch)")
    for f in files if isinstance(files, list) else []:
        if not f["name"].endswith((".yml", ".yaml")):
            continue
        text = subprocess.run(["gh", "api", f["url"], "-H", "Accept: application/vnd.github.raw"],
                              capture_output=True, text=True).stdout
        for expr in re.findall(r"cron:\s*['\"]([^'\"]+)['\"]", text):
            try:
                print(f"  {runs_per_month(expr):7.0f} runs/mo  {expr:18}  {f['name']}")
            except ValueError:
                print(f"        ? runs/mo  {expr:18}  {f['name']}  (could not parse)")


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = p.add_subparsers(dest="cmd", required=True)
    s = sub.add_parser("inventory"); s.add_argument("owner"); s.add_argument("--days", type=int, default=60)
    s = sub.add_parser("month"); s.add_argument("repo"); s.add_argument("--days", type=int, default=30)
    s = sub.add_parser("jobs"); s.add_argument("repo"); s.add_argument("--runs", type=int, default=150); s.add_argument("--days", type=int, default=30)
    s = sub.add_parser("steps"); s.add_argument("repo"); s.add_argument("run_id")
    s = sub.add_parser("schedules"); s.add_argument("repo")
    a = p.parse_args()
    {"inventory": cmd_inventory, "month": cmd_month, "jobs": cmd_jobs, "steps": cmd_steps, "schedules": cmd_schedules}[a.cmd](a)


if __name__ == "__main__":
    main()
