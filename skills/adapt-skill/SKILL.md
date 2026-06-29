---
name: adapt-skill
description: When you want to port an external skill (from GitHub, agentskills.io, or anywhere public) into one of his sibling skill repos and adapt it to his voice, tooling, and conventions. Examples already done informally — riffing on garrytan/gstack for naming, frontend-slides for the slide-deck workflow, last30days for deep-research, llm-wiki for second-brain. Three-bucket analysis (keep verbatim / adapt / add), tool-swap pass (their video tool → Corey's watch-video, their kanban → pm, etc.), voice pass, attribution file, license check (MIT/Apache green; GPL warn; proprietary stop). Triggers on "/adapt-skill <url>," "adapt this skill," "port this skill," "fork this skill," "borrow this skill," "let's adapt X for our repo," "make our own version of this." Sibling to create-skill — that one creates from chat/dump/scratch; this one adapts from an external source.
metadata:
  version: 0.1.0
---

# /adapt-skill — Port an external skill into your namespace

Sibling to `create-skill`. Different jobs:

- `create-skill` → build a new skill from chat / dump / scratch
- `adapt-skill` → take someone else's skill and make it yours

## Step 1 — Fetch the source

Accept:
- **GitHub URL** to a SKILL.md or a repo containing one (`https://github.com/<owner>/<repo>` or `https://github.com/<owner>/<repo>/blob/main/SKILL.md`)
- **agentskills.io URL** or **skills.sh URL**
- **Local path** to an existing skill on disk (other plugins installed in `~/.claude/plugins/`)
- **Pasted SKILL.md content**

```bash
# GitHub repo: clone shallow to a temp dir
git clone --depth 1 <url> /tmp/adapt-skill-<short-id>/
# OR fetch a single file
gh api -H "Accept: application/vnd.github.raw" repos/<owner>/<repo>/contents/SKILL.md > /tmp/adapt-source.md
```

Capture the commit SHA so attribution can point at a stable revision.

## Step 2 — Analyze + classify

Read the source SKILL.md + any `references/` it ships. Classify into three buckets per `references/buckets.md`:

| Bucket | What | Example |
|---|---|---|
| **Keep verbatim** | Format, schema, mechanic, scripts, frameworks | The 38 decision questions, ffmpeg flags, a regex pattern, JSON schema for output |
| **Adapt** | Tool defaults, paths, voice, naming, opinions | Their video tool → your `watch-video`, their kanban → your `pm`, their voice → your voice, their "user" → "Corey" specifics |
| **Add** | Cross-references to your existing skills, composition notes, your conventions | "Composes with `decide`," "Saves to `second-brain raw/` as `<prefix>-`," "Uses MLX-Whisper local" |

Output the classification as a table for Corey to approve before writing anything. Don't silently rewrite — surface the changes.

## Step 3 — License check

Read the source repo's LICENSE file. See `references/license-check.md` for the policy:

| License | Action |
|---|---|
| MIT / Apache-2.0 / BSD / ISC / CC0 | ✅ Green — proceed |
| MPL-2.0 / LGPL | 🟡 Yellow — adapt OK but warn about file-level reciprocity |
| GPL-2.0 / GPL-3.0 / AGPL | ❌ Red — contagion risk for derivative work. Surface to Corey before proceeding. |
| Proprietary / no license | ❌ Red — stop. No legal basis to copy. |
| Unclear | 🟡 Yellow — ask Corey, default to skip if uncertain |

For permissive licenses, attribution is the only requirement — handled in Step 6.

## Step 4 — Pick target repo

Same as `create-skill`. Match by topic:

| Repo | What lives here |
|---|---|
| **makerskills** | Personal cross-cutting operator work |
| **cf-skills** | CF agency operations |
| **marketingskills** | Generic marketing tactics (public) |
| **nonfictionskills** | Writing a nonfiction book |
| **fictionskills** | Writing fiction |
| **youtubeskills** | Making YouTube videos |

Infer if obvious; ask if ambiguous.

## Step 5 — Rewrite the skill

For each bucket from Step 2:

**Keep verbatim**: copy as-is. Add a comment marker if helpful (`<!-- from <source> -->`).

**Adapt**:
- **Naming**: rename to verb-noun if not (matches your convention: `watch-video`, `read-book`, `create-skill`, `adapt-skill`)
- **Tool swaps**: their generic kanban tool → your `pm`; their video tool → `watch-video`; their transcript tool → `watch-video transcript`; their note system → `second-brain`; their decision framework → `decide`
- **Voice**: apply your voice rules — direct, conviction-coded, no AI-slop. For social-adjacent skills, apply the link-placement rule.
- **Paths**: their `~/outputs/` → your `~/Documents/<skill>-<...>/` convention; their config files → your `references/` pattern
- **Names + context**: their "the user" / generic examples → Corey + his portfolio context (CF, Swipe Files, Magister, Truelist, etc.) where the skill needs it

**Add**:
- Cross-references to existing makerskills/cf-skills/marketingskills siblings
- Composition notes (which other skills this calls or feeds)
- Your conventions (frontmatter version, references/ subdir structure, BACKLOG entry if it spawns sub-ideas)

## Step 6 — Attribution file

Write `references/attribution.md`:

```markdown
# Attribution

This skill was adapted from an external source. Original credit:

- **Source**: <original SKILL.md URL>
- **Repository**: <repo URL>
- **Author**: <author name + handle if known>
- **Commit SHA**: <SHA at time of adapt>
- **License**: <license name + URL>
- **Adapted**: <YYYY-MM-DD>
- **Adapted by**: Corey Haines

## What was kept verbatim
- <piece>
- <piece>

## What was adapted
- <piece> → <new version>
- <piece> → <new version>

## What was added
- <piece>
- <piece>

## License compliance

<copy the upstream LICENSE text here if MIT/BSD/Apache requires it, OR reference where in this repo it lives>

## Upgrade path

To check for upstream changes:
\`\`\`bash
git ls-remote <repo-url> HEAD
\`\`\`

Compare returned SHA to the "Commit SHA" above. If different, run `/adapt-skill` again on the same source to re-port (you'll get a 3-way merge view: upstream changes vs your local adaptations vs current).
```

For permissive licenses requiring notice (MIT, Apache, BSD), the LICENSE text either gets copied into this file or the source LICENSE file gets copied to the skill dir.

## Step 7 — Scaffold + commit

Same as `create-skill` Step 6–7:
- Write `SKILL.md` + `references/` (including `attribution.md`)
- Append to target repo's README skill table
- Commit with message: `"Adapt <name> skill from <source-name>"`
- Push

## Step 8 — Report + offer follow-ups

- Commit hash + new skill path
- Show the three-bucket classification one more time (what was kept / adapted / added) so Corey sees the diff clearly
- Offer:
  - *"Want to flesh out the adaptations? Some defaults may still need your touch."*
  - *"Want me to run `compound-engineering:heal-skill` for a QA pass?"*
  - *"Should I set up an upstream-check reminder via `loop` or `compound-engineering:schedule`?"*

## Composes with

- `create-skill` — sibling. Use that for from-scratch / from-chat / from-dump. Use this for from-external.
- `compound-engineering:create-agent-skill` — call into for format expertise during the rewrite
- `compound-engineering:heal-skill` — QA pass after adaptation
- `compound-engineering:skill-creator` — deep best-practices reference
- `loop` / `compound-engineering:schedule` — for periodic upstream-check (future enhancement)

## Examples of adaptations already done informally in this repo

These were done by hand during the conversation that built this plugin. Future ones should run through `/adapt-skill`:

| Source | Adapted into | What was taken |
|---|---|---|
| `zarazhangrui/frontend-slides` | `slide-deck` | "Show, don't tell" pattern, density modes, anti-AI-slop rules, Playwright export approach |
| `mvanhorn/last30days-skill` | `deep-research` (composes) | Used as a sub-tool, not adapted directly |
| Hermes' `llm-wiki` | `second-brain` (reference) | Schema validation — referenced but not ported |
| `garrytan/gbrain` | `second-brain` | People-as-entities, scheduled maintenance pattern |
| `garrytan/gstack` | Naming inspiration | Short brand-able skill repo names |

These already exist with informal attribution in their SKILL.md bodies. If you want, run `/adapt-skill` retroactively on any of them to get a proper `references/attribution.md` file.

## Notes on quality

- **Surface the bucket classification before writing.** Don't silently rewrite — Corey approves what changes and what stays.
- **Attribution is non-negotiable.** Every adapted skill ships with `references/attribution.md`. Credit + license compliance + future upgrade path live here.
- **License is the gate.** Don't proceed on GPL/proprietary without explicit Corey approval. Defaults to stop, not warn.
- **Don't import dependencies you don't need.** If the source ships 5 reference files and you only need 2, leave the other 3. Carrying weight = future maintenance.
- **Tool-swap aggressively.** If your stack has a better-fit tool than the source's choice, swap. The adaptation IS the value — verbatim copies aren't.
