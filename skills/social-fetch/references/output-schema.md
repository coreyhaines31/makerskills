# Normalized output schema

Same shape returned for every platform. Fields with no equivalent on a platform get `null`, not zero or empty string. Missing ≠ zero.

## Schema

```typescript
{
  "platform": "x" | "linkedin" | "linkedin-profile" | "instagram" | "tiktok"
    | "bluesky" | "reddit" | "mastodon" | "threads" | "hn",
  "url": string,                 // canonical URL of the post
  "fetched_at": ISO8601,
  "raw_source":                   // which strategy succeeded
    "direct-api" | "agent-browser" | "open-graph" | "nitter"
    | "wayback" | "scrapecreators" | "apify",

  "author": {
    "handle": string | null,      // @username
    "name": string | null,        // display name
    "verified": boolean | null,
    "follower_count": number | null,
    "profile_url": string | null,
    "avatar_url": string | null
  },

  "posted_at": ISO8601 | null,
  "edited_at": ISO8601 | null,

  "text": string,                 // post body, plain text. Markdown OK if source supports it.
  "html": string | null,          // original HTML if scraped (Mastodon, etc.)
  "language": string | null,      // ISO 639-1 if detected

  "media": Array<{
    "type": "image" | "video" | "gif" | "audio",
    "url": string,
    "alt": string | null,
    "width": number | null,
    "height": number | null,
    "duration_seconds": number | null    // video/audio only
  }>,

  "engagement": {
    "likes": number | null,         // tweets/posts: likes. Reddit: upvotes.
    "reposts": number | null,       // retweets, shares, reposts, reblogs
    "replies": number | null,
    "bookmarks": number | null,
    "views": number | null,
    "quotes": number | null         // quote-tweets where applicable
  },

  "links": Array<{                  // links cited in the post body
    "url": string,
    "expanded_url": string,         // resolved if t.co or similar shortener
    "title": string | null
  }>,

  "mentions": string[],             // @handles mentioned
  "hashtags": string[],

  "is_reply": boolean,
  "reply_to": {                     // if is_reply = true
    "url": string,
    "author_handle": string
  } | null,

  "is_thread": boolean,             // post is part of a multi-post thread by same author
  "thread": Array<{                 // siblings in the thread (excludes self), in order
    "url": string,
    "text": string,
    "posted_at": ISO8601
  }>,

  "replies": Array<{                // top-level replies (only if --with-replies)
    "url": string,
    "author": { "handle": string, "name": string },
    "text": string,
    "posted_at": ISO8601,
    "engagement": { "likes": number, "replies": number }
  }>,

  "raw": object | null               // raw API/scrape response (only if --raw)
}
```

## Platform field-coverage matrix

What each platform typically provides on a successful free-strategy fetch:

| Field | bluesky | mastodon | hn | reddit | x (free) | x (paid) | linkedin (free) | linkedin (paid) | ig (paid) | tiktok (paid) | threads (paid) |
|---|---|---|---|---|---|---|---|---|---|---|---|
| author.handle | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| author.verified | — | — | — | — | partial | ✅ | — | ✅ | ✅ | ✅ | ✅ |
| author.follower_count | ✅ | ✅ | — | — | — | ✅ | — | ✅ | ✅ | ✅ | ✅ |
| posted_at | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | partial | ✅ | ✅ | ✅ | ✅ |
| text | ✅ | ✅ | ✅ | ✅ | partial | ✅ | partial | ✅ | ✅ | ✅ | ✅ |
| media | ✅ | ✅ | — | ✅ | — | ✅ | — | ✅ | ✅ | ✅ | ✅ |
| engagement.likes | ✅ | ✅ | ✅ (score) | ✅ | — | ✅ | — | ✅ | ✅ | ✅ | ✅ |
| engagement.reposts | ✅ | ✅ | — | — | — | ✅ | — | ✅ | — | ✅ | ✅ |
| engagement.views | — | — | — | — | — | ✅ | — | partial | partial | ✅ | partial |
| replies | ✅ | ✅ | ✅ | ✅ | — | ✅ | — | partial | — | partial | partial |
| thread (own author) | ✅ | ✅ | n/a | n/a | — | ✅ | — | ✅ | — | — | partial |

`partial` = sometimes available depending on the post / scraping conditions.

## Example outputs (abbreviated)

### bluesky — full

```json
{
  "platform": "bluesky",
  "url": "https://bsky.app/profile/jay.bsky.team/post/3kphvqpv6xs2t",
  "raw_source": "direct-api",
  "author": {
    "handle": "@jay.bsky.team",
    "name": "Jay Graber",
    "verified": null,
    "follower_count": 500123
  },
  "posted_at": "2026-06-15T14:23:00Z",
  "text": "We're rolling out video posts.",
  "media": [],
  "engagement": {
    "likes": 1245, "reposts": 234, "replies": 89, "bookmarks": null, "views": null
  }
}
```

### x — partial (free strategy: agent-browser preview)

```json
{
  "platform": "x",
  "url": "https://x.com/coreyganim/status/2067289417803538931",
  "raw_source": "agent-browser",
  "author": {
    "handle": "@coreyganim",
    "name": "Corey Ganim",
    "verified": true,
    "follower_count": null
  },
  "posted_at": "2026-06-17T16:53:00Z",
  "text": "The 80/20 of a useful AI second brain: ...",
  "engagement": {
    "likes": 51, "reposts": 13, "replies": 9, "bookmarks": 7, "views": 32700
  },
  "is_thread": true,
  "thread": []
}
```

Note `thread: []` despite `is_thread: true` — free strategy can detect a thread exists but can't fetch the other posts. Use paid fallback or visit each thread URL directly.

### hn — full

```json
{
  "platform": "hn",
  "url": "https://news.ycombinator.com/item?id=12345678",
  "raw_source": "direct-api",
  "author": { "handle": "pg" },
  "posted_at": "2026-06-15T18:00:00Z",
  "text": "Title of the submission",
  "links": [{"url": "https://example.com/article", "expanded_url": "https://example.com/article"}],
  "engagement": { "likes": 234, "replies": 89 },
  "replies": [
    {
      "url": "https://news.ycombinator.com/item?id=12345679",
      "author": { "handle": "user1" },
      "text": "Great article because…",
      "engagement": { "likes": 45, "replies": 3 }
    }
  ]
}
```

## Returning to the user

When the skill completes, output:

1. **One-line summary** in chat: `<author> · <platform> · <date> · "<first 80 chars>..."`
2. **Path to the JSON output** if `--save` flag set (saved to `~/Documents/social-fetches/<platform>-<id>.json`)
3. **Inline JSON** in chat for the calling skill / Corey to use

If only partial data was retrievable (free strategy on X/LinkedIn/IG/TikTok), surface it clearly: *"Free strategy returned author + text + engagement. Replies + full thread require `$SCRAPECREATORS_API_KEY`. See references/auth-keys.md to set up."*
