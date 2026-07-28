# Xquik Apify Actor Routes

Use these Actors as paid X fallbacks. Preserve free strategies,
ScrapeCreators, and any configured community Actor.

## Actors

| Actor | Store | Stable Actor ID | API Actor ID |
|---|---|---|---|
| X Tweet Scraper | [Actor listing](https://apify.com/xquik/x-tweet-scraper) | `wAusCMrm284Voaw86` | `xquik~x-tweet-scraper` |
| X Follower Scraper | [Actor listing](https://apify.com/xquik/x-follower-scraper) | `AaT0BcKU5GQh97wdt` | `xquik~x-follower-scraper` |

Store slugs:

- `xquik/x-tweet-scraper`
- `xquik/x-follower-scraper`

## Tweet Routes

Supported modes:

- `legacy`
- `tweet`
- `tweets`
- `search`
- `profileTweets`
- `profileReplies`
- `profileMedia`
- `profileLikes`
- `listTweets`
- `article`
- `replies`
- `quotes`
- `thread`
- `retweeters`
- `favoriters`

For the base `social-fetch` URL workflow, use `mode: "tweet"` with `tweetUrls`.
Use `replies` or `thread` only when the matching flag requests that depth.

```json
{
  "mode": "tweet",
  "tweetUrls": ["https://x.com/example/status/1234567890"],
  "maxItems": 1,
  "outputVariant": "rich",
  "fieldStyle": "camelCase",
  "outputPreset": "nested"
}
```

Use `maxItems` as the whole-run cap. Use `maxItemsPerTarget` for supported
multi-target routes. Output variants are `legacy`, `rich`, and `raw`. Field
styles are `legacy`, `camelCase`, and `snake_case`. Output presets are `nested`
and `flat`.

## Audience Route

Supported relations:

- `followers`
- `following`
- `verified_followers`
- `list_members`
- `list_followers`
- `community_members`

The `--audience` enrichment is opt-in. Resolve the post author's public handle,
then send only the requested relation.

```json
{
  "twitterHandles": ["example"],
  "relations": ["verified_followers"],
  "maxItems": 20,
  "maxItemsPerTarget": 20,
  "outputMode": "compact",
  "includeTargetMetadata": true,
  "dedupeMode": "none"
}
```

Follower output modes are `compact`, `full`, and `raw`. Use
`dedupeMode: "merge"` or `overlapMode: true` only for an explicitly requested
cross-target comparison.

## Paid-Run Gate

Before execution:

1. Check the cache and free strategies.
2. Inspect the live input schema and current Store pricing.
3. Validate each target and the selected mode or relation.
4. Set `maxItems`, per-target limits, and `MAX_TOTAL_CHARGE_USD`.
5. Show the scope and estimated spend. Obtain explicit approval.
6. Send `APIFY_API_TOKEN` only through the bearer authorization header.
7. Separate rows with `resultType: "diagnostic"` from usable records.

Do not treat diagnostic-only output as a successful fetch. Do not infer
protected or sensitive traits from public relationship data.

Xquik is an independent third-party service. Not affiliated with X Corp.
"Twitter" and "X" are trademarks of X Corp.
