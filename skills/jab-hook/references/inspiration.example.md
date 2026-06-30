# Inspiration accounts (example / template)

**Copy this file to `${MAKERSKILLS_CONFIG:-$HOME/.config/makerskills}/jab-hook/inspiration.local.md` and replace with your real list.** The local copy is gitignored.

## Setup

```bash
mkdir -p ~/.config/makerskills/jab-hook
cp skills/jab-hook/references/inspiration.example.md \
   ~/.config/makerskills/jab-hook/inspiration.local.md
# Then edit ~/.config/makerskills/jab-hook/inspiration.local.md with your real accounts
```

## Schema — organize by platform

What works on LinkedIn doesn't work on X (and vice versa). Organize the file with one section per platform you draft for. The `jab-hook` skill scans accounts from the section matching the draft's target platform.

```markdown
# Inspiration accounts

## LinkedIn
Long-form professional, carousels, framework breakdowns.

| Name | LinkedIn | Why |
|---|---|---|
| <Real Name> | https://www.linkedin.com/in/<handle> | <1-line note — their niche, angle, what they do well> |

## X (Twitter)
Short, punchy, thread mechanics, reply-as-content.

| Name | X handle | Why |
|---|---|---|
| <Real Name> | https://x.com/<handle> | <note> |

## Instagram
Visual-first, reel-driven.

| Name | Instagram | Why |
|---|---|---|
| <Real Name> | https://www.instagram.com/<handle> | <note> |

## TikTok
Vertical video, hook-heavy, trend-aware.

| Name | TikTok | Why |
|---|---|---|

## YouTube
Long-form video. (More relevant to youtubeskills than jab-hook.)

| Name | YouTube | Why |
|---|---|---|

## Bluesky / Threads / Mastodon / other

| Name | Platform | URL | Why |
|---|---|---|---|
```

Only fill in sections for platforms you actually draft for. Leave others as placeholders.

## Same operator, two platforms?

If someone is strong on both LinkedIn and X, list them in **both** sections — their craft differs per platform. Treat each listing as a separate inspiration source.

## How `jab-hook` uses your list

When drafting a `promo` or `educational` post:

1. The skill determines the target platform(s) of the draft (X, LinkedIn, both)
2. Picks 1–2 accounts from the matching section(s) whose audience overlaps the property being promoted
3. Pulls recent posts via `social-fetch` (uses `agent-browser` for LinkedIn if no paid keys; ScrapeCreators for full X threads when `SCRAPECREATORS_API_KEY` is set)
4. Extracts: hook openers, structural patterns, CTA styles, post length, line-break rhythm
5. Chooses one pattern that fits the property + content type + platform conventions
6. Applies the pattern to YOUR voice — don't mimic their voice, only the structure

Extracted patterns accumulate in `${MAKERSKILLS_CONFIG:-$HOME/.config/makerskills}/jab-hook/patterns.local.md`, tagged with `platform: <linkedin | x | …>` so the skill knows which patterns transfer where.

## Notes

- LinkedIn often blocks unauthenticated scraping. If `agent-browser` walls, fall back to: pasting examples, pulling from their public newsletters, or scraping their X accounts.
- X scraping needs `$SCRAPECREATORS_API_KEY` for full threads. Free strategy returns preview only.
- Never copy phrasing — only structure, format, hook archetype.
- Inspiration is a starting point. Your voice rules in `voice.md` (+ `voice.local.md` overlay) always override format choices.
- Some patterns transfer across platforms (story-open hooks); others don't (LinkedIn carousels ≠ X threads).
