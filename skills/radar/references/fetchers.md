# Fetchers — one recipe per source type

Every command here was verified live. Where a recipe has a gotcha, the gotcha is the reason the recipe looks the way it does — don't "simplify" it back to the obvious version.

## Ground rules

- **Always send a realistic browser User-Agent.** Several of these endpoints return 200 to Chrome and 403/404 to `curl/8.x`. Use:
  `-A "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Safari/537.36"`
- **Parse XML with `/usr/bin/python3`, not `python3`.** On a Mac with Homebrew Python 3.14 installed, `python3` resolves to a build whose `pyexpat` fails to load (`Symbol not found: _XML_SetAllocTrackerActivationThreshold`), which breaks `xml.etree` entirely. System Python parses fine. `xmllint` (ships with macOS) is the other safe option.
- **Pace requests.** Reddit in particular will 429 an unpaced burst and keep 429ing for minutes. Sleep ~2s between requests to the same host, and treat a 429 as `degraded` for the run rather than retrying hard.
- **Timeout everything**: `--max-time 20`. An unattended job that hangs on one dead host is a job that silently never finishes.
- **Never fetch full content during a poll.** Polls read metadata; full fetch happens at capture time only.
- **Reuse `social-fetch`'s cache.** If `~/Documents/social-fetches/_cache/` exists, check it before any social fetch and write successful ones back (24h TTL, keyed `{platform}-{id}.json`). Radar and `social-fetch` hit the same posts constantly; a shared cache is free quota.
- **Wayback is the universal last resort.** For anything deleted, rate-limited, or auth-walled:
  `curl -s "https://archive.org/wayback/available?url=<encoded>" | jq -r '.archived_snapshots.closest.url'`

## Credentials

Radar's free tiers cover youtube / rss / hn / bluesky / mastodon outright. Reddit and X get meaningfully better with credentials, and X is barely usable without them.

Resolution order for every key: **env var → macOS Keychain → absent (degrade)**.

```bash
# Keychain read, matching the convention last30days already uses
security find-generic-password -s "last30days-AUTH_TOKEN" -w 2>/dev/null
```

| Key | Unlocks | Cost |
|---|---|---|
| `AUTH_TOKEN` + `CT0` | **X, properly** — real search and per-handle timelines | Free (your own x.com session cookies) |
| `BSKY_HANDLE` + `BSKY_APP_PASSWORD` | Bluesky beyond public reads (rarely needed) | Free app password |
| `SCRAPECREATORS_API_KEY` | X / LinkedIn / IG / TikTok, reliably | Paid |
| `APIFY_API_TOKEN` | Same, alternate vendor | Paid |

Note the env var is `APIFY_API_TOKEN` — matching `social-fetch` and `last30days`. Don't invent a second name.

**Unattended runs**: a launchd job has no shell profile, so env vars from `~/.zshenv` are absent — see `scheduling.md`. Keychain reads from a launchd agent work but may need a one-time "Always Allow" on the item's ACL. Test with `launchctl start` before assuming the morning run has credentials. `doctor` reports which keys resolved and from where.

---

## youtube

**Poll — per-channel RSS. No API key, no quota, ~15 most recent videos.**

```bash
curl -s --max-time 20 "https://www.youtube.com/feeds/videos.xml?channel_id=UCPjNBjflYl0-HQtUvOx0Ibw"
```

Parse (Atom + the `yt:` and `media:` namespaces):

```bash
/usr/bin/python3 - "$FEED" <<'PY'
import sys, xml.etree.ElementTree as ET
ns = {'a':'http://www.w3.org/2005/Atom',
      'yt':'http://www.youtube.com/xml/schemas/2015',
      'm':'http://search.yahoo.com/mrss/'}
for e in ET.parse(sys.argv[1]).getroot().findall('a:entry', ns):
    vid  = e.find('yt:videoId', ns).text
    grp  = e.find('m:group', ns)
    print('\t'.join([
        vid,
        e.find('a:published', ns).text,
        e.find('a:title', ns).text,
        f'https://www.youtube.com/watch?v={vid}',
        (grp.find('m:description', ns).text or '')[:400].replace('\n', ' ') if grp is not None else '',
    ]))
PY
```

The `media:description` is the video description — that plus the title is what scoring runs on. Item ID: `yt:<videoId>`.

**Gotchas**

- The feed carries **no duration**, so `shorts: false` and `min_duration_seconds` can't be applied from the feed alone. Cheap heuristic first (`/shorts/` in a title, "#shorts" tag); only call `yt-dlp --print duration --skip-download <url>` when a source actually sets those fields, and only for the handful of new items.
- The feed only holds ~15 videos. A channel that posts more than that between runs will lose the overflow — for high-volume channels set `cadence: daily` and don't let the source sit paused for weeks.

**Full fetch (capture)** — `watch-video` in transcript mode. It handles the yt-dlp + MLX-Whisper path and platform-provided subs. Fall back to `yt-dlp --write-auto-sub --skip-download` if that skill isn't loaded.

---

## rss

**Poll**

```bash
curl -sL --max-time 20 -A "$UA" "$FEED_URL"
```

Handle both shapes with one parser — RSS 2.0 (`channel/item`, `pubDate`, `guid`) and Atom (`entry`, `published`/`updated`, `id`). Item ID: the `guid`/`id` if present, else the link URL, else `sha1(link + title)`.

**Read the body from `content` OR `summary`, in that order.** Plenty of Atom feeds put the whole post in `<summary type="html">` and omit `<content>` entirely (simonwillison.net does). A parser that only looks at `content` scores every item from its title alone, which quietly makes every score a 3:

```python
body = next((n.text for t in ('content', 'summary')
             if (n := entry.find(f'a:{t}', NS)) is not None and n.text), '')
text = re.sub(r'\s+', ' ', re.sub('<[^>]+>', '', body)).strip()   # feeds carry HTML
```

Same for RSS 2.0: prefer `content:encoded`, fall back to `description`.

**Feed discovery** (when the user gives a site URL, not a feed URL), in order:

1. `<link rel="alternate" type="application/rss+xml">` or `atom+xml` in the homepage `<head>`:
   `curl -sL -A "$UA" "$SITE" | grep -oiE '<link[^>]+type="application/(rss|atom)\+xml"[^>]*>'`
2. Common paths: `/feed`, `/rss`, `/feed.xml`, `/rss.xml`, `/atom.xml`, `/index.xml`, `/feed/atom`.
3. Platform patterns: Substack → `<domain>/feed`; Ghost → `/rss/`; WordPress → `/feed/`; Beehiiv → `/feed`.
4. JS-rendered sites (Next.js marketing sites especially) expose nothing to `curl` — `every.to` returns HTML with no feed link tag. Use `agent-browser` to load the page and read the head, or ask the user for the feed URL directly. Don't guess and store a URL that 200s with HTML — validate that the body actually parses as a feed before writing it to `sources.yaml`.

**Full fetch (capture)** — `WebFetch` the article URL. If the source sets `full_text: true`, the feed's `content:encoded` / `content` already holds the article; skip the fetch.

---

## reddit

**Poll — the shreddit `/svc` listing partial. Keyless, HTTP 200, and it carries real upvote scores.**

```bash
curl -s --max-time 20 -A "$UA" \
  "https://www.reddit.com/svc/shreddit/community-more-posts/top/?name=SaaS&t=day"
```

Each post is a `<shreddit-post>` element whose start-tag attributes carry everything worth having — no JSON API, no key:

```python
import re, html
def attr(tag, name):
    m = re.search(rf'\b{name}="([^"]*)"', tag)
    return html.unescape(m.group(1)) if m else ''

for tag in re.findall(r'<shreddit-post\b[^>]*>', page):
    score   = attr(tag, 'score')            # real upvotes
    ncom    = attr(tag, 'comment-count')
    title   = attr(tag, 'post-title')
    link    = attr(tag, 'permalink')
    created = attr(tag, 'created-timestamp')
```

**Use `top` with `t=day`, not `new`** — verified on r/SaaS the same hour: `new` returned a median score of **1** (posts were minutes old, so scores are noise and `min_score` filters nothing), while `top&t=day` returned a real spread of 277 → 8 across 24 posts. `top&t=day` is both the better signal and the only sort where a `min_score` floor means anything. Reach for `new` only when you genuinely need same-hour latency.

**Gotchas — all verified the hard way**

- **`/r/<sub>/new.json` returns 403** for unauthenticated clients regardless of User-Agent. The old "just add `.json`" trick is dead. (`last30days` reached the same conclusion independently and demoted its `.json` tier for the same reason.)
- **Reddit rate-limits hard and stays angry.** An unpaced burst earns a 429 on *every* Reddit endpoint for minutes afterward, including ones that worked seconds earlier — then recovers on its own. Sleep ≥2s between Reddit calls, one call per source per run, and on 429 mark `degraded` and move on. Never retry-loop.
- **Search endpoints (`/search.rss`, `/r/<sub>/search.rss`) 429 far more readily than listing endpoints.** For keyword coverage of Reddit use a `keyword` source with `site:reddit.com`, which sidesteps Reddit's limits entirely.

**Fallback chain**: shreddit listing → `/r/<sub>/<sort>.rss` (keyless, no scores) → Wayback. The RSS path is the one radar shipped with; it still works and is a fine degraded mode, it just can't pre-filter on score.

Item ID: the permalink-derived `t3_<id>`.

**Full fetch (capture)** — fetch the post URL; for link posts fetch the linked target too, since that's usually the actual content. For comments (frequently the real signal on Reddit), the keyless comment partial:

```bash
curl -s -A "$UA" "https://www.reddit.com/svc/shreddit/comments/r/<sub>/t3_<id>"
```

Comments are `<shreddit-comment>` elements; bodies live in `<div id="{thingId}-post-rtjson-content">`.

---

## hn

**Poll — Algolia's API. Free, no key, generous.**

```bash
curl -s --max-time 20 "https://hn.algolia.com/api/v1/search_by_date?query=%22claude%20code%22&tags=story&advancedSyntax=true&numericFilters=points%3E20,created_at_i%3E$SINCE"
```

```bash
jq -r '.hits[] | [.objectID, .created_at, .points, .title, (.url // ("https://news.ycombinator.com/item?id=" + .objectID))] | @tsv'
```

Notes: `tags=story` excludes comments; `tags=(story,show_hn)` narrows further. `numericFilters` accepts `created_at_i>UNIXTIME` — use it with the lookback window so filtering happens server-side. Item ID: `hn:<objectID>`. Set `min_points` around 50 for a broad query, lower for a niche one.

**Gotcha — the query is fuzzy and you can't fix it with syntax.** A bare `query=claude code` returns stories matching either word: an insurance startup and "Tell HN: Man, AI is killing my brain" both came back on a live test. Quoting the phrase plus `advancedSyntax=true` helps a little. A client-side post-filter (phrase must appear in `title + url + story_text`) helps a little more, but still passes anything that merely *mentions* the phrase — a "Show HN" for an unrelated tool that happens to say it was built with Claude Code.

So: use `advancedSyntax=true` with the phrase quoted, keep a real `min_points` floor, and then **let relevance scoring be the actual filter**. Don't burn time tuning query syntax — HN keyword sources have a low capture rate by nature, and that's the correct outcome, not a misconfiguration.

**Full fetch (capture)** — the story URL, plus `https://hn.algolia.com/api/v1/items/<objectID>` for the comment tree.

---

## x

**No public API, but there is a free authenticated path** — and it changes this source type from "expect degradation" to genuinely usable.

### Strategy 1 — bird-search with your own session cookies (FREE, preferred)

`last30days` vendors a Node client for X's GraphQL API (`@steipete/bird` v0.8.0, MIT). It's already on disk:

```
~/.claude/plugins/cache/last30days-skill/last30days/<ver>/skills/last30days/scripts/lib/vendor/bird-search/bird-search.mjs
```

```bash
AUTH_TOKEN=… CT0=… node "$BIRD" "from:levelsio since:2026-08-25" --count 15 --json
```

`from:<handle> since:<YYYY-MM-DD>` is exactly radar's per-account poll — the lookback window maps straight onto `since:`. Returns JSON items with text, timestamps, and engagement.

**Credentials** are the `auth_token` and `ct0` cookies from your own logged-in x.com session (Chrome DevTools → Application → Cookies → x.com). Resolution order is env → Keychain, per the Credentials section above. Run without them and the tool says so explicitly rather than failing oddly:

```json
{"error":"Missing auth_token - provide via --auth-token, AUTH_TOKEN env var, or login to x.com in Safari/Chrome/Firefox","items":[]}
```

**Handle these cookies like a password** — they are full session credentials for the X account. Keychain, not a plaintext dotfile, and never committed. They expire when the session ends, so `doctor` should treat a sudden X auth failure as "re-grab the cookies," not "X is broken." Resolve the version-pinned vendor path at runtime (glob the newest) rather than hardcoding it — the plugin updates.

### Strategy 2 — `social-fetch`

Owns the fallback ladder (agent-browser with modal dismissal, Wayback for older posts). Prefer calling it over hand-rolling agent-browser, so that knowledge stays in one place.

### Strategy 3 — paid

`$SCRAPECREATORS_API_KEY`, then `$APIFY_API_TOKEN`. Only if set.

### Not a strategy

**Nitter is effectively dead** — instances are down or rate-limited nearly always. `social-fetch`'s strategy list still mentions it; treat it as a historical note, not a path worth trying.

If everything fails: mark `degraded` with the reason and continue. Never retry within the run.

Item ID: `x:<tweet-id>`. Exclude replies and reposts unless the source opts in — that's where the noise lives.

**Full fetch (capture)** — `social-fetch` on the post URL, which pulls the full thread. Prefix `tweet-`.

---

## bluesky

**Reliability: high. Fully keyless, real engagement counts, no anti-bot.** The easiest social source radar has — if an account you follow on X also posts here, prefer this source type.

```bash
DID=$(curl -s "https://public.api.bsky.app/xrpc/com.atproto.identity.resolveHandle?handle=pfrazee.com" | jq -r .did)
curl -s "https://public.api.bsky.app/xrpc/app.bsky.feed.getAuthorFeed?actor=$DID&limit=25&filter=posts_no_replies"
```

```bash
jq -r '.feed[] | [.post.uri, .post.indexedAt, .post.likeCount, .post.repostCount,
                  (.post.record.text | gsub("\n"; " "))] | @tsv'
```

`filter=posts_no_replies` drops replies server-side. Resolve the handle → DID once at add-time and cache it as `did` in `sources.yaml`, exactly like `channel_id` for YouTube. Because `likeCount` comes back on every item, a `min_likes` floor is a cheap and honest pre-filter here.

Item ID: `bsky:<rkey>` from the post URI. **Full fetch (capture)** — `social-fetch` (Strategy 1, public AppView) returns post + parent + first-level replies in one call. Prefix `tweet-`.

---

## mastodon

**Reliability: high. Keyless public API.**

```bash
# handle → account id, once at add-time
curl -s "https://<instance>/api/v1/accounts/lookup?acct=<user>" | jq -r .id
# then poll
curl -s -H "Accept: application/json" \
  "https://<instance>/api/v1/accounts/<id>/statuses?limit=25&exclude_replies=true&exclude_reblogs=true"
```

Instance comes from the handle (`@user@hachyderm.io` → `hachyderm.io`). Cache `instance` + `account_id`. Item ID: `masto:<status-id>`. `content` is HTML — strip tags for the scoring excerpt. Prefix `tweet-`.

---

## linkedin

Same shape as X, and harder. LinkedIn actively blocks unauthenticated fetching and rate-limits logged-in automation.

1. **`social-fetch`** against the profile/company URL — it owns the modal-dismissal logic.
2. **`agent-browser`** with a logged-in persistent profile. The recipe `social-fetch` uses, which is the one that actually works:

   ```bash
   agent-browser open "https://www.linkedin.com/in/<slug>/recent-activity/all/"
   sleep 3
   agent-browser snapshot -i 2>&1 | head -20   # is the first interactive element a Dismiss button?
   agent-browser click @e1                      # dismiss the signup modal
   sleep 2
   agent-browser snapshot 2>&1 | head -100
   ```

   Profile `recent-activity` pages render for logged-out sessions after the modal is dismissed. Individual post URLs (`linkedin.com/posts/…`) usually still demand a login — fall through rather than fighting it.
3. Paid: `$SCRAPECREATORS_API_KEY` → `$APIFY_API_TOKEN`.
4. Otherwise `degraded`.

**Be conservative.** Keep LinkedIn sources few, `cadence: daily` at most, and never parallel-fetch several LinkedIn profiles in one run — that's the pattern that triggers a checkpoint on the account. Fetch them sequentially, spaced.

Item ID: `li:<activity-urn>` (or a SHA of permalink + text when the URN isn't exposed). Capture prefix: `bookmark-`.

---

## keyword

A standing search rather than a named source. Runs across the engines listed in `engines`:

| Engine | How |
|---|---|
| `web` | `WebSearch` with the query + a recency qualifier. Also the right way to cover Reddit — `<query> site:reddit.com` avoids Reddit's search rate limits entirely. |
| `hn` | Algolia recipe above with `created_at_i>` set to the lookback |
| `youtube` | vidIQ MCP `vidiq_youtube_search`, or `yt-dlp "ytsearch20:<query>"` with `--print` for metadata only |
| `reddit` | Only via `web` + `site:reddit.com`. See the Reddit gotchas. |
| `last30days` | `Skill({skill: "last30days", args: "<query>"})` — the heavyweight option. One call sweeps Reddit, X, YouTube, TikTok, HN, Bluesky, GitHub and the web with engagement data and citations. |

**On `last30days` as an engine**: it is far more thorough than radar's own keyword sweep and it already solves the access problems radar works around. It's also slow and broad — the wrong shape for a daily poll across many sources. Use it for at most one or two standing keyword sources where depth genuinely beats latency, and let the cheap engines carry the rest. `deep-research` remains the right escalation for a specific question.

Dedupe across engines by URL before scoring — the same launch shows up on all four. Item ID: `kw:<sha1(url)>`.

Keyword sources are the noisiest type by a wide margin. Start them at `list_at: 4` and never at `auto_capture_at: 4` until one has proven itself for a couple of weeks.

---

## Reliability at a glance

| Type | Free path | Needs credentials | Expect |
|---|---|---|---|
| `youtube` | Channel RSS | — | Rock solid |
| `rss` | Feed fetch | — | Rock solid |
| `hn` | Algolia API | — | Rock solid |
| `bluesky` | Public AppView API | — | Rock solid, with engagement |
| `mastodon` | Public instance API | — | Rock solid |
| `reddit` | shreddit `/svc` listing (scored) → RSS | — | Good, if paced |
| `keyword` | WebSearch + HN | — | Noisy by nature |
| `x` | bird-search | `AUTH_TOKEN` + `CT0` (free) | Good with cookies, poor without |
| `linkedin` | agent-browser | logged-in profile | Intermittent, always |

The practical read: **everything except X and LinkedIn is free and reliable.** X becomes reliable for the price of pasting two cookies. LinkedIn never quite does — keep those sources few.

## Resolving a target (`add` mode)

| Type | Input | Resolution |
|---|---|---|
| youtube | `@handle` or channel URL | `curl -sL -A "$UA" "https://www.youtube.com/@handle" \| grep -o 'channel_id=UC[A-Za-z0-9_-]*' \| head -1` — **the realistic UA is required**; the default curl UA gets a page with no channel ID in it. Cache the result as `channel_id`. |
| rss | site URL | Feed discovery chain above. Validate the body parses as a feed. |
| reddit | `r/name` or URL | Strip to the name; confirm `https://www.reddit.com/r/<name>/new/.rss` returns entries. |
| hn | query string | Nothing to resolve; test-run it and show hit count. |
| x | `@handle` or URL | Normalize to the handle; test-fetch through the chain and report which tier answered. |
| linkedin | profile/company URL | Normalize to the canonical `/in/<slug>` or `/company/<slug>`. |
| bluesky | `handle` or `bsky.app/profile/<handle>` | `resolveHandle` → cache `did`. |
| mastodon | `@user@instance` or profile URL | Split to instance + user, `accounts/lookup` → cache `instance` + `account_id`. |
| keyword | free text | Nothing to resolve; test-run across the configured engines. |

**A source that fails its test-fetch never gets written to `sources.yaml`.** Report what failed and let the user decide — a silently-broken source is worse than no source, because it makes the digest look complete when it isn't.
