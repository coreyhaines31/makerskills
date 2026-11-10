# Fix playbook

Ranked by how often each one paid off in real audits. Every fix needs a before/after number on a **warm** cache (the second run after the change), not a single run. Timings swing 2–5× run to run, so baseline from about 10 runs.

## 1. Broken scheduled workflows (check first)

The biggest find is usually a pipeline that's been failing quietly for months, not a slow one.

- List every workflow whose last 10 scheduled runs all failed. Read the logs (`gh api repos/O/R/actions/runs/ID/logs > logs.zip`, then unzip). `gh run view --log` sometimes prints nothing.
- **Errors come in layers.** Fixing the first one (an empty API credit balance) often exposes the next (a retired model ID). Before calling it fixed, grep the repo for hardcoded, dated model IDs (`claude-*-2025…`, `gpt-4-…`) and deprecated APIs.
- Test the fix from the branch before merging: `gh workflow run <file> --ref <branch> -f <inputs>` with a small limit, if the workflow takes one.
- Run `actionlint` on every workflow file. A file GitHub can't parse never runs its schedule. The only symptom is a red "workflow file issue" run on every push, which reads as noise.
- An explicit `permissions:` block replaces all the defaults. If it lists only `issues: write`, `actions/checkout` fails on a private repo. Add `contents: read`.

## 2. Over-scheduled crons

- Run `ci_audit.py schedules` and multiply runs/month by billed minutes per run. A 30-second hourly job bills 730 min a month, because every run rounds up to a full minute.
- Ask what the job protects against and how fast it really needs to notice. A check on an artifact that only changes on deploy can run every 6 hours, plus a manual dispatch after deploys.
- Stagger crons that share a rate-limited API (the same scraper or LLM key). Three jobs at 03:00 compete for the same 429 budget.
- Scheduled workflows run **only from the default branch**. A cron fix does nothing until it's released to `main`.
- When one `on.schedule` has several crons and the steps branch on `github.event.schedule == '…'`, change the cron and its matching `if:` together.

## 3. Dependency install

- **Node:** cache `node_modules` itself, keyed on OS + Node version + lockfile hash, and skip `npm ci` on a hit. `setup-node`'s `cache: npm` only caches `~/.npm`, so `npm ci` still runs every time. Typical result: 16–67 s down to about 5 s.
- **pnpm:** `cache: pnpm` on setup-node is usually enough. Check that `pnpm install --frozen-lockfile` takes under 10 s.
- **Ruby:** swap a `ruby:` container for `ruby/setup-ruby` with `bundler-cache: true` (gems 87 s down to 13 s). Gems then install into `vendor/bundle` inside the workspace. Gitignore `/vendor/bundle`, or Tailwind v4's automatic source scan reads every gem (CSS build 0.3 s → 5 s).
- Remove leftover debug steps and `apt-get install` of packages the runner image already has.

## 4. Build caches

- `.next/cache` helps `next build` only. `next dev` and Turbopack dev leave it empty, so check what was actually saved with `gh api repos/O/R/actions/caches`.
- A Turborepo remote or local cache helps monorepos with several apps.

## 5. Things that look like wins but aren't

- **Playwright browser cache with `--with-deps`:** apt install-deps dominates, and a cache hit still has to run it. Measured slower (6 s restore + 28 s deps vs 19 s uncached). Measure before you keep it.
- **Splitting one job into parallel jobs on a private repo:** each job pays its own setup (about 45 s) and its own minute rounding. Faster wall-clock, higher bill.
- **Test parallelism on private repos:** `ubuntu-latest` there has 2 vCPU (public repos get 4). Plan for 2 processes at most, and only if wall-clock matters more than minutes.
- **Folding a separate tiny job into another:** check its triggers first. A scheduled run against `main` can't merge into a push or PR job.

## 6. Pipelines that run inside Actions

When the long job is the product's own data pipeline (scraping, enrichment, LLM calls), CI tuning won't help. Instrument it instead:

- Log wall time per phase (`msPlaces`, `msSite`…) in the stage's summary line. Sums across concurrent workers exceed wall time, so compare shares, not totals.
- Replace per-row work with bulk queries (one UPDATE … FROM instead of N round trips). One case went from 267–397 s to 1 s.
- Run independent network calls a few at a time (`p-limit(4)`), respecting the provider's rate limit.
- **Read SDK retry defaults, not just timeouts.** Stainless-generated SDKs (Anthropic, OpenAI, Tabstack and others) retry 5xx, 429 and timeouts twice by default, so one bad request can hold a worker for 3× the timeout. When a fallback provider exists, set `maxRetries: 0` and a short `timeout`.
- Cap the nightly batch (`--limit`) so a monthly discovery spike drains over several nights instead of one long run.
- A batch that fails as a whole on one bad row (for example, an emoji split mid-surrogate) wastes the entire batch. Sanitize inputs before batching.

## 7. Flaky tests

- Rerun the failed job once before investigating. Starved runners cause timeout flakes (a 5 s test limit hit at 21 s in a run that took 19 min overall).
- If it keeps happening, loop the suspect test 15–20× in a draft-PR CI job, and upload failure screenshots (`tmp/screenshots` on Rails) as an artifact. If it won't reproduce, keep the screenshot upload, drop the loop, and leave the issue open.
