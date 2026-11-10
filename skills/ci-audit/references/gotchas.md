# Gotchas

What tripped up real audits. Read before the measurement step.

## Billing

- Each **job** is billed rounded up to the whole minute. A 7-second job costs 1 minute, so a workflow with 4 tiny jobs costs 4. Minute rounding alone wasted 10–15% across one portfolio.
- macOS minutes count **10×** against the included allowance on private repos (Windows 2×). A macOS job that only checks whether anything changed still bills 10 minutes. Do the check on `ubuntu-latest` and gate the macOS job on its output (`needs:` + `if:`).
- Public repos run free on standard GitHub-hosted runners. Only private repos cost money, but speed still matters for public repos when agents wait on CI before merging.
- Billing API: `/organizations/<org>/settings/billing/usage?year=&month=` works with a normal token. The user-level equivalent needs the `user` scope (`gh auth refresh -h github.com -s user`). Without it, estimate with `ci_audit.py month`.

## Measuring

- **Look at daily durations, not 30-day averages.** A monthly cron (the 1st of the month) makes a spike that looks like a slow average.
- **A 30-day lookback misses newly added crons.** Read every `schedule:` (`ci_audit.py schedules`) and compute runs/month × billed minutes yourself.
- **The setup column in `jobs` guesses from step names.** It misfiles steps like "Run pnpm lint" as setup. Confirm the slow steps with `ci_audit.py steps <repo> <run-id>` on a recent green run.
- **Caches only pay off on the second run.** A PR's cache is scoped to its ref, so measure warm with `gh run rerun <id>`. After merge, the first push to the integration branch seeds the cache for every PR.
- Each repo gets **10 GB of Actions cache**. Delete caches from abandoned experiments (`gh cache delete`). Old setup-node caches age out on their own once nothing writes them.
- Timings are noisy (the same code measured 186 s, then 142 s). Compare across several runs.

## Waiting and tooling

- Runner queue waits of 10+ minutes happen. Wait in the background (`gh pr checks <n> --watch` or an until-loop), not with a foreground `gh run watch` that can hit an agent's tool timeout.
- `gh pr edit --body` can fail with a Projects (classic) GraphQL error. Use `gh api -X PATCH repos/O/R/pulls/N -F body=@file` instead.
- `gh issue create --body "$(cat <<EOF …)"` breaks on apostrophes. Use `--body-file`.
- "Closes #N" only fires when a PR merges into the **default** branch. Issues closed by PRs into `development` stay open until the release.
- Old job logs stay readable via `gh api repos/O/R/actions/jobs/<job-id>/logs`. Diff step lines between an old and new run to prove a change.

## Scope

- Don't cut test coverage to save minutes. Every fix keeps the same test count, and the PR body says so ("still 2478 examples, all passing").
- Don't move to paid runners or third-party CI as part of the audit. Recommend it, with numbers, and let the owner decide.
- Repos where another person or agent is actively working: file an issue with the measurement and suggested fix, don't push code.
- Security problems found along the way in **public** repos go into a private security advisory, not a public issue.
