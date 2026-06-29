# Inspiration accounts (example / template)

**Copy this file to `${MAKERSKILLS_CONFIG:-$HOME/.config/makerskills}/jab-hook/inspiration.local.md` and replace with your real list.** The local copy is gitignored.

## Setup

```bash
mkdir -p ~/.config/makerskills/jab-hook
cp skills/jab-hook/references/inspiration.example.md \
   ~/.config/makerskills/jab-hook/inspiration.local.md
# Then edit ~/.config/makerskills/jab-hook/inspiration.local.md with your real accounts
```

## Schema

A list of operators / creators whose social content you want to learn formats, hooks, and structures from. Not voices to copy — patterns to study.

```markdown
# Inspiration accounts

## Accounts

| Name | LinkedIn | Why |
|---|---|---|
| <Real Name> | https://www.linkedin.com/in/<handle> | <1-line note on why — their angle, niche, what they do well> |
| <Real Name> | https://twitter.com/<handle> | <note> |
| <Real Name> | https://bsky.app/profile/<handle> | <note> |
```

X / LinkedIn / Bluesky / wherever — the platform doesn't matter; the skill handles each via `social-fetch`.

## How `jab-hook` uses your list

When drafting a `promo` or `educational` post, the skill:

1. Picks 1–2 accounts whose audience or angle aligns with the property being promoted
2. Pulls their recent posts (via `social-fetch` — uses `agent-browser` for LinkedIn if no paid keys; ScrapeCreators for full X threads when `SCRAPECREATORS_API_KEY` is set)
3. Extracts: **hook openers**, **structural patterns** (numbered list, contrarian-take, story open), **CTA styles**, **post length**, **line-break rhythm**
4. Chooses one pattern that fits the property + content type
5. Applies the pattern to YOUR voice (don't mimic their voice — only the structure)

Extracted patterns accumulate in `${MAKERSKILLS_CONFIG:-$HOME/.config/makerskills}/jab-hook/patterns.local.md` (also gitignored — your patterns library grows over time and stays private).

## Notes

- LinkedIn often blocks unauthenticated scraping. If `agent-browser` walls, fall back to: pasting examples, pulling from their public newsletters, or scraping their X accounts.
- Never copy phrasing — only structure, format, hook archetype.
- Inspiration is a starting point. Your voice rules in `voice.md` (+ `voice.local.md` overlay) always override format choices.
