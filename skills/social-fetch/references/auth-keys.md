# Auth keys — unlocking paid fallback strategies

The free strategies (Bluesky API, Mastodon API, HN Algolia, Reddit .json, agent-browser) work for many cases. For X / LinkedIn (specific posts) / Instagram / TikTok / Threads, paid keys unlock reliable + complete data.

## Which key unlocks what

| Key | Unlocks | Cost (approx, 2026) |
|---|---|---|
| `$SCRAPECREATORS_API_KEY` | X (tweets + threads + replies), LinkedIn posts, Instagram, TikTok, possibly Threads | Pay-as-you-go, ~$0.005–$0.02/post depending on endpoint |
| `$APIFY_API_TOKEN` | Nearly any platform via "Actors" (X, IG, TikTok, LinkedIn, Threads, even niche ones) | Per-actor pricing, often $1–$5 / 1K results |

## Setting up

### ScrapeCreators

1. Sign up at https://scrapecreators.com
2. Get API key from dashboard
3. Add to `~/.zshenv`:
   ```bash
   export SCRAPECREATORS_API_KEY="<your-key>"
   ```
4. `source ~/.zshenv` or new terminal
5. Verify: `echo $SCRAPECREATORS_API_KEY | head -c 8`

### Apify

1. Sign up at https://apify.com (free tier exists; pay-as-you-go after)
2. Get API token from Settings → Integrations → API
3. Add to `~/.zshenv`:
   ```bash
   export APIFY_API_TOKEN="<your-token>"
   ```
4. `source ~/.zshenv`
5. Verify: `echo $APIFY_API_TOKEN | head -c 8`

## Free-only mode

If neither key is set, `social-fetch` runs in free-only mode:

- **Bluesky / Mastodon / HN / Reddit** — fully functional
- **X** — preview only (text + basic engagement, no thread/replies)
- **LinkedIn profiles** — recent activity feed visible (no specific post fetch)
- **Instagram / TikTok / Threads** — Open Graph metadata only (title, description, image — no engagement, no replies)

This is fine for most one-off fetches. Paid fallback is mostly useful when:
- Building corpus (deep-research running many fetches)
- Analyzing thread structure or reply trees on X
- Inspiration-account analysis on Instagram / TikTok (where free fails entirely)

## Cost discipline

When using paid strategies:
- Always check the cache first (`~/Documents/social-fetches/_cache/` if it exists)
- Default to 24h cache TTL
- Don't auto-enrich with `--with-replies` or `--thread` unless requested — these multiply quota use
- For high-volume work (e.g., fetching last 50 posts from an inspiration account), batch via Apify actors (cheaper per item) instead of ScrapeCreators per-call

## When to set up paid

Don't set up keys preemptively. Set them up when:
- A real workflow (deep-research, inspiration analysis, competitor monitoring) is being blocked
- You've done >10 fetches and the free strategies are missing data you need
- You're starting on `swipe-save` or another skill where social capture is central

If `social-fetch` falls through to "no paid key set" on the same platform 3+ times in a session, it'll surface a one-time prompt.
