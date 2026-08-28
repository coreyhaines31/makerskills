# sources.yaml — schema

Lives at `${MAKERSKILLS_CONFIG:-$HOME/.config/makerskills}/radar/sources.yaml`. Private, gitignored, never in the repo.

## Shape

```yaml
defaults:
  cadence: daily                  # daily | weekly | hourly
  lookback_days: 2                # window to consider "new" on a normal run
  first_run_lookback_days: 3      # window for a source with no state file yet
  max_items_per_source: 15
  auto_capture_at: 5              # score >= this → fetched + written to raw/ automatically
  list_at: 3                      # score >= this → listed in the digest as promotable
                                  # below list_at → collapsed into the skipped block

sources:
  - id: yt-greg-isenberg          # kebab-case, unique, stable — state files key off this
    type: youtube
    target: "@GregIsenberg"
    channel_id: UCG2fPDWk6C1RE0FbTexrJ2A   # resolved once at add-time, cached here
    focus: >
      Business ideas with a real wedge, AI agent products, indie SaaS
      teardowns. Not: generic motivation, guest interviews about fundraising.
    tags: [business, ai]
    enabled: true
```

## Fields

### `defaults`

Every key can be overridden per source. A source that needs a different `auto_capture_at` than the rest is usually a source with a `focus` that needs rewriting instead — check that first.

### Per source

| Field | Required | Notes |
|---|---|---|
| `id` | ✅ | Kebab-case, unique. Convention: `<type-prefix>-<slug>` (`yt-`, `rss-`, `rd-`, `hn-`, `x-`, `li-`, `kw-`). Changing an `id` orphans its state file and re-surfaces old items — rename deliberately. |
| `type` | ✅ | `youtube` \| `rss` \| `reddit` \| `hn` \| `bluesky` \| `mastodon` \| `x` \| `linkedin` \| `keyword` |
| `target` | ✅ | The human-readable handle/URL/query. What you'd type. |
| `focus` | ✅ | Free prose: what you want from this source **and what you don't**. The negative half does most of the filtering work. |
| `enabled` | | Default `true`. `pause` sets this to `false` rather than deleting — keeps the state file, so resuming doesn't re-surface a backlog. |
| `tags` | | Free labels. Used to group the digest and to run a subset (`/radar run --tag ai`). |
| `cadence` | | Overrides `defaults.cadence`. |
| `notes` | | Why this source is on the list. Useful at prune time. |

### Type-specific fields

| Type | Extra fields |
|---|---|
| `youtube` | `channel_id` (cached `UC…`), `shorts: false` to skip Shorts, `min_duration_seconds` |
| `rss` | `feed_url` (resolved at add-time), `full_text: true` if the feed carries whole articles (skips the WebFetch on capture) |
| `reddit` | `subreddit`, `sort: top\|new\|hot` (**default `top`**), `t: day\|week` (with `top`), `min_score` (upvotes floor — the cheapest possible pre-filter, and it only works on `top`/`hot`; see fetchers.md) |
| `hn` | `query`, `min_points` (default 50), `story_only: true` |
| `x` | `handle`, `include_replies: false`, `include_reposts: false` |
| `bluesky` | `handle`, `did` (cached at add-time), `min_likes`, `include_replies: false` |
| `mastodon` | `handle` (`@user@instance`), `instance`, `account_id` (both cached at add-time) |
| `linkedin` | `profile_url`, `company: true` for company pages |
| `keyword` | `query`, `engines: [web, hn, reddit, youtube]`, `recency_days` |

## Writing a `focus` that works

This field is the entire filter. Three rules:

1. **Name concrete things, not categories.** "Server-side attribution, CAPI, consent-mode workarounds" filters. "Marketing tech" does not.
2. **Include the exclusions.** Most sources are 80% something you don't want; say what it is. "Not: hiring posts, conference recaps, anything gated behind a webinar signup."
3. **Tie it to an open question where you can.** "Anything that changes how TracerKit should handle iOS 17 link tracking" gives scoring a real bar to measure against, and it makes a 5 mean something.

## Picking the type when an account is on several platforms

Several people post the same thing to X, Bluesky, and Mastodon. Radar's reliability differs enormously between them (see fetchers.md → "Reliability at a glance"), so when there's a choice: **bluesky or mastodon over x**, always. Same content, keyless access, real engagement counts, and no source that quietly goes degraded for a week.

Only reach for an `x` source when the account posts *there and nowhere else* — and even then, set up the `AUTH_TOKEN` + `CT0` cookies first.

Rewrite the `focus` when a source's capture rate goes wrong in either direction — too many 5s means it's too loose, a month of nothing means it's too tight or the source is dead weight.

## State files

`state/<source-id>.json`:

```json
{
  "last_run": "2026-08-28T07:00:12Z",
  "last_status": "ok",
  "error": null,
  "seen": ["yt:dQw4w9WgXcQ", "rss:https://example.com/post-slug"],
  "stats": { "items_7d": 12, "captured_30d": 3 }
}
```

- `seen` is capped at the most recent 300 IDs, newest last.
- ID format is `<type>:<native-id>` — video ID, GUID or URL, Reddit `t3_…`, HN object ID, tweet ID, Bluesky rkey, Mastodon status ID. Feeds without a stable ID fall back to a SHA of `url + title`.
- Deleting a state file is the supported way to re-scan a source from scratch. It will re-surface items — that's the point.

## Run records

`runs/<YYYY-MM-DD>.json` backs `promote`, so it holds everything needed to fetch an item without re-polling:

```json
{
  "date": "2026-08-28",
  "runs": [{ "started": "2026-08-28T07:00:02Z", "sources": 9, "duration_s": 41 }],
  "items": [
    {
      "n": 4,
      "source_id": "yt-greg-isenberg",
      "type": "youtube",
      "native_id": "dQw4w9WgXcQ",
      "title": "…",
      "url": "https://…",
      "published": "2026-08-28T02:11:00Z",
      "score": 4,
      "reason": "Names the exact attribution problem TracerKit solves",
      "summary": "…",
      "captured": false,
      "raw_path": null
    }
  ],
  "degraded": [{ "source_id": "x-levelsio", "error": "no fetch strategy available" }]
}
```

`n` is stable for the day and shared with the digest — a second run continues the numbering rather than renumbering.
