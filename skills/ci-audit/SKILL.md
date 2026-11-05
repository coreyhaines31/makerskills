---
name: ci-audit
description: "When you want to cut GitHub Actions minutes and wait time across one repo or a whole portfolio. Measures queue, setup and run time per job, billed minutes with per-job minute rounding and the macOS 10× multiplier, and cron runs per month. Finds pipelines that have been failing quietly, ranks fixes by minutes saved, then ships them as small PRs with warm-cache before/after numbers. Triggers on \"/ci-audit,\" \"audit our CI,\" \"why is CI so slow,\" \"cut Actions minutes,\" \"we're over our Actions minutes,\" \"optimize GitHub Actions,\" \"CI costs,\" \"speed up CI.\" Not for designing CI from scratch or picking a CI vendor."
metadata:
  version: 0.1.0
---

# /ci-audit — Find and fix wasted GitHub Actions time

Measure first, then fix the few things that matter. In real audits the biggest win was rarely a slow test suite. It was a scheduled pipeline that had failed every day for months, a 30-second hourly cron billed as 730 minutes a month, or an SDK silently retrying a dead request three times.

A stdlib script, `scripts/ci_audit.py` in this skill's folder, does the measuring. You read its output, decide what's worth fixing, and ship it.

```bash
python3 <skill-dir>/scripts/ci_audit.py inventory <owner>              # which repos run Actions, private vs public
python3 <skill-dir>/scripts/ci_audit.py month <owner/repo>             # billable minutes by workflow, 30 days
python3 <skill-dir>/scripts/ci_audit.py jobs <owner/repo> --runs 150   # queue / setup / run per job
python3 <skill-dir>/scripts/ci_audit.py steps <owner/repo> <run-id>    # per-step seconds for one run
python3 <skill-dir>/scripts/ci_audit.py schedules <owner/repo>         # every cron as runs per month
```

It needs the GitHub CLI (`gh`) logged in. `month` and `jobs` make one API call per run, so a busy repo takes a minute or two. Run them in the background.

## Step 0 — Scope and rules

Before measuring, settle with the user:

- **Which owners and repos.** One repo, or everything pushed to in the last 60 days.
- **Off-limits repos.** Someone else (a teammate, another agent) is mid-feature there. Those get an issue with numbers, never a pushed branch.
- **Where merges go.** The integration branch (`development`, say) by default. Releasing to the default branch is a separate yes, but crons and scheduled fixes only take effect after it (Step 6).
- **What's out of scope:** cutting test coverage, paid runners, switching CI vendors. Recommend those with numbers; don't do them.

Read `references/gotchas.md` now.

## Step 1 — Inventory and money

1. `ci_audit.py inventory <owner>` for each owner. Note private vs public: only private repos cost money, but every repo's wait time matters when agents block on CI.
2. For an org, pull real billing: `gh api "/organizations/<org>/settings/billing/usage?year=YYYY&month=M"`. For a personal account, use `ci_audit.py month` on each private repo and compare the total with the plan's included minutes.
3. Write down the top 5 repos by billable minutes. That's where the time goes.

## Step 2 — Broken before slow

For every repo with scheduled workflows:

- Check the last 10 scheduled runs per workflow. Any workflow that fails every time is the first finding, whatever its cost. Read its logs (`gh api repos/O/R/actions/runs/<id>/logs > logs.zip`).
- Run `actionlint` on `.github/workflows/`. A file GitHub can't parse never runs its schedule.

Expect layered errors. See `references/fixes.md` §1.

## Step 3 — Schedules

`ci_audit.py schedules <repo>` on each repo with crons. Multiply runs/month by the billed minutes per run (from `jobs`). Flag:

- Short jobs on tight schedules (an hourly 30-second check is 730 billed min/month).
- Several crons at the same minute that hit the same rate-limited API.
- Monthly crons that make one huge run. Split the work across nights.

## Step 4 — Per-job breakdown

For the top repos: `ci_audit.py jobs <repo> --runs 150`, then `steps` on one recent green run of each expensive job. Classify each job's time:

| Bucket | What it points to |
|---|---|
| **Queue** high | Runner contention or concurrency groups. Usually not fixable cheaply; note it. |
| **Setup** high | Dependency install and caching (`references/fixes.md` §3–4). |
| **Run** high, app tests | Real test time. Leave it unless a step is plainly redundant. |
| **Run** high, data pipeline | Instrument phases and fix the code, not the CI (`references/fixes.md` §6). |
| **Failures** > 5% | Flaky tests or broken pipelines (`references/fixes.md` §1, §7). |

## Step 5 — Report and pick

Write one table, sorted by estimated minutes saved per month:

| Repo | Finding | Evidence | Fix | Est. saved/mo | Risk |
|---|---|---|---|---|---|

Include findings you won't fix (off-limits repos, owner decisions such as cron frequency or parallelism) with the numbers the owner needs to decide. Show it to the user and get a go on which rows to ship. Archive it as `${MAKERSKILLS_CONFIG:-$HOME/.config/makerskills}/ci-audit/archive/<YYYY-MM-DD>-<scope>.md`.

## Step 6 — Fix pass

One repo, one worker. On hosts that support subagents, run repos in parallel with the same brief: fresh clone, issue first, branch named for the issue, small commits, before/after numbers in the PR body.

For each fix:

1. Open an issue with the measurement.
2. Make the change on a branch. Lint and run tests locally, confirming by exit code.
3. Prove it: push, then **rerun the PR's CI** so the cache is warm, and compare against a baseline of several old runs. For pipeline fixes, dispatch the workflow from the branch with a small limit.
4. If the change didn't help (it happens, e.g. Playwright caches), close the PR with the numbers. That's a result, not a failure.
5. Merge into the integration branch after review and green checks.
6. For anything scheduled, open the release PR to the default branch once the user agrees. Until then, nothing changes in production.

## Step 7 — Verify and log

- After the next scheduled run, read its timings and logs. Confirm the fix held in production, not just on the branch.
- Append results to the archive file: per-repo before/after, what was closed without merging, and new gotchas.
- Suggest rerunning the audit monthly, or whenever CI feels slow. A recurring reminder (`loopify`) works well.

## Composes with

- `loopify` — schedule a monthly re-audit or a next-morning check of the first scheduled run.
- `castmate` — get a second model's review on a risky workflow change.
- `unstuck` — when a fix that should work measures slower, before giving up on it.
- `pm` — track owner decisions (cron frequency, paid runners) that the audit surfaced but didn't make.

## Notes on quality

- **Broken beats slow.** Always check failing scheduled workflows before timing anything. A daily pipeline failing for six months is a bigger loss than any cache.
- **Warm numbers or no claim.** Never report a speedup from one cold run. Rerun, baseline from several old runs, and state both numbers in the PR.
- **Billed minutes, not seconds.** Rounding per job means fewer, fuller jobs beat many tiny ones on private repos. Parallelizing is a speed decision with a cost, not a free win.
- **Same coverage, every time.** The test count before and after goes in the PR body. A faster suite that runs less is not a fix.
- **Scheduled means default branch.** Don't call a cron or pipeline fix done until it's on the default branch and one scheduled run has passed.
- **Close failed experiments with data.** A PR that measured slower gets closed with its numbers, so nobody retries the same idea next quarter.
- **Respect other people's branches.** Off-limits repos get issues, never pushes.
