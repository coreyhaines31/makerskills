# Examples

One worked example per skill — what you say, what the skill produces (abbreviated for readability).

**Note**: outputs are hand-authored illustrations, not literal captures. Real invocations produce longer, more detailed responses. Your mileage will vary depending on model, context, and the personal-config layer.

---

## `skillify`

**You:** *"Extract a skill from what we've been doing this session."*

**Skillify:** Reads back through the conversation, identifies the workflow pattern, asks 3 clarifying questions (trigger, edge cases, references), drafts the SKILL.md, scaffolds `skills/<name>/SKILL.md` + `references/`, updates the target repo's README, commits, and returns the path + commit hash.

For CREATE / ADAPT / UPDATE mode routing, invocation shape:

```
/skillify                          # from-chat (default in a conversation)
/skillify from-video <url>         # from-video (records → visual mode → SKILL.md)
/skillify from-scratch weekly-review
/skillify https://github.com/matt/skills/blob/main/wizard/SKILL.md  # ADAPT mode
/skillify update jab-hook cadence  # UPDATE mode, targeted
```

---

## `toolify`

**You:** *"Integrate Stripe into this Next.js project."*

**Toolify:** Detects the category (payments), asks the 9 structural questions (auth pattern, env var naming, official SDK vs raw fetch, webhook needed, where the client wrapper lives, etc.), fetches current Stripe docs via `context7`, scaffolds:

```
src/lib/stripe.ts                    # client singleton
src/app/api/webhooks/stripe/route.ts # webhook handler with signature verification
src/app/api/stripe/example/route.ts  # one working example route
.env.local.example                    # env var template
```

Adds `STRIPE_SECRET_KEY` + `STRIPE_WEBHOOK_SECRET` to `.env.local` (via `vercel env add --no-sensitive --value`), pins the SDK version in `package.json`, runs a smoke-test curl, and reports what to add manually (the webhook URL in Stripe dashboard).

---

## `loopify`

**You:** *"Set up a loop that pulls the Fathom call transcripts every night."*

**Loopify:** Asks the 5 essential questions (frequency, stop condition, loop body, output destination, failure mode). Detects cadence pattern (predictable timing → cron). Registers via `CronCreate`:

```
CronCreate({
  schedule: "0 6 * * *",           // daily at 6am
  timezone: "America/Los_Angeles",
  prompt: "Pull yesterday's Fathom transcripts into ~/Documents/CompanyBrain/meetings/. Dedupe by transcript ID."
})
```

Returns the `cron_id` + instructions on how to stop it (`CronDelete <cron_id>`). Documents idempotency (dedupe by transcript ID) so the loop can fire twice safely. Bails out on 3 consecutive failures.

---

## `decide`

**You:** *"Should I hire a full-time content editor or keep freelance?"*

**Decide:** Picks 6 of the 38 questions from the 37signals framework based on the decision's shape (hiring / cost / capacity questions). Asks one at a time. Captures answers verbatim. Produces:

```markdown
# Hire vs freelance content editor (2026-07-01)

## Decision
Keep freelance for 6 more months, then reassess.

## Why
Q7 (What's the smallest test that could kill this?): freelance experiment already running,
too early to lock a hire. Q19 (What are you giving up?): $10k/mo FTE budget can go
toward 3 different freelance experiments instead. Q34 (Principles bending?): none.

## Revisit
2027-01-01 — reassess based on Q4 result and Q19 outcomes.
```

Archives to `references/decisions-archive/2026-07-01-hire-vs-freelance-editor.md`, appends to `INDEX.md`.

---

## `business-brainstorm`

**You:** *"Should I build a Kit-vs-Beehiiv comparison tool for creators?"*

**Business-brainstorm:** Runs the idea through 9 dimensions (problem clarity, audience specificity, wedge, monetization path, moat, portfolio fit, distribution, energy fit, opportunity cost). Scores each ✓ / ⚠️ / ❌. Checks `.com` availability via `/domain`. Verdicts one of: **Build / Sleep on it / Kill**.

Output shape:

```markdown
# Kit vs Beehiiv comparison tool

## Verdict: Sleep on it (30-day revisit: 2026-08-01)

## Dimensions
Problem: ⚠️ (real but small — <500 creators/month evaluating)
Audience: ✓ (creators with 1k-10k subs deciding to migrate)
Wedge: ⚠️ (no obvious edge over "read both blogs")
Monetization: ❌ (affiliate revenue would be <$2k/mo unrealistic)
Moat: ❌ (both vendors could publish own comparison)
Portfolio fit: ✓ (SwipeWell / SwipeFiles adjacent audience)
Distribution: ✓ (existing audience knows creator-tool space)
Energy fit: ⚠️ (mostly maintenance work, not building)
Opportunity cost: ❌ (Marketing Skills / Founding Marketing bigger)

## Angle to steal (even if killed)
- Add a "which ESP" quiz to SwipeWell — one afternoon of work, no infra
```

Archives to `references/ideas-archive/2026-07-01-kit-vs-beehiiv-tool.md`.

---

## `deep-research`

**You:** *"Research the current state of AI-native email marketing platforms."*

**Deep-research:** Restates the question, picks a strategy chain (WebSearch → `/last30days` for freshness → WebFetch on top-5 hits → agent-browser on paywalled sources → cross-check memory). Produces:

```markdown
# AI-native email marketing platforms — 2026-07-01

## TL;DR
5 platforms explicitly positioning as AI-native (Kit + AI, Beehiiv + AI, Substack AI,
new: Mailglow, Elevate). Differentiation is mostly UI polish over ESP + generic LLM
prompt; only Mailglow has a proprietary personalization model.

## Findings
[detailed breakdown by platform, with citations]

## Sources
- kit.com/blog/kit-ai (2026-06-15) — official positioning
- beehiiv.com/podcast/ep-42 (2026-06-18) — CEO on AI roadmap
- [17 more citations]

## Adjacent
- RightMessage MCP for site personalization
- Personalize-first tools (Superhuman AI email inbox)

## Not found
- Objective performance benchmarks (all sources are vendor-authored)
```

Archives to `references/research-archive/2026-07-01-ai-native-esps.md`.

---

## `domain`

**You:** *"Find me a great .com for an AI-marketing coaching product."*

**Domain:** Asks budget ($250-$1k? $1k-$2k?). Brainstorms 30 candidates (real-word mashups, `try/use/with/join + word` prefixes, `word + ly/labs` suffixes). Runs Vercel dry-run for availability + price. Cross-checks whois. Aggregates via Domainr + Namecheap. Reports:

```
AVAILABLE NOW ($10-30/yr):
- coachai.com (Vercel: available, $12/yr)
- withaimarketing.com (Vercel: available, $16/yr)

AFTERMARKET (under $1k budget):
- aimarketer.com — TAKEN, HugeDomains: $795
  https://www.hugedomains.com/domain-profile.cfm?d=aimarketer&e=com

AFTERMARKET (over budget):
- promptmarketer.com — TAKEN, Sedo asking $4,500

TAKEN, NO LISTING FOUND:
- aicoach.com, marketai.com, aimktg.com
```

For top 3 candidates, runs USPTO trademark screening via `agent-browser` and social-handle checks on X + LinkedIn.

---

## `second-brain`

**You:** *"Capture this article: https://every.to/superorganizers/how-i-built-my-second-brain"*

**Second-brain (capture mode):** Fetches the article, saves to `<vault>/raw/article-how-i-built-my-second-brain-every.md` with front-matter:

```markdown
source: https://every.to/superorganizers/how-i-built-my-second-brain
captured: 2026-07-01
```

Reports the path + a one-line summary. Doesn't compile into the wiki yet — that's a separate `/sb compile` pass.

**You (later):** *"Compile the wiki."*

**Second-brain (compile mode):** Grep raw/*.md against wiki/*.md `## Sources` sections to find unprocessed captures. Reads each. For the article above: extracts key concepts (Zettelkasten adaptation, weekly review discipline, output-driven consumption). Merges into existing `[[Second Brain Systems]]` wiki page (or creates it if missing). Updates `wiki/INDEX.md`. Adds source citation to the wiki page's `## Sources` section.

---

## `company-brain`

**You:** *"Capture this meeting: [pasted Fathom transcript from 2026-06-30 Acme discovery call]"*

**Company-brain (capture mode):** Detects `meetings/` as the target dir. Saves to `<vault>/meetings/2026-06-30-acme-discovery.md` with multi-author front-matter:

```markdown
source: Fathom recording (call with Acme on 2026-06-30)
author: @alex
captured: 2026-06-30
sensitivity: internal
attendees: [alex, sam, jane-doe (Acme CTO)]
company: acme
duration_min: 45
recording_url: https://fathom.video/share/xxx
```

Extracts the transcript text into the body. Reports path.

**You (later):** *"Compile the company wiki."*

**Company-brain (compile mode):** Merges the Acme meeting into an existing `[[Acme Corp Deal]]` wiki page (or creates it). Attribution in `## Sources`: `meetings/2026-06-30-acme-discovery.md (added by @alex)`. Inherits `internal` sensitivity. Links to `[[Discovery Call Playbook]]` (SOP page). If jane-doe isn't in `people/` yet, prompts to create her profile.

---

## `read-book`

**You:** *"Take chapter notes on this: ~/Documents/books/atomic-habits.pdf"*

**Read-book:** Reads the PDF, detects TOC + chapter boundaries, extracts per-chapter notes:

```markdown
# Atomic Habits — Chapter 4: The Man Who Didn't Look Right

## Key ideas
- Cue → craving → response → reward loop
- Habits are context-dependent (Pavlov's dogs, addiction environments)
- Behavior is a function of the person AND their environment

## Quotes worth keeping
- "Environment is the invisible hand that shapes human behavior." (p. 62)
- "You do not rise to the level of your goals. You fall to the level of your systems." (p. 27)

## Applications
- Redesign the phone's home screen to reduce social-media cue exposure
- Move the guitar out of the closet, onto the couch

## Open questions
- How to modify environments you don't control (office, co-parenting)?
```

Saves to `~/Documents/books/atomic-habits-notes/ch-04.md`. Also generates a `summary.md` at the end covering all chapters.

---

## `watch-video`

**You:** *"Transcribe this Loom: https://loom.com/share/abc123def"*

**Watch-video (transcript mode):** Uses yt-dlp to download at 720p, checks for Loom's built-in transcript first (usually available), falls back to MLX-Whisper local if not. Produces:

```
~/Documents/videos/loom-onboarding-walkthrough-2026-07-01/
├── video.mp4
├── transcript.txt
└── metadata.json
```

One-line chat summary: *"Loom transcript captured — 12 min, 2,400 words, saved to ~/Documents/videos/loom-onboarding-walkthrough-2026-07-01/"*

**You:** *"Now watch that Loom in visual mode."*

Runs frame extraction (1 frame per 5s since it's a screen-share), pairs frames with transcript chunks, batches to Claude vision for key-moment identification. Produces `moments.md` with per-timestamp screen state + transcript + notes, then a `summary.md` with TL;DR + Key moments + Action items flagged + Decisions flagged.

---

## `jab-hook`

**You:** *"Plan my socials for next week."*

**Jab-hook (plan mode):** Reads `~/.config/makerskills/jab-hook/properties.yaml` (your rotation portfolio) + recent Typefully drafts (last 30 days). Computes days-since-last-promo per property. Outputs:

```markdown
# Week of 2026-07-07 — social plan

| Day | Type | Property/Topic | Draft summary |
|---|---|---|---|
| Mon | Promo | SwipeWell (23 days overdue) | ORB framework applied to email newsletters |
| Tue | BIP | — | shipped v0.5.0 of makerskills last night |
| Wed | Edu | — | first-principles thinking applied to positioning |
| Thu | Promo | Truelist | new B1 logo + brand walkthrough |
| Fri | BIP | — | last week's stats: X + LinkedIn |
| Sat | Edu | — | why "Composes with" sections matter in AI skills |
| Sun | (rest) | — | — |
```

Asks: *"Draft each one now, or in sequence?"* Drafts push to Typefully as drafts (not scheduled) for human review.

---

## `slide-deck`

**You:** *"Draft a 15-slide keynote called Marketing Like an Engineer for MicroConf 2026."*

**Slide-deck (new mode):** Asks the 7 setup questions (audience: MicroConf B2B SaaS founders; length: 15; density: speaker-led; CTA: rethink positioning; slug: marketing-like-an-engineer; content state: rough notes). Proposes 3 narrative angles:

```
Safe: "The 5-part framework for engineering-native marketing"
Bold: "Marketing is engineering. The founders who see it first win."
Wildcard: "One product I've watched die from marketing malpractice"
```

You pick Bold. Outlines 15 slides across 4 sections. Expands each slide with primitives (`Eyebrow`, `Heading`, `Accent`, `BulletList`). Writes speaker notes (3-5 lines per slide, meant to be read aloud verbatim). Generates `page.tsx` + `layout.tsx` in `${SLIDE_DECK_REPO}/src/app/slides/marketing-like-an-engineer/`. Verifies dev server + prints preview URL.

Later: `/slide-deck export marketing-like-an-engineer pdf` → Playwright snapshots each slide at 1920×1080, combines to PDF via `img2pdf`, saves to `~/Documents/slide-exports/marketing-like-an-engineer-2026-07-01.pdf`, opens in Preview.

---

## `pm`

**You:** *"What should I work on next?"*

**Pm (next mode):** Reads `~/.config/makerskills/pm/boards.md` (your business list + tool per business). Queries each board's Ready column via the appropriate adapter (Notion, GitHub, Plane, Linear, Obsidian, or manual). Applies Eisenhower matrix across the portfolio. Reports:

```markdown
Next up: **Truelist — B1 logo variants ready for review** (Q1: Urgent + Important)

Why: 4 days on the Ready column, blocking the marketing site launch scheduled for
2026-07-08. Zach flagged 3 variants; picking one unblocks the next 4 downstream cards.

If not that:
- CF — Client Acme discovery synthesis (Q2: Not Urgent + Important, 2 days on Ready)
- SwipeWell — pricing page copy (Q2, 6 days on Ready, waiting on brand voice sign-off)

WIP check: In Progress at 2/3 on Truelist board. Safe to pull next.
```

---

## `personal-cfo`

**You:** *"Model buying this house: $1.4M, 20% down, 6.5% 30-yr, plus $180K renovation with an ADU rental at $2,400/mo."*

**Personal-cfo (house mode):** Asks the full input questionnaire (property taxes, HOA, insurance, current housing cost, income, tax bracket, time horizon). Runs 4 scenarios (Baseline / A: ADU only / B: ADU + 1 bedroom / C: full house-hack). Produces:

```markdown
| Scenario | Yr 1 net | Yr 5 net | Yr 10 net | Yr 30 net | Notes |
|---|---|---|---|---|---|
| Baseline | -$4,200/mo | -$50K | -$102K | -$308K | No rental income |
| A: ADU | -$1,800/mo | -$22K | -$45K | -$135K | $2,400/mo ADU rent, 6% vacancy |
| B: ADU + 1 br | -$300/mo | -$4K | -$7K | -$22K | Add roommate $1,400/mo |
| C: full house-hack | +$1,100/mo | +$14K | +$28K | +$83K | 3 rentals, mgmt in-house |
```

Archives to `references/scenarios-archive/2026-07-01-1400k-house-with-adu.md`.

---

## `company-cfo`

**You:** *"Run the June CFO snapshot."*

**Company-cfo (monthly mode):** Loads `${COMPANY_CFO_ROOT}/CLAUDE.md` (your methodology + data source map). Pulls bank + payment processor + payroll + expense-mgmt data for June. Categorizes outflows (distributions / team / software / reimbursements / benefits / other). Computes EOM cash via transaction-sum method. Updates the scenario projector's `HISTORICAL` array + `startingCash`. Writes `${COMPANY_CFO_ROOT}/reports/monthly/2026-06.md`:

```markdown
# 2026-06 monthly snapshot

## TL;DR
Net cash: +$8,200. Ending balance: $187,400. MRR: $94,100 (up $2,400 m/m).
Runway: 6.2 months at current burn. 3/3 partner distributions paid.
Recommendation: hold hiring; revisit August with Q2 results.

[detailed sections follow]
```

Commits + PRs the changes to the `company-cfo` repo per your git workflow.

---

## `paste`

**You (with terminal output in clipboard):** *"/paste linkedin"*

**Paste:** Reads clipboard, strips ANSI escape codes, converts terminal formatting to LinkedIn-compatible (unicode bold via `𝗔𝗕𝗖`, italic via `𝘈𝘉𝘊`), scans for API keys or secrets first (prompts if any detected), warns at 2,500 chars (LinkedIn max 3,000), copies back to clipboard, prints preview:

```
Cleaned for LinkedIn (1,847 chars — under 3,000 limit)
Preview:
─────
𝗦𝗵𝗶𝗽𝗽𝗲𝗱 𝘃𝟬.𝟱.𝟬 𝗼𝗳 𝗺𝗮𝗸𝗲𝗿𝘀𝗸𝗶𝗹𝗹𝘀

Now with domain: 11-step .com hunt built on Laura Roeder's...
[etc.]
─────
Reminder: link goes in first comment, not body. Suggested comment:
https://github.com/coreyhaines31/makerskills/releases/tag/v0.5.0
```

---

## `social-fetch`

**You:** *"Fetch this: https://x.com/gregisenberg/status/1234567890"*

**Social-fetch:** Detects platform (X). Runs strategy chain: (1) Twitter oEmbed (free) → (2) `agent-browser` with modal dismissal → (3) ScrapeCreators API if `$SCRAPECREATORS_API_KEY` set. Returns structured JSON:

```json
{
  "platform": "x",
  "url": "https://x.com/gregisenberg/status/1234567890",
  "posted_at": "2026-06-28T14:22:00Z",
  "author": {
    "handle": "gregisenberg",
    "name": "Greg Isenberg",
    "verified": true
  },
  "text": "The next $100B market: selling to AI agents...",
  "engagement": {
    "likes": 4200,
    "reposts": 850,
    "replies": 130
  },
  "media": [],
  "strategy_used": "scrapecreators"
}
```

Caches to `~/Documents/social-fetches/_cache/x-1234567890.json` (24h TTL) so downstream calls don't re-hit the API.
