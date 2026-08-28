---
name: radar
description: "When you want to monitor known sources on a schedule and feed the good stuff into your second brain. Configure sources once (YouTube channels, RSS/blogs/newsletters, subreddits, Hacker News, Bluesky, Mastodon, X accounts, LinkedIn profiles, keyword searches), then each run fetches only what's new since last time, scores it for relevance against your stated focus, writes one digest note to the vault, and captures the high-signal items into raw/ automatically. Everything else stays in the digest until you promote it. Incremental by design — state files mean nothing is fetched or captured twice. Modes — run (poll everything due), digest (show/re-render the latest), promote (pull specific items into raw/ in full), add / sources / pause (manage the source list), doctor (health-check every source), schedule (install the daily launchd job). Triggers on \"/radar,\" \"run my radar,\" \"check my sources,\" \"what's new from my sources,\" \"add a source,\" \"monitor this channel,\" \"watch this subreddit,\" \"track this account,\" \"daily digest,\" \"promote item 4,\" \"radar doctor.\" Complements second-brain (radar fills raw/, second-brain compiles it) and deep-research (radar is standing surveillance, deep-research is a one-off dive)."
metadata:
  version: 0.2.0
---

# /radar — Standing surveillance on the sources you care about

`deep-research` answers a question you asked. `radar` surfaces the answers to questions you haven't asked yet, from sources you already trust, every day, without you going to look.

## Mental model

```
sources.yaml  →  fetch new only  →  score  →  digest  →  promote  →  raw/  →  /sb compile
  (config)        (state files)     (1–5)    (vault)    (you)      (vault)     (wiki)
```

Two hard rules keep this from becoming noise:

1. **Only one thing is written per run by default** — the digest. Individual `raw/` captures happen only for items that clear the auto-capture bar, or that you explicitly promote.
2. **Nothing is fetched twice.** Every source has a state file of seen item IDs. A run at 7am and a manual run at 9am produce no duplicates.

## Layout

| Path | What |
|---|---|
| `${MAKERSKILLS_CONFIG:-$HOME/.config/makerskills}/radar/sources.yaml` | The source list (private, gitignored) |
| `${MAKERSKILLS_CONFIG:-$HOME/.config/makerskills}/radar/interests.local.md` | Global relevance context — what you care about right now |
| `${MAKERSKILLS_CONFIG:-$HOME/.config/makerskills}/radar/state/<source-id>.json` | Seen-item IDs + last run per source |
| `${MAKERSKILLS_CONFIG:-$HOME/.config/makerskills}/radar/runs/<date>.json` | Machine-readable run record (backs `promote`) |
| `${MAKERSKILLS_CONFIG:-$HOME/.config/makerskills}/radar/logs/<date>.log` | Unattended-run stdout, for debugging a silent morning |
| `<vault>/outputs/radar/<YYYY-MM-DD>.md` | The human digest |
| `<vault>/raw/<type>-<slug>.md` | Captured items, in second-brain's schema |

`<vault>` is `${SECOND_BRAIN_VAULT:-$HOME/Documents/SecondBrain}`.

## Step 0 — Parse mode

| Invocation | Mode |
|---|---|
| `/radar` / `/radar run` / "check my sources" / "run my radar" | **run** |
| `/radar run <source-id>` | **run**, single source |
| `/radar digest` / "what's new from my sources" | **digest** |
| `/radar promote 3 7 12` / "promote item 4" / "capture the Isenberg one" | **promote** |
| `/radar add <type> <target>` / "monitor this channel" / "watch r/SaaS" | **add** |
| `/radar sources` / `/radar list` | **sources** |
| `/radar pause <id>` / `/radar resume <id>` / `/radar remove <id>` | **manage** |
| `/radar doctor` | **doctor** |
| `/radar schedule` | **schedule** |

If `sources.yaml` doesn't exist in any mode but `add`/`schedule`, run first-time setup: copy `references/templates/sources.example.yaml` into place, create `state/`, `runs/`, `logs/`, then walk the user through adding their first 3–5 sources. Don't run against the example file's placeholder sources.

Read `references/sources-schema.md` before touching `sources.yaml` in any mode.

---

## Mode: run

### Step 1 — Load

1. Read `sources.yaml`. Filter to `enabled: true` sources whose `cadence` is due (compare against each state file's `last_run`; `daily` = due if last run was on an earlier calendar day).
2. Read `interests.local.md` — this is the global relevance context every item gets scored against, on top of each source's own `focus`.
3. Read each due source's state file. Missing state file = first run for that source; use `defaults.first_run_lookback_days` (default 3) instead of "since last run" so a new source doesn't dump its entire archive.

### Step 2 — Fetch, in parallel

Read `references/fetchers.md` for the exact command per source type. Fetch every due source **in parallel** — they're independent, and a serial run over 15 sources is the difference between a 40-second morning job and a 6-minute one.

Rules that matter more than they look:

- **A failing source never fails the run.** Catch per-source errors, mark the source `degraded` with the error text, and carry on. A dead RSS feed must not cost you the YouTube results.
- **Cap per source** at `max_items_per_source` (default 15). If a source blew past the cap, say so in the digest — it usually means the lookback is too wide or the source got noisy.
- **Filter to new** by ID against the state file's `seen` list, then by `published` against the lookback window. Both, not either: IDs catch re-publishes, dates catch feeds that recycle IDs.
- **X and LinkedIn are the only unreliable types.** Everything else (youtube / rss / hn / bluesky / mastodon / reddit) has a keyless path that just works. X becomes reliable once `AUTH_TOKEN` + `CT0` are set; LinkedIn never fully does. When a chain is exhausted, mark degraded and move on — don't retry in a loop, don't let it block the digest.
- **Check credentials once, at the start.** Resolve `AUTH_TOKEN`/`CT0` and any paid keys (env → Keychain) before fetching, and skip the source types that need what's missing rather than discovering it per-item. `references/fetchers.md` → "Credentials" has the resolution order.

### Step 3 — Score

For each new item, produce a relevance score 1–5 against the source's `focus` + `interests.local.md`:

| Score | Meaning |
|---|---|
| **5** | Directly actionable for a named project or open question. You'd want this in the wiki. |
| **4** | Strong topical match with genuinely new information. |
| **3** | On-topic, but restates what you already know. |
| **2** | Tangential — same field, different concern. |
| **1** | Noise. Promo, engagement bait, off-topic. |

Score from the title + description/excerpt + whatever the feed gave you. **Do not fetch full content to score** — that's backwards, and it's what makes daily jobs slow and expensive. Full fetch happens on capture only.

Then bucket:

- `>= auto_capture_at` (default 5) → capture now, in full (Step 4)
- `>= list_at` (default 3) → listed in the digest as promotable
- below `list_at` → collapsed into a "skipped" count with titles in a `<details>` block. Never silently dropped — a bad filter must be visible.

Write the score's *reason* in one clause. "Names the exact attribution problem TracerKit solves" is useful. "Relevant to your interests" is not, and if that's the best you can write, the score is a 3.

### Step 4 — Capture the auto-captures

For each item at or above `auto_capture_at`, fetch the full thing and write it to `<vault>/raw/` following second-brain's schema (read that skill's capture conventions; the vault's `CLAUDE.md` is authoritative):

| Source type | Full fetch | raw/ prefix |
|---|---|---|
| youtube | `watch-video` in transcript mode | `resource-` |
| rss / keyword | `WebFetch` the article body | `article-` |
| reddit / hn | Fetch the post + top comments | `article-` (link posts: fetch the target) |
| bluesky / mastodon | `social-fetch` (public APIs — post + replies in one call) | `tweet-` |
| x | `social-fetch` | `tweet-` |
| linkedin | `social-fetch` | `bookmark-` |

Every captured file gets a header:

```markdown
source: <url>
captured: YYYY-MM-DD
via: radar/<source-id>
```

The `via:` line is what makes a bad source auditable later — when the wiki fills with mediocre pages, you can trace which source produced them.

### Step 5 — Write the digest

Render `references/templates/digest.md` to `<vault>/outputs/radar/<YYYY-MM-DD>.md`.

If a digest already exists for today (second run same day), **merge**: append the new items with continued numbering, update the run header's counts, and add a second run line. Never overwrite — the numbers in an existing digest may already have been used in a `promote` call.

### Step 6 — Persist state

Per source, write `state/<source-id>.json`: `last_run`, `last_status` (`ok` | `degraded` | `error`), `error` if any, and `seen` — the item IDs, capped at the most recent 300 (a feed rarely revisits further back, and unbounded state files are how this rots).

Write `runs/<YYYY-MM-DD>.json` with the full item list, each with its digest number, score, URL, source ID, and capture status. **`promote` reads this file**, so it must contain everything needed to fetch an item without re-polling the source.

### Step 7 — Commit the vault

Per the standing vault rule: `git -C "<vault>" pull --rebase --autostash`, commit the digest + captures in one semantic commit (`radar: 2026-08-28 digest — 34 items, 3 captured`), push. Pull first, always — an unattended job that force-diverges the vault is worse than one that doesn't run.

### Step 8 — Report

In an interactive session, print the digest summary inline — run stats, the captured items, the top 5 promotable ones by score, and any degraded sources. Don't print the full skipped list.

In an unattended run (`claude -p`), print the same thing to stdout; launchd captures it to `logs/<date>.log`.

---

## Mode: promote

`/radar promote 3 7 12` — pull specific digest items into `raw/` in full.

1. Read `runs/<date>.json` (today's by default; `/radar promote --date 2026-08-26 4` for an older digest).
2. Resolve each number to its item. Refuse cleanly on a number that doesn't exist or was already captured — say which, don't guess at intent.
3. Fetch + capture each exactly as Step 4 does.
4. Update the run record (`captured: true`) and the digest note — move the promoted lines into the Captured section with their `raw/` paths.
5. Commit + push.

Accept fuzzy references too: "promote the Isenberg one" → match against titles in the run record, confirm the match if there's more than one candidate.

## Mode: digest

Show today's digest. If none exists, say when the last run was and offer to run now. `/radar digest yesterday` or `/radar digest 2026-08-26` for a specific day. `/radar digest week` summarizes the last 7 days: totals per source, capture rate, and which sources produced nothing.

## Mode: add

`/radar add youtube @GregIsenberg`, `/radar add reddit r/SaaS`, `/radar add x @levelsio`, or just "monitor this channel" with a URL.

1. **Resolve the target** — read `references/fetchers.md` → "Resolving a target" for the per-type resolution (handle → channel ID, site URL → feed URL, etc.).
2. **Test-fetch immediately.** A source that can't be fetched must never be written to `sources.yaml`. Show the user the 3 most recent items as proof it works.
3. **Ask for the focus line** if it isn't obvious from context. This is the single highest-leverage field in the whole config — it's what scoring runs against. Propose one from the test-fetch results and let the user correct it.
4. Append to `sources.yaml` with a kebab-case `id` (`yt-greg-isenberg`, `rd-saas`). Don't create the state file — first run handles it, with the first-run lookback.

## Mode: sources

Table of every source: id, type, target, enabled, cadence, last run, last status, items seen in the last 7 days, capture rate. Sort degraded/erroring sources to the top.

Flag two failure patterns explicitly, because they're the ones that quietly waste a daily job:

- **Dead weight** — a source with 0 captures in 30+ days. Suggest tightening `focus` or removing it.
- **Firehose** — a source repeatedly hitting `max_items_per_source`. Suggest a narrower target or a shorter lookback.

## Mode: doctor

Health-check without writing anything to the vault:

1. Config parses; every source has `id`, `type`, `focus`; IDs are unique.
2. Env: `SECOND_BRAIN_VAULT` set and the vault writable; vault is a git repo with a remote; `MAKERSKILLS_CONFIG` set.
3. Every enabled source test-fetches (in parallel), reporting per-source OK / degraded / broken with the actual error.
4. Credentials, and **where each resolved from** (env vs Keychain vs absent): `AUTH_TOKEN` + `CT0` (free, unlocks X), `$SCRAPECREATORS_API_KEY` / `$APIFY_API_TOKEN` (paid, X/LinkedIn/IG), `BSKY_*` (rarely needed — public reads are keyless). No key is required for youtube / rss / hn / bluesky / mastodon / reddit. Flag expired X cookies as "re-grab from x.com," not as a broken source.
5. The launchd job is loaded and its last exit status.

Output a fix list, most-broken first. Run this before blaming the skill for a quiet morning.

## Mode: schedule

Installs the daily job. Read `references/scheduling.md` — it has the plist template, the `PATH`/env gotchas that make unattended `claude -p` runs fail silently, and the verification steps.

Defer to `loopify` if the user wants something other than a fixed daily run (interval polling, conditional bail-outs, dynamic pacing).

---

## Notes on quality

- **The digest is the product.** If the digest isn't worth reading in 90 seconds, the source list is wrong — fix the sources, don't fix the digest format.
- **Prune quarterly.** The natural failure mode of this skill is source creep: 40 sources, 200 items a day, nothing captured. `sources` mode exists to catch that; act on what it flags.
- **Scoring is not fetching.** Score from metadata; fetch on capture. Reversing this is what turns a cheap daily job into an expensive one.
- **Degraded ≠ broken.** X and LinkedIn will fail intermittently forever. Report it in the digest, don't escalate it, don't retry-loop it.
- **Never write to `Projects/`, `Daily/`, `Inbox/`, `Notes/`, `Templates/`, `Tasks.md`, `Kanban.md`, or `Home.md`.** radar owns exactly two paths in the vault: `outputs/radar/` and new files in `raw/`.

## Composes with

- `second-brain` — radar fills `raw/`, `/sb compile` turns it into wiki pages. A good rhythm is radar daily, compile weekly. Captured files carry `via: radar/<source-id>` so compilation can trace provenance.
- `watch-video` — full-fetch path for YouTube captures (transcript mode; escalate to visual mode manually if a video earns it).
- `social-fetch` — full-fetch path for every social item, and the owner of the per-platform strategy ladders. Radar deliberately does not reimplement them; when a chain changes, it changes there. Radar also shares its cache at `~/Documents/social-fetches/_cache/`.
- `last30days` — available as a `keyword` engine, and the source of radar's free X path (it vendors the `bird-search` client) and the keyless Reddit techniques. Worth re-reading when a platform's access breaks; it tracks these endpoints closely.
- `deep-research` — escalation path. When a digest item is interesting enough to need context radar can't give, hand the URL to deep-research.
- `loopify` — scheduling judgment beyond the default daily launchd job.
- `jab-hook` — high-scoring items are content raw material; a `Content Ideas` wiki page is the handoff point.
- `business-brainstorm` — a keyword source watching a market you're considering feeds the idea filter with live signal.
