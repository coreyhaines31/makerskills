---
name: social
description: When Corey wants to plan, pick the next post, audit coverage, or draft + syndicate personal social posts on X and LinkedIn. Enforces a portfolio rotation so each of his six properties (Conversion Factory, Swipe Files, Magister, Truelist, Marketing Skills, ebooks) gets promoted at least once every ~3 weeks, with build-in-public and educational content filling the rest. Drafts go into his personal Typefully workspace via MCP. Triggers on "what should I post," "plan my socials," "next promo," "social rotation," "promote [property]," "BIP post," "audit my socials," "what haven't I posted about." This is for Corey's personal feed — for CF partner syndication use cf-skills:x-li, for generic frameworks use marketing-skills:social.
metadata:
  version: 0.1.0
---

# /social — Personal portfolio rotation + drafting

Keeps Corey's personal X + LinkedIn feed consistently promoting his six properties while mixing in build-in-public and educational content. Drafts to personal Typefully workspace.

## Mental model

- **6 rotation slots** (see `references/properties.md`): Conversion Factory, Swipe Files, Magister, Truelist, Marketing Skills, ebooks-rotating
- **~2 promo posts/week** → each property cycles every ~3 weeks at equal weight
- **Non-promo days**: 50/50 build-in-public vs educational
- **Target weekly rhythm**: ~2 promo + ~2–3 BIP + ~2–3 educational
- **Platforms**: X + LinkedIn via Corey's personal Typefully workspace

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
4. Pull recent posts from Corey's personal Typefully workspace:
   - First run: call `mcp__typefully__typefully_list_social_sets` and ask which social set is Corey's personal (X + LinkedIn). Save the ID to `references/typefully-config.md` for future runs.
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

For **promo** posts, always end with the property URL on its own line. For LinkedIn, put a blank line before the URL — no embedded links inside the body.

## Step 5 — Syndicate to Typefully

Ask: *"Push to Typefully now? (X + LinkedIn, your personal workspace)"*

If yes:
1. Read social set ID from `references/typefully-config.md`
2. Call `mcp__typefully__typefully_create_draft` once for X, once for LinkedIn (or once with both platforms if the social set spans both)
3. Default to **draft** state (not scheduled) — Corey reviews in Typefully UI before sending
4. Return the Typefully draft URLs

## Cross-references

- `cf-skills:x-li` — for posts syndicated across all three CF partner accounts (Corey + Zach + Nick). Use that instead when the post should land on the CF/agency accounts.
- `marketing-skills:social` — generic social frameworks, useful for client work or when teaching social strategy.
- `marketing-skills:copywriting` — for hook / headline ideation when stuck.
- Memory: `feedback_cf_promo_voice.md` (conviction-coded CTAs, reader-perspective framing) — voice principles also apply to Corey's personal promo posts.
- Memory: `feedback_cf_social_cadence.md` — CF-specific cap of 2 posts/day per platform. Same cap is sensible for Corey's personal account.
