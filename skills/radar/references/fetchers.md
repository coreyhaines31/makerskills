# Fetchers — one recipe per source type

Every command here was verified live. Where a recipe has a gotcha, the gotcha is the reason the recipe looks the way it does — don't "simplify" it back to the obvious version.

## Ground rules

- **Always send a realistic browser User-Agent.** Several of these endpoints return 200 to Chrome and 403/404 to `curl/8.x`. Use:
  `-A "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Safari/537.36"`
- **Parse XML with `/usr/bin/python3`, not `python3`.** On a Mac with Homebrew Python 3.14 installed, `python3` resolves to a build whose `pyexpat` fails to load (`Symbol not found: _XML_SetAllocTrackerActivationThreshold`), which breaks `xml.etree` entirely. System Python parses fine. `xmllint` (ships with macOS) is the other safe option.
- **Pace requests.** Reddit in particular will 429 an unpaced burst and keep 429ing for minutes. Sleep ~2s between requests to the same host, and treat a 429 as `degraded` for the run rather than retrying hard.
- **Timeout everything**: `--max-time 20`. An unattended job that hangs on one dead host is a job that silently never finishes.
- **Never fetch full content during a poll.** Polls read metadata; full fetch happens at capture time only.

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

**Poll — the `.rss` endpoint, not `.json`.**

```bash
curl -s --max-time 20 -A "$UA" "https://www.reddit.com/r/SaaS/new/.rss"
```

**Gotchas — both verified the hard way**

- **`/r/<sub>/new.json` returns 403** for unauthenticated clients regardless of User-Agent. The old "just add `.json`" trick is dead. `.rss` still works.
- **Reddit rate-limits hard and stays angry.** An unpaced burst of a few requests earns a 429 on *every* Reddit endpoint for minutes afterward, including ones that worked seconds earlier. Sleep ≥2s between Reddit calls, do at most one call per source per run, and on 429 mark the source `degraded` and move on. Never retry-loop.
- **Search endpoints (`/search.rss`, `/r/<sub>/search.rss`) 429 much more readily than subreddit feeds.** Prefer a subreddit source over a Reddit keyword source. For keyword coverage of Reddit, use a `keyword` source with a `site:reddit.com` web search instead.

Parse as Atom. Item ID is the entry `<id>` (`t3_1w0uez8`). The entry `<content>` is HTML — strip tags for the scoring excerpt.

`min_score` can't be read from the RSS feed. Apply it at capture time (the post page has it) or leave it unset and let relevance scoring do the work.

**Full fetch (capture)** — fetch the post URL. For link posts, fetch the linked target too; that's usually the actual content. Grab the top few comments — on Reddit the comments are frequently the signal.

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

**No free API. Expect this source type to be degraded some of the time — that's the baseline, not a bug.**

Strategy chain, in order, stopping at the first that works:

1. **`$SCRAPECREATORS_API_KEY` or `$APIFY_TOKEN`** if set — cheapest and most reliable. *(Neither is set on this machine as of 2026-08-28; the chain starts at 2.)*
2. **`social-fetch`** against the profile URL — it owns the fallback logic (agent-browser with modal dismissal, Wayback for older posts) and keeps that knowledge in one place. Prefer this over hand-rolling agent-browser here.
3. **`agent-browser`** directly against `https://x.com/<handle>` with a persistent profile, reading the timeline's article elements.
4. **Ahrefs MCP** (`social-media-posts`, `social-media-authors`) if the handle is tracked there — coverage is partial and lags, so it's a floor, not a plan.

If all fail: mark `degraded` with the reason and continue. Do not retry within the run.

**Unattended runs**: agent-browser needs a logged-in persistent profile to see much of X. If the session expires, the digest should say `x-<handle>: needs re-auth` rather than failing silently — that line is the only thing that will ever prompt a fix.

Item ID: `x:<tweet-id>`. Exclude replies and reposts unless the source opts in — they're where the noise lives.

**Full fetch (capture)** — `social-fetch` on the specific post URL, which pulls the full thread. Prefix `tweet-`.

---

## linkedin

Same shape as X, and harder. LinkedIn actively blocks unauthenticated fetching and rate-limits logged-in automation.

1. **`social-fetch`** against the profile/company URL.
2. **`agent-browser`** with a logged-in persistent profile against `https://www.linkedin.com/in/<slug>/recent-activity/all/`.
3. Otherwise `degraded`.

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

Dedupe across engines by URL before scoring — the same launch shows up on all four. Item ID: `kw:<sha1(url)>`.

Keyword sources are the noisiest type by a wide margin. Start them at `list_at: 4` and never at `auto_capture_at: 4` until one has proven itself for a couple of weeks.

---

## Resolving a target (`add` mode)

| Type | Input | Resolution |
|---|---|---|
| youtube | `@handle` or channel URL | `curl -sL -A "$UA" "https://www.youtube.com/@handle" \| grep -o 'channel_id=UC[A-Za-z0-9_-]*' \| head -1` — **the realistic UA is required**; the default curl UA gets a page with no channel ID in it. Cache the result as `channel_id`. |
| rss | site URL | Feed discovery chain above. Validate the body parses as a feed. |
| reddit | `r/name` or URL | Strip to the name; confirm `https://www.reddit.com/r/<name>/new/.rss` returns entries. |
| hn | query string | Nothing to resolve; test-run it and show hit count. |
| x | `@handle` or URL | Normalize to the handle; test-fetch through the chain and report which tier answered. |
| linkedin | profile/company URL | Normalize to the canonical `/in/<slug>` or `/company/<slug>`. |
| keyword | free text | Nothing to resolve; test-run across the configured engines. |

**A source that fails its test-fetch never gets written to `sources.yaml`.** Report what failed and let the user decide — a silently-broken source is worse than no source, because it makes the digest look complete when it isn't.
