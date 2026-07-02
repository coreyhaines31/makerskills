---
name: social-fetch
description: When you or another skill needs to fetch the content of a social media post by URL — tweet, X thread, LinkedIn post, Instagram post, TikTok video, Bluesky post, Reddit thread, Mastodon status, Threads post, Hacker News thread. Returns normalized structured data (author, posted_at, text, engagement counts, media URLs, replies if requested) regardless of platform. Tries strategies in order: direct API (Bluesky, Mastodon, HN, Reddit), agent-browser with modal dismissal (LinkedIn, X preview), Wayback Machine (older posts), paid APIs (ScrapeCreators / Apify — only if env keys present). Triggers on "/social-fetch <url>," "fetch this tweet," "fetch this post," "what does this LinkedIn say," "read this thread," "pull this post." Used by deep-research (citing specific posts), jab-hook (inspiration account analysis), business-brainstorm (competitor / operator commentary).
metadata:
  version: 0.1.1
---

# /social-fetch — Pull any social post by URL

Normalized fetcher for social posts across platforms. Detects platform from URL, tries strategies in order, returns the same JSON shape regardless of source.

## Step 1 — Detect platform

| URL pattern | Platform |
|---|---|
| `x.com/<user>/status/<id>` or `twitter.com/<user>/status/<id>` | **x** (Twitter) |
| `linkedin.com/posts/<slug>` or `linkedin.com/feed/update/urn:li:activity:<id>` | **linkedin** |
| `linkedin.com/in/<handle>` (profile, recent activity) | **linkedin-profile** |
| `instagram.com/p/<id>` or `instagram.com/reel/<id>` | **instagram** |
| `tiktok.com/@<user>/video/<id>` | **tiktok** |
| `bsky.app/profile/<handle>/post/<rkey>` | **bluesky** |
| `reddit.com/r/<sub>/comments/<id>/...` | **reddit** |
| `<mastodon-instance>/@<user>/<id>` (e.g. mastodon.social, hachyderm.io) | **mastodon** |
| `threads.net/@<user>/post/<id>` | **threads** |
| `news.ycombinator.com/item?id=<id>` | **hn** |
| `youtube.com/watch?v=<id>` or `youtu.be/<id>` | → defer to `watch-video` |

If the URL doesn't match any pattern, ask the user what platform it is.

## Step 2 — Pick strategy chain

Read `references/strategies.md` for the per-platform strategy chain. Each platform has 2–5 strategies tried in order.

Key principles:
- **Free strategies first** (direct APIs, agent-browser)
- **Paid only as fallback** (ScrapeCreators / Apify) — and only if the env key is set
- **Bluesky / Mastodon / HN / Reddit are free + reliable** (public APIs)
- **X / LinkedIn / Instagram / TikTok / Threads** need paid or scraping fallback for full data

## Step 3 — Execute strategy

For each strategy in the chain:
1. Try it
2. If success: parse → normalize → return
3. If failure (404, 402, auth wall, empty response): note the failure and try the next strategy

After exhausting the chain, return a clear error: which strategies were tried, why each failed, and what's needed to unlock (e.g., "Add `$SCRAPECREATORS_API_KEY` for X — see `references/auth-keys.md`").

## Step 4 — Normalize output

Return this shape regardless of platform (see `references/output-schema.md` for the full spec + platform-specific examples):

```json
{
  "platform": "x",
  "url": "https://x.com/example/status/1234567890",
  "fetched_at": "2026-06-17T14:35:00Z",
  "raw_source": "scrapecreators",
  "author": {
    "handle": "@example",
    "name": "the user Ganim",
    "verified": true
  },
  "posted_at": "2026-06-17T16:53:00Z",
  "text": "The 80/20 of a useful AI second brain: ...",
  "media": [],
  "engagement": {
    "likes": 51,
    "reposts": 13,
    "replies": 9,
    "bookmarks": 7,
    "views": 32700
  },
  "is_thread": true,
  "thread": [],
  "replies": []
}
```

Fields with no equivalent on a platform (e.g., `bookmarks` on Mastodon) get `null`, not `0`. Missing data is different from zero data.

## Step 5 — Optional enrichments

Based on flags / asks:

| Flag | Behavior |
|---|---|
| `--with-replies` | Fetch top-level replies (1 hop). Costs extra API quota. |
| `--thread` | If the post is part of a thread by the same author, fetch the whole thread. |
| `--raw` | Include the raw API/scrape response in the output (for debugging) |
| `--media` | Download media files (images/videos) to `~/Documents/social-fetches/<platform>-<id>/` |

Default: just the post itself, no replies, no media download (just URLs).

## Step 6 — Cache (optional)

If `~/Documents/social-fetches/_cache/` exists, cache successful fetches there by `{platform}-{id}.json` for 24h. Saves API quota when the same post is referenced repeatedly across skills.

Skip cache if `--no-cache` flag is set or for `--with-replies` / `--thread` (likely-stale).

## Composes with

- `deep-research` — cite specific posts in research briefs. When research surfaces a relevant tweet/post URL, fetch and include in the brief.
- `jab-hook` — pull recent posts from inspiration accounts for deeper format analysis (currently uses agent-browser inline; should call this skill instead).
- `business-brainstorm` — pull competitor / operator commentary as evidence during scoring.
- `second-brain` — capture a post into `raw/` with the `tweet-` / `bookmark-` prefix; the structured output makes for cleaner raw files than a screenshot or copy-paste.
- `watch-video` — for YouTube URLs (or any video — Loom, Vimeo, Riverside, MP4), route there instead.

## Known limits

- **X**: free strategies return tweet preview only (text, author, basic engagement). Full thread + replies need `$SCRAPECREATORS_API_KEY` or `$APIFY_API_TOKEN`.
- **LinkedIn**: agent-browser works for profile recent-activity (after dismissing the modal). Specific post URLs (`linkedin.com/posts/...`) often need paid fallback.
- **Instagram / TikTok / Threads**: heavy anti-bot. Paid fallback strongly recommended.
- **Bluesky / Mastodon / HN / Reddit**: free + reliable.
- **Private / deleted posts**: nothing helps. Try Wayback Machine for deleted content.

If a platform consistently fails on free strategies and the user uses it often, prompt to set up the paid key (see `references/auth-keys.md`).

## Notes on quality

- **Strategy chain, not single-source.** Every platform has a fallback ladder (native oEmbed → agent-browser → SCS API → Apify). If one step fails, degrade gracefully to the next. Never fail hard on the first attempt.
- **Structured output over screenshots.** Downstream skills (jab-hook, deep-research, second-brain) need JSON with author + text + engagement fields, not an image. Even when the underlying strategy is a screenshot, extract text before returning.
- **Cache aggressively, invalidate honestly.** 24h TTL on `~/Documents/social-fetches/_cache/` prevents API burn when the same post is referenced across multiple skills in a session. `--with-replies` / `--thread` skip cache because replies age fast.
- **Respect paid-key economics.** ScrapeCreators / Apify calls cost real money. Prompt before hitting paid strategies if the user hasn't confirmed they want depth. Free strategies first, always.
- **Media download is opt-in.** Default is post text only; `--media` downloads images/videos. Silent media downloads eat disk quickly.
- **Private / deleted content is a hard stop.** No strategy chain rescues private accounts or deleted posts. Suggest Wayback Machine for deleted content and stop.
- **Rate-limits are per-platform.** X free strategies hit rate limits fast; LinkedIn agent-browser burns session fingerprints. Space out calls in loops or the workflow degrades to worse-than-manual.
