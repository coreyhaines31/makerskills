# Inspiration accounts

**Your personal list lives at `${MAKERSKILLS_CONFIG:-$HOME/.config/makerskills}/jab-hook/inspiration.local.md`** — not in this repo (gitignored, on disk only). The list of operators you're learning from is your taste — keep it private.

See `inspiration.example.md` in this directory for the schema + setup instructions.

## How the skill loads it

1. Read `${MAKERSKILLS_CONFIG:-$HOME/.config/makerskills}/jab-hook/inspiration.local.md` for the personal account list
2. If missing, skip the inspiration scan (skill still works, just without external pattern pull)

## Pattern library — also local

When the skill extracts hook patterns / structural patterns from inspiration-account posts, it writes them to:

`${MAKERSKILLS_CONFIG:-$HOME/.config/makerskills}/jab-hook/patterns.local.md`

This file is also gitignored. The pattern library grows with use and stays your private playbook.

## Methodology (this stays public — it's the recipe, not the data)

When drafting a `promo` or `educational` post:

1. Pick 1–2 accounts from your inspiration list whose audience overlaps the property being promoted
2. Pull their recent posts via `social-fetch`
   - LinkedIn: `agent-browser` with modal dismissal (no API key needed) or ScrapeCreators if `SCRAPECREATORS_API_KEY` set for full post data
   - X: ScrapeCreators recommended; free tier returns preview only
3. Extract: **hook openers**, **structural patterns** (numbered list / contrarian-take / story-open), **CTA styles**, **post length**, **line-break rhythm**
4. Choose ONE pattern that fits the property + content type
5. Apply the pattern to YOUR voice — don't mimic their voice, only the structure

## Notes

- LinkedIn often blocks unauthenticated scraping. If `agent-browser` walls, fall back to: pasting examples, pulling from their public newsletters, or scraping their X accounts.
- Never copy phrasing — only structure, format, hook archetype.
- Inspiration is a starting point. Your voice rules in `voice.md` (+ `voice.local.md` overlay) always override format choices.
