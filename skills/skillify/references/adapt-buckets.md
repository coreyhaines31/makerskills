# Three-bucket classification

When porting a skill, every piece of the source maps to one of three buckets. Surface this classification to the user **before** writing the adapted skill — never silently rewrite.

## Bucket 1: Keep verbatim

What it is: format, schema, mechanic, scripts, frameworks, regex patterns, JSON shapes, math/algorithm details.

Why: this is the *value* the source is bringing. Reinventing wastes effort and risks bugs.

Examples:
- The 38 decision questions from the 37signals decision skill
- ffmpeg flag patterns for frame extraction
- A regex for detecting URLs in a post
- A JSON schema for the output payload
- Specific API endpoints + auth patterns
- The viewport-base.css from frontend-slides
- The Karpathy LLM wiki schema rules

Action: **copy as-is**. Optionally add a `<!-- from <source> -->` marker.

## Bucket 2: Adapt

What it is: tool defaults, paths, voice, naming, opinions, user-context examples.

Why: these are the source author's preferences. Yours differ.

### Sub-buckets to look for

| Sub-bucket | Source has | Adapt to |
|---|---|---|
| **Naming** | Their convention | Verb-noun (matches `watch-video`, `read-book`, `create-skill`) when possible |
| **Tool defaults** | Their video tool | Your `watch-video` |
| | Their kanban | Your `pm` |
| | Their transcript tool | Your `watch-video transcript` mode |
| | Their notes / KB | Your `second-brain` (or `${SECOND_BRAIN_VAULT:-$HOME/Documents/SecondBrain}/`) |
| | Their decision framework | Your `decide` |
| | Their social drafting | Your `jab-hook` |
| | Their research | Your `deep-research` |
| **Paths** | `~/outputs/` or `~/notes/` | `~/Documents/<skill>-<...>` convention |
| | Custom config dirs | Your `references/` pattern |
| **Voice** | Generic / corporate / theirs | Yours — direct, conviction-coded, listener-perspective, no AI-slop |
| **Context** | "The user," generic examples | Your specific context (your name, your products / portfolio / partnerships) where the skill needs it |
| **Defaults** | Their assumed environment | Your Mac, MLX-Whisper, brew, uv, Notion API key, Typefully MCP, etc. |
| **Cadence** | Their suggested frequency / WIP limits | Yours (e.g., 2 promo/week for social, 3 In-Progress WIP for pm) |

Action: **rewrite** the affected lines, surface the change in the bucket report.

## Bucket 3: Add

What it is: cross-references, composition notes, your conventions that the source doesn't know about.

Why: the source is generic; your version sits in a network of other skills.

Examples:
- "Composes with `decide`" (when the skill hits a decision moment)
- "Outputs to `second-brain raw/` as `<prefix>-`"
- "Falls back to `social-fetch` for the URL fetch step"
- "Uses MLX-Whisper local (see install in `watch-video` references)"
- Memory references: `feedback_*` files in `~/.claude/memory/`
- BACKLOG.md entry if the adapt spawns sub-ideas

Action: **add net-new sections** to the adapted SKILL.md — typically a `## Composes with` section and inline references in the body.

## Bucket report format

Present to the user before writing:

```markdown
## Three-bucket classification — <source skill name>

### Keep verbatim
- <piece 1>
- <piece 2>

### Adapt
- <source piece> → <new version> (why: <reason>)
- <source piece> → <new version> (why: <reason>)

### Add
- <new piece> (compose with `<your skill>`)
- <new piece>

**Proceed?** y/n / edit
```

the user approves, edits, or rejects. Only then proceed to write the adapted SKILL.md.
