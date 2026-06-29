---
name: jab-hook
description: Gary Vaynerchuk's jab-jab-jab-right-hook framework applied to a personal portfolio rotation on X and LinkedIn. Jabs = build-in-public + educational (value). Hooks = promo (the ask). Each property in the user's configured portfolio (see `~/.config/makerskills/jab-hook/properties.yaml`) gets a hook at least once every ~3 weeks; jabs fill the rest. Drafts go into the user's Typefully workspace via MCP. Modes — plan (7-day plan), pick-next (single post), audit (coverage report), draft (specific post). Triggers on "/jab-hook," "what should I post," "plan my socials," "next promo," "next jab," "next hook," "social rotation," "promote [property]," "BIP post," "audit my socials," "what haven't I posted about."
metadata:
  version: 0.3.0
---

# /jab-hook — Jab-jab-jab-right-hook for a personal portfolio

Gary Vaynerchuk's framework applied to your configured portfolio: keep the feed mostly *jabs* (value — BIP + educational) so the *hooks* (promo) earn attention when they land. Drafts to your personal Typefully workspace.

**One-time setup**: see `references/properties.md` and `references/typefully-config.md` to configure your real portfolio + workspace. Personal config lives in `${MAKERSKILLS_CONFIG:-$HOME/.config/makerskills}/jab-hook/`.

## Mental model

- **N rotation slots** (configured in `~/.config/makerskills/jab-hook/properties.yaml`): one per property you want to promote on rotation
- **~2 promo posts/week** → each property cycles every ~3 weeks at equal weight
- **Non-promo days**: 50/50 build-in-public vs educational
- **Target weekly rhythm**: ~2 promo + ~2–3 BIP + ~2–3 educational
- **Platforms**: X + LinkedIn via your personal Typefully workspace

## Step 1 — Pick the mode

Detect from the trigger:

| User says | Mode |
|---|---|
| "plan my socials," "next week's posts" | **plan** |
| "what should I post," "next promo," "pick next" | **pick-next** |
| "audit my socials," "what's overdue," "what haven't I posted about" | **audit** |
| "draft a promo for X," "BIP post about Y," "educational about Z" | **draft** |

If ambiguous, confirm.

## Step 2 — Load context

1. Read `references/properties.md` — the 6 rotation slots and angle ideas
2. Read `references/voice.md` — Corey's voice rules per platform
3. Read `references/content-types.md` — templates for promo / BIP / educational
4. Pull recent posts from your personal Typefully workspace:
   - First run: call `mcp__typefully__typefully_list_social_sets` and ask which social set is your personal (X + LinkedIn). Save the ID to `references/typefully-config.md` for future runs.
   - Call `mcp__typefully__typefully_list_drafts` filtered to the last 30 days
   - Classify each as promo / BIP / educational by content
5. Compute **days since last promo** for each of the 6 slots

## Step 3 — Mode logic

### plan (7-day plan)
- Slot the 1–2 most overdue properties as **promo** posts
- Fill remaining 5 days with **alternating** BIP and educational (50/50)
- Output as a table: `Day | Type | Property/Topic | Hook | Draft summary`
- Don't stack two promo on consecutive days
- After Corey approves the plan, offer to draft each one in sequence

### pick-next
- Identify the most overdue property
- If most overdue < 14 days, suggest a BIP or educational instead (whichever is less recent)
- Draft 1 post; ask before syndicating

### audit
- Report: days since last promo per property, ordered by most overdue
- Flag any property >21 days as overdue
- Suggest the next 1–2 moves

### draft
- Skip rotation logic — draft the requested post
- Use the right content-type template

## Step 4 — Draft

Follow `references/voice.md` and `references/content-types.md`. Default: **single post**, one per platform (X version + LinkedIn version). Thread only if the second post earns its place.

**Link placement (load-bearing)**: never put a URL in the body. Default is no link at all — let curiosity drive the click. When a link is needed, draft it as a **first comment** for LinkedIn (Typefully supports auto-comment) or a **reply** for X. The body always stands alone.

### Optional: inspiration scan

For `promo` and `educational` posts, optionally scan inspiration accounts (`references/inspiration.md`) before drafting:

1. Pick 1–2 accounts whose audience overlaps with the property
2. Pull recent posts (agent-browser if it works on LinkedIn; otherwise ask Corey to paste examples or fall back to their X/newsletter)
3. Extract structural patterns: hook openers, post length, line-break rhythm, CTA styles
4. Apply ONE pattern to Corey's voice — never mimic phrasing
5. Log new patterns in `references/patterns.md` (create if missing) so they accumulate

Skip inspiration scan when Corey says "just draft it" or when iterating on an existing post.

## Step 5 — Syndicate to Typefully

Ask: *"Push to Typefully now? (X + LinkedIn, your personal workspace)"*

If yes:
1. Read social set ID from `references/typefully-config.md`
2. Call `mcp__typefully__typefully_create_draft` once for X, once for LinkedIn (or once with both platforms if the social set spans both)
3. If the draft has a first-comment link, configure Typefully to add it automatically (LinkedIn auto-comment / X reply). If the MCP doesn't support auto-comment for one of the platforms, surface the comment text so Corey can paste it after publishing.
4. Default to **draft** state (not scheduled) — Corey reviews in Typefully UI before sending
5. Return the Typefully draft URLs

## Cross-references

- `cf-skills:x-li` — for posts syndicated across all three CF partner accounts (Corey + Zach + Nick). Use that instead when the post should land on the CF/agency accounts.
- `marketing-skills:social` — generic social frameworks, useful for client work or when teaching social strategy.
- `marketing-skills:copywriting` — for hook / headline ideation when stuck.
- Memory: `feedback_cf_promo_voice.md` (conviction-coded CTAs, reader-perspective framing) — voice principles also apply to your personal promo posts.
- Memory: `feedback_cf_social_cadence.md` — CF-specific cap of 2 posts/day per platform. Same cap is sensible for your personal account.
