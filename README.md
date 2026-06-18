# makerskills

Personal Claude Code skills for Corey Haines — sibling to [`marketingskills`](https://github.com/coreyhaines31/marketingskills) and `cf-skills`.

Where `marketingskills` covers marketing tactics and `cf-skills` covers Conversion Factory operations, **`makerskills`** covers the cross-cutting craft-forward operator work: decisions, research, brainstorming, content rotation, utilities, and the meta skill that scaffolds new skills.

## Install

```bash
# In Claude Code
/plugin marketplace add coreyhaines31/makerskills
/plugin install makerskills@makerskills
```

Or for local development, symlink into `~/.claude/plugins/`:

```bash
ln -s ~/code/makerskills ~/.claude/plugins/makerskills
```

## Structure

```
makerskills/
├── .claude-plugin/
│   ├── plugin.json        # plugin manifest
│   └── marketplace.json   # marketplace listing
├── skills/
│   └── <skill-name>/
│       ├── SKILL.md       # skill instructions + frontmatter
│       └── references/    # optional supporting files (templates, archives, etc.)
└── README.md
```

### SKILL.md frontmatter

```yaml
---
name: skill-name
description: When the user wants to [X]. Also use when they mention "[trigger phrase]"...
metadata:
  version: 0.1.0
---
```

The `description` is what Claude uses to decide when to load the skill — be specific about triggers, what it does, and when to use it vs. other skills.

## Cross-referencing other skill collections

Skills can reference each other across plugins by name. In a SKILL.md description or body:

- **Within this plugin:** mention by skill name (`see decide`)
- **From `marketing-skills`:** mention with prefix (`see marketing-skills:cro`)
- **From `cf-skills`:** mention with prefix (`see cf-skills:positioning`)
- **From other plugins (`compound-engineering`, `vercel`, `expo`, etc.):** mention by plugin-prefixed name

Claude resolves these by description match at load time. No manifest linking needed — keep references readable in prose.

## Related skill collections

- [`marketingskills`](https://github.com/coreyhaines31/marketingskills) — 44 marketing skills (CRO, copywriting, SEO, ads, etc.)
- `cf-skills` — Conversion Factory-specific skills (positioning, brand strategy, growth engine, cf-blog, x-li, etc.)

## Skills

| Skill | What it does |
|---|---|
| [`add-skill`](./skills/add-skill/SKILL.md) | Bootstrap a new skill in this plugin. Generates SKILL.md frontmatter, creates references/, updates README, commits + pushes. Meta — speeds every other skill we build. |
| [`business-brainstorm`](./skills/business-brainstorm/SKILL.md) | Pressure-test a potential new business or product against Corey's serial-founder filter (9 dimensions). Composes with `deep-research` and `/domain`. Archives every brainstorm so past ideas are searchable + revisit-able. |
| [`decide`](./skills/decide/SKILL.md) | Structured decision workflow based on the 37signals Guide to Making Decisions (38 questions). Triages to 6–8 load-bearing questions per decision, walks through them, reaches a call, archives the rationale with a revisit date. Composes with `business-brainstorm`. |
| [`deep-research`](./skills/deep-research/SKILL.md) | Multi-source research with citations and archive. Uses WebSearch, WebFetch, agent-browser, `/last30days`, memory, Notion. Outputs structured brief with contradictions and gaps. Compounds — every run adds to the archive. |
| [`my-social`](./skills/my-social/SKILL.md) | Personal portfolio rotation for X + LinkedIn. Ensures each of Corey's 6 properties gets promoted ~1× every 3 weeks, with build-in-public + educational filling the rest. Drafts and syndicates to personal Typefully workspace. |
| [`paste`](./skills/paste/SKILL.md) | Clean terminal output for any destination (Slack, Notion, Twitter, LinkedIn, email, GitHub, plain, HTML). Strips ANSI codes, box-drawing chars, prompts. Reads clipboard, writes back to clipboard + chat preview. Scans for secrets first. |
| [`pm`](./skills/pm/SKILL.md) | Project management across your portfolio. Kanban (5-column) + Eisenhower methodology. Tool-agnostic adapters (Notion, GitHub Projects, Plane, Linear, Obsidian, manual). One board per business. Six modes: setup, triage, next, status, unblock, weekly. |
| [`read-book`](./skills/read-book/SKILL.md) | Read PDFs, EPUBs, MOBI, markdown books with structured note extraction. Four modes: `notes` (chapter-by-chapter — default), `summary` (TL;DR + takeaways), `quotes` (pull quotes only), `study` (notes + spaced-rep Q&A). Chunks by chapter when TOC exists, by 50 pages otherwise. Captures to `second-brain raw/` as `highlights-`. Sibling to `watch-video`. |
| [`second-brain`](./skills/second-brain/SKILL.md) | Karpathy LLM Wiki workflow over your Obsidian vault (`~/SecondBrain/`). Three layers: raw/ (sources) → wiki/ (compiled topic pages with [[wikilinks]]) → outputs/ (generated artifacts). Six modes: capture, compile, query, lint, connect, search. Complements `deep-research` (this is internal corpus). |
| [`slide-deck`](./skills/slide-deck/SKILL.md) | Draft branded React decks for `corey.co/slides`. Generates TypeScript `Slide[]` for `${COREYCO_REPO:-$HOME/code/coreyco}/src/app/slides/<slug>/page.tsx` using your primitives (Eyebrow, Heading, Accent, Body, BulletList, Divider, TwoCol). "Show, don't tell" applied to narrative — pitches 3 angles, you pick. Speaker notes per slide. For unbranded HTML/PDF decks, use `frontend-slides` instead. |
| [`social-fetch`](./skills/social-fetch/SKILL.md) | Pull any social post by URL (X, LinkedIn, Instagram, TikTok, Bluesky, Reddit, Mastodon, Threads, HN). Detects platform, tries strategies in order (free APIs → agent-browser → Wayback → paid fallback), returns normalized JSON. Free strategies cover Bluesky/Mastodon/HN/Reddit fully; X/LinkedIn/IG/TikTok need ScrapeCreators or Apify keys for full data. |
| [`watch-video`](./skills/watch-video/SKILL.md) | Transcribe and analyze any video — YouTube, Loom, Vimeo, Riverside, Zoom, local MP4. Three depth modes: `transcript` (Whisper local), `visual` (transcript + ffmpeg frames + Claude vision on key moments), `multimodal` (Gemini native if `$GEMINI_API_KEY`, else dense Claude vision). Optionally captures summary to `second-brain raw/` as `call-`/`meeting-`/`note-`/`resource-`. Replaces the prior `youtube-transcript` skill. |
