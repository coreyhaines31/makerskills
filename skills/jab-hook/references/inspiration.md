# Inspiration accounts

**Your personal list lives at `${MAKERSKILLS_CONFIG:-$HOME/.config/makerskills}/jab-hook/inspiration.local.md`** — not in this repo (gitignored, on disk only). The list of operators you're learning from is your taste — keep it private.

See `inspiration.example.md` in this directory for the schema + setup instructions.

## How the skill loads it

1. Read `${MAKERSKILLS_CONFIG:-$HOME/.config/makerskills}/jab-hook/inspiration.local.md` for the personal account list
2. If missing, skip the inspiration scan (skill still works, just without external pattern pull)

## Per-platform organization (load-bearing)

The local file is organized by platform — `## LinkedIn`, `## X (Twitter)`, `## Instagram`, etc. — because **what works on one platform usually doesn't work on another**:

- **LinkedIn**: long-form professional, carousel/document posts, framework breakdowns, narrative + takeaway
- **X**: short (≤280 chars), thread mechanics, reply-as-content, punchier + snarkier
- **Instagram**: visual-first, reel-driven, lifestyle / behind-the-scenes
- **TikTok**: vertical video, hook-heavy, trend-aware short-form
- **YouTube**: long-form (more relevant to `youtubeskills` than `jab-hook`)

When the skill scans inspiration, it pulls from the section matching the TARGET PLATFORM of the draft. Cross-posted drafts (e.g., X + LinkedIn) scan both sections.

## Same person, two platforms

When an operator appears on multiple platforms with strong presence on each, list them in both relevant sections — their craft per platform is usually different. Treat each listing as a separate inspiration source for that platform.

## Pattern library — also local + platform-tagged

When the skill extracts hook patterns / structural patterns from inspiration-account posts, it writes them to:

`${MAKERSKILLS_CONFIG:-$HOME/.config/makerskills}/jab-hook/patterns.local.md`

Each pattern is tagged with the source platform (e.g., `platform: linkedin`) so future scans know which patterns transfer where. Some patterns are platform-portable (story-open hooks); others are platform-specific (LinkedIn carousel structure, X thread mechanics).

This file is gitignored. The pattern library grows with use and stays your private playbook.

## Methodology (this stays public — recipe, not data)

When drafting a `promo` or `educational` post:

1. **Determine the target platform(s)** — X, LinkedIn, both, etc.
2. **Pick 1–2 accounts from the matching platform section(s)** whose audience overlaps the property being promoted
3. **Pull their recent posts via `social-fetch`**
   - LinkedIn: `agent-browser` with modal dismissal (no API key needed) or ScrapeCreators if `SCRAPECREATORS_API_KEY` set for full post data
   - X: ScrapeCreators recommended; free tier returns preview only
4. **Extract**: hook openers, structural patterns (numbered list / contrarian-take / story-open / thread mechanics), CTA styles, post length, line-break rhythm
5. **Choose ONE pattern** that fits the property + content type + platform conventions
6. **Apply the pattern to YOUR voice** — don't mimic their voice, only the structure

## Notes

- LinkedIn often blocks unauthenticated scraping. If `agent-browser` walls, fall back to: pasting examples, pulling from their public newsletters, or scraping their X accounts.
- Never copy phrasing — only structure, format, hook archetype.
- Inspiration is a starting point. Your voice rules in `voice.md` (+ `voice.local.md` overlay) always override format choices.
- Some patterns transfer across platforms (story-open hooks); others don't (LinkedIn carousels won't work on X). The `patterns.local.md` platform tag helps the skill respect the boundary.
