# Per-platform strategies

Each platform has 2–5 strategies tried in order. Free first, paid as fallback (and only if env keys are set).

---

## bluesky

**Reliability: high.** Public API, free.

### Strategy 1 — Public AppView API (DEFAULT)

URL: `https://bsky.app/profile/<handle>/post/<rkey>`

```bash
# Resolve handle → DID
DID=$(curl -s "https://public.api.bsky.app/xrpc/com.atproto.identity.resolveHandle?handle=<handle>" | jq -r .did)

# Build AT-URI and fetch the post + thread
URI="at://${DID}/app.bsky.feed.post/<rkey>"
curl -s "https://public.api.bsky.app/xrpc/app.bsky.feed.getPostThread?uri=${URI}" | jq .
```

Returns the post + immediate parent + first-level replies in one call. Perfect for `--with-replies`.

---

## mastodon

**Reliability: high.** Public API, free, no auth.

### Strategy 1 — Status endpoint

URL pattern: `https://<instance>/@<user>/<status-id>`

```bash
# Single status
curl -s -H "Accept: application/json" "https://<instance>/api/v1/statuses/<status-id>"

# With replies
curl -s -H "Accept: application/json" "https://<instance>/api/v1/statuses/<status-id>/context"
```

Note: instance and ID parsed from URL. Web URL `https://hachyderm.io/@user/123456` → API `https://hachyderm.io/api/v1/statuses/123456`.

---

## hn

**Reliability: high.** Free public Algolia API.

### Strategy 1 — Algolia items API

URL pattern: `https://news.ycombinator.com/item?id=<id>`

```bash
curl -s "https://hn.algolia.com/api/v1/items/<id>" | jq .
```

Returns the item + full nested comment tree. Comments are recursive — flatten or limit depth per `--with-replies` flag.

---

## reddit

**Reliability: medium.** The `.json` path is dead; the keyless shreddit partials work.

### Strategy 1 — shreddit `/svc` comment partial (CURRENT)

URL pattern: `https://www.reddit.com/r/<sub>/comments/<id>/<slug>/`

```bash
curl -s -A "$BROWSER_UA" "https://www.reddit.com/svc/shreddit/comments/r/<sub>/t3_<id>"
```

Serves HTTP 200 HTML with no API key. Comments are `<shreddit-comment>` elements whose start-tag attributes carry `score` / `author` / `created` / `permalink`; each body lives in a `<div id="{thingId}-post-rtjson-content">` block. `total-comments` on the page gives the real comment count.

For post-level upvote score (which the comments partial does *not* carry), use the listing partial:
`https://www.reddit.com/svc/shreddit/community-more-posts/top/?name=<sub>&t=day` — `<shreddit-post>` elements carry `score`, `comment-count`, `post-title`, `permalink`, `created-timestamp`.

### Strategy 2 — Append `.json` to URL (DEPRECATED — usually 403)

```bash
curl -s -A "Mozilla/5.0 social-fetch/0.1" "<url>.json" | jq .
```

**Verified 403 on 2026-08-28** for unauthenticated clients regardless of User-Agent — Reddit's shreddit anti-bot now gates it. A residential IP occasionally still gets a 200, so it's worth one cheap try, but never depend on it. Returns `[post, comments_tree]` when it does work.

**Rate limits**: Reddit 429s an unpaced burst and keeps 429ing *every* endpoint for minutes, then recovers on its own. Space calls ≥2s; treat a 429 as a failed strategy, not something to retry.

### Strategy 3 — Wayback Machine fallback

If rate-limited or post deleted:

```bash
curl -s "https://archive.org/wayback/available?url=<encoded-url>" | jq -r '.archived_snapshots.closest.url'
```

Returns Wayback URL — re-fetch from there.

---

## x (twitter)

**Reliability: good with your own session cookies, low without.** X blocks anonymous scraping aggressively, but `AUTH_TOKEN` + `CT0` unlock a real free path — see Strategy 1.

### Strategy 1 — bird-search with session cookies (FREE, preferred)

`last30days` vendors a Node client for X's GraphQL API (`@steipete/bird` v0.8.0, MIT):

```
~/.claude/plugins/cache/last30days-skill/last30days/<ver>/skills/last30days/scripts/lib/vendor/bird-search/bird-search.mjs
```

```bash
AUTH_TOKEN=… CT0=… node "$BIRD" "from:<handle> since:2026-08-25" --count 15 --json
```

Real search and per-handle timelines, free. Credentials are the `auth_token` and `ct0` cookies from your own logged-in x.com session (DevTools → Application → Cookies). Resolve env → macOS Keychain; **treat them as passwords** — never a plaintext dotfile, never committed. They expire with the session, so a sudden auth failure means "re-grab the cookies," not "X is broken." Glob the newest vendored version at runtime rather than hardcoding the path.

Without credentials the tool fails explicitly rather than oddly:

```json
{"error":"Missing auth_token - provide via --auth-token, AUTH_TOKEN env var, ...","items":[]}
```

### Strategy 2 — agent-browser preview (LIMITED, fallback)

For tweet preview only — body text and basic author info. No engagement counts, no replies, no thread.

```bash
agent-browser open "<url>"
sleep 3
agent-browser snapshot 2>&1 | head -50
# Parse the StaticText for tweet body
```

Often hits "Sign up to see" modal — dismiss with first interactive button if visible.

### Nitter mirrors — EFFECTIVELY DEAD, don't try

Instances are down or rate-limited essentially always as of 2026-08. Removed as a strategy; noted so nobody re-adds it.

### Strategy 3 — Wayback Machine

```bash
curl -s "https://archive.org/wayback/available?url=https://twitter.com/<user>/status/<id>" | jq -r '.archived_snapshots.closest.url'
```

Older tweets often cached; recent ones rarely.

### Strategy 4 — ScrapeCreators API (PAID, recommended for X)

Requires `$SCRAPECREATORS_API_KEY`. If unset, skip and surface a one-time setup prompt.

```bash
curl -s "https://api.scrapecreators.com/v1/twitter/tweet?url=<encoded-url>" \
  -H "x-api-key: $SCRAPECREATORS_API_KEY"
```

Endpoint exact path may differ — verify in ScrapeCreators docs on first use.

### Strategy 5 — Apify scraper (PAID)

Requires `$APIFY_API_TOKEN`. Use the `apify/twitter-scraper` actor or a community equivalent.

```bash
curl -X POST "https://api.apify.com/v2/acts/<actor-id>/run-sync-get-dataset-items?token=$APIFY_API_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"tweetUrls": ["<url>"], "maxItems": 1}'
```

---

## linkedin

**Reliability: medium.** agent-browser works for some content.

### Strategy 1 — agent-browser + dismiss modal

```bash
agent-browser open "<url>"
sleep 3
# Detect signup modal and dismiss
agent-browser snapshot -i 2>&1 | head -20
# If first interactive element is "Dismiss" button:
agent-browser click @e1
sleep 2
agent-browser snapshot 2>&1 | head -100
```

Works well for `linkedin.com/in/<handle>` profile pages (recent activity feed visible).
Specific post URLs (`linkedin.com/posts/...`) usually require login — fall through.

### Strategy 2 — ScrapeCreators API (PAID)

```bash
curl -s "https://api.scrapecreators.com/v1/linkedin/post?url=<encoded-url>" \
  -H "x-api-key: $SCRAPECREATORS_API_KEY"
```

### Strategy 3 — Apify (PAID)

Use `apify/linkedin-profile-scraper` or `apify/linkedin-post-scraper` actor.

---

## instagram

**Reliability: low without paid.** Heavy anti-bot.

### Strategy 1 — Open Graph fallback (LIMITED — just description/image)

```bash
curl -s -A "Mozilla/5.0" "<url>" | grep -E 'og:(title|description|image)'
```

Returns metadata only. No engagement counts. Often blocked.

### Strategy 2 — ScrapeCreators API (PAID, recommended for IG)

```bash
curl -s "https://api.scrapecreators.com/v1/instagram/post?url=<encoded-url>" \
  -H "x-api-key: $SCRAPECREATORS_API_KEY"
```

### Strategy 3 — Apify (PAID)

Use `apify/instagram-scraper` actor.

---

## tiktok

**Reliability: low without paid.**

### Strategy 1 — Open Graph fallback (LIMITED)

```bash
curl -s -A "Mozilla/5.0" "<url>" | grep -E 'og:(title|description|video)'
```

### Strategy 2 — ScrapeCreators API (PAID)

```bash
curl -s "https://api.scrapecreators.com/v1/tiktok/video?url=<encoded-url>" \
  -H "x-api-key: $SCRAPECREATORS_API_KEY"
```

### Strategy 3 — Apify (PAID)

Use `apify/tiktok-scraper` actor.

---

## threads

**Reliability: low without paid.** Meta's anti-bot, like Instagram.

### Strategy 1 — Open Graph fallback (LIMITED)

```bash
curl -s -A "Mozilla/5.0" "<url>" | grep -E 'og:(title|description)'
```

### Strategy 2 — ScrapeCreators API (PAID, if supported)

Check ScrapeCreators docs for Threads endpoint — coverage varies.

### Strategy 3 — Apify (PAID)

Use a Threads scraper actor (search Apify marketplace).

---

## Strategy chain summary

| Platform | Free strategies | Paid fallback |
|---|---|---|
| bluesky | Direct API | — |
| mastodon | Direct API | — |
| hn | Algolia API | — |
| reddit | shreddit `/svc` partials → `.json` (usually 403) → Wayback | — |
| x | bird-search (`AUTH_TOKEN`+`CT0`) → agent-browser → Wayback | ScrapeCreators → Apify |
| linkedin | agent-browser (modal dismiss) | ScrapeCreators → Apify |
| instagram | OG tags | ScrapeCreators → Apify |
| tiktok | OG tags | ScrapeCreators → Apify |
| threads | OG tags | ScrapeCreators → Apify |
