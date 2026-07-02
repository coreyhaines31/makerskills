---
name: skillify
description: When you want to create, adapt, or update a Claude Code skill in one of your sibling repos (list your own repos in ~/.config/makerskills/skillify/repos.yaml; defaults to makerskills). Routes to the right mode automatically. Modes — CREATE (from-chat / from-video / from-dump / from-scratch) turns a workflow, brief, recording, or fresh idea into a new skill. ADAPT ports an external skill (GitHub URL, agentskills.io, local disk) into your namespace with three-bucket classification (keep/adapt/add) + license check + attribution. UPDATE improves existing skills from learnings with cross-skill propagation, memory-vs-skill triage, and semver discipline. Defers to Anthropic's guidance (compound-engineering:create-agent-skill, compound-engineering:skill-creator, compound-engineering:heal-skill) for schema and best-practice depth. Triggers on "/skillify," "create a skill," "make this a skill," "skill from this chat," "extract a skill from what we've been doing," "adapt this skill," "port this skill," "fork this skill," "borrow this skill," "update X skill," "apply this to the relevant skills," "propagate this learning," "improve [skill]," "fix [skill]," "iterate on [skill]." Part of the -ify trifecta (skillify / toolify / loopify) for extending Claude Code.
metadata:
  version: 0.2.0
---

# /skillify — Create, adapt, or update a skill

One skill, three modes. Routes automatically to the right one based on input signal.

Consolidates and replaces the prior `create-skill`, `adapt-skill`, and `update-skill` (all merged as of v0.2.0 for vocabulary-moat consistency with the `-ify` trifecta).

## Step 0 — Detect mode

Route by signal:

| Signal | Mode |
|---|---|
| Invoked mid-conversation with substantive recent workflow discussion | **CREATE / from-chat** (default) |
| `/skillify from-video <url>` OR `/skillify` + a video URL | **CREATE / from-video** |
| `/skillify from-dump` + pasted brief/transcript/notes | **CREATE / from-dump** |
| `/skillify from-scratch <name>` OR "make a new skill called X" with no context | **CREATE / from-scratch** |
| `/skillify <github-url>` OR "adapt this skill" / "port this skill" / "fork this skill" + external source | **ADAPT** |
| `/skillify <existing-skill> <change>` OR "update X skill" / "propagate this learning" | **UPDATE / targeted** |
| `/skillify update` (mid-conversation) | **UPDATE / from-chat** — scan recent chat for learnings |
| `/skillify usage <skill>` | **UPDATE / usage** — review recent runs, suggest improvements |

If ambiguous, ask before proceeding. Never guess between CREATE and ADAPT if there's an external URL involved.

---

## Mode: CREATE

Build a new skill from chat / video / dump / scratch.

### Step 1 — Confirm the input source

| Sub-mode | What |
|---|---|
| **from-chat** (default) | Extract the skill from the workflow discussed in this conversation. Most common case. |
| **from-video** | User recorded a Loom / Zoom / screen-share. Calls `watch-video` in visual mode → transcript + key visual moments → SKILL.md. Best for visual/UI-heavy workflows. |
| **from-dump** | User pastes a brief, prior conversation transcript, exported chat, or notes. |
| **from-scratch** | Fresh idea with no source material — interactive Q&A. |

### Step 2 — Defer to Anthropic guidance for the schema

Don't reinvent SKILL.md format rules. For frontmatter, description-writing, references/ structure, and skill best practices:

- **`compound-engineering:create-agent-skill`** (agent) — expert guidance for creating + editing Claude Code skills
- **`compound-engineering:skill-creator`** (skill) — deeper guide for effective skills
- **`compound-engineering:heal-skill`** (skill) — for fixing existing skills
- **[anthropics/skills](https://github.com/anthropics/skills)** — official Anthropic examples
- **[agentskills.io](https://agentskills.io)** — open Agent Skills spec

Call those directly when in doubt about format. `skillify` orchestrates *your* workflow — which repo, which conventions, which cross-references. Format expertise lives upstream.

### Step 3 — Pick target repo

Load the user's sibling repo list from `${MAKERSKILLS_CONFIG:-$HOME/.config/makerskills}/skillify/repos.yaml` if present. Otherwise default to `makerskills` (this repo). Example format:

```yaml
# ~/.config/makerskills/skillify/repos.yaml
repos:
  - name: makerskills
    domain: Personal cross-cutting operator work
    path: ~/code/makerskills
  - name: marketingskills
    domain: Generic marketing tactics
    path: ~/code/marketingskills
```

Infer target if obvious from the skill's domain; ask if ambiguous.

### Step 4 — Synthesize per sub-mode

**from-chat:**
1. Read backward through this conversation. Look for a workflow repeated multiple times, a process re-explained, opinions restated, tooling/voice/output decisions.
2. Identify the load-bearing pieces: trigger, steps, references, success shape, voice.
3. Surface gaps that need clarification before scaffolding — ask 2–4 tight questions.
4. Draft SKILL.md, citing chat moments inline ("Per your message about X…") so the user can verify.

**from-dump:**
1. Parse the dump (Notion page, Slack thread, Loom transcript, teammate brief, exported ChatGPT conversation).
2. Same synthesis logic as from-chat.
3. Cite where in the dump each rule came from.

**from-video:**
1. Take the URL or local path.
2. Call `watch-video <url> visual` — get transcript + key visual moments + summary.
3. Read outputs: `<workdir>/transcript.txt`, `<workdir>/moments.md`, `<workdir>/summary.md`.
4. Synthesize: trigger (first 30s), steps (visual moments + matching transcript), tools used, decision points ("if X do Y" moments), success shape (last few seconds), voice cadence.
5. Surface gaps — ambiguous moments needing clarification.
6. Draft SKILL.md citing video moments by timestamp.
7. Optionally save the source to `second-brain` as `call-<slug>.md` or `note-<slug>.md`.

Heuristic: recording >10 minutes = process probably too big for one skill. Suggest splitting before drafting.

**from-scratch:**
Interactive Q&A:
1. Name (kebab-case, verb-noun preferred — matches `watch-video`, `read-book`, `paste`)
2. One-line purpose
3. Trigger phrases (4–8)
4. Initial reference files?
5. Composes with which other skills?

### Step 5 — Generate frontmatter

```yaml
---
name: <kebab-case>
description: <rich, trigger-rich, ~2–4 sentences. Lead with "When you want to..." Include 4–8 trigger phrases in quotes. Differentiate from adjacent skills.>
metadata:
  version: 0.1.0
---
```

Description rules (load-bearing — Claude routes by description match):
- Lead with the use case ("When you want to X…")
- Include explicit trigger phrases
- Differentiate from sibling skills
- Mention key references the skill loads
- Keep under ~500 characters

For deeper description-writing guidance, consult `compound-engineering:skill-creator`.

### Step 6 — Scaffold the directory

```
<target-repo>/skills/<name>/
├── SKILL.md
└── references/
    └── ...
```

Body follows existing skills' pattern (`pm`, `decide`, `second-brain`):
- `# /<name> — <one-line purpose>`
- Numbered `## Step N — <phase>` sections
- Composes-with cross-references
- Quality notes at the end

### Step 7 — Update README, commit, push

Append to target repo's README skill table:

```markdown
| [`<name>`](./skills/<name>/SKILL.md) | <one-line purpose> |
```

Commit + push. Report new skill path, commit hash, and reminder that `/plugin install` or symlink may need a refresh.

### Step 8 — Offer follow-ups

- *"Flesh out a specific Step now, or come back to it?"*
- *"Run through `compound-engineering:heal-skill` for a quality pass?"*
- *"Should this compose with [adjacent skill]?"*

---

## Mode: ADAPT

Port an external skill (GitHub URL, agentskills.io, local disk, or pasted SKILL.md) into your namespace.

### Step 1 — Fetch the source

Accept:
- **GitHub URL** to a SKILL.md or repo (`https://github.com/<owner>/<repo>` or full path to SKILL.md)
- **agentskills.io URL** or **skills.sh URL**
- **Local path** to an existing skill on disk (other plugins in `~/.claude/plugins/`)
- **Pasted SKILL.md content**

```bash
# GitHub repo: clone shallow
git clone --depth 1 <url> /tmp/skillify-adapt-<short-id>/
# OR fetch a single file
gh api -H "Accept: application/vnd.github.raw" repos/<owner>/<repo>/contents/SKILL.md > /tmp/adapt-source.md
```

Capture the commit SHA so attribution can point at a stable revision.

### Step 2 — Analyze + classify

Read source SKILL.md + any `references/` it ships. Classify into three buckets per `references/adapt-buckets.md`:

| Bucket | What | Example |
|---|---|---|
| **Keep verbatim** | Format, schema, mechanic, scripts, frameworks | Question banks, ffmpeg flags, regex patterns, JSON schemas |
| **Adapt** | Tool defaults, paths, voice, naming, opinions | Their video tool → your `watch-video`, their kanban → your `pm`, their voice → your voice |
| **Add** | Cross-references to your existing skills, composition notes, your conventions | "Composes with `decide`," "Saves to `second-brain raw/`," "Uses MLX-Whisper local" |

Output classification as a table for approval before writing anything. Don't silently rewrite — surface the changes.

### Step 3 — License check

Read the source's LICENSE. Per `references/adapt-license-check.md`:

| License | Action |
|---|---|
| MIT / Apache-2.0 / BSD / ISC / CC0 | ✅ Green — proceed |
| MPL-2.0 / LGPL | 🟡 Yellow — adapt OK; warn about file-level reciprocity |
| GPL-2.0 / GPL-3.0 / AGPL | ❌ Red — contagion risk. Surface before proceeding. |
| Proprietary / no license | ❌ Red — stop. No legal basis to copy. |
| Unclear | 🟡 Yellow — ask, default to skip if uncertain |

For permissive licenses, attribution is the only requirement — handled in Step 6.

### Step 4 — Pick target repo

Same table as CREATE Step 3.

### Step 5 — Rewrite

**Keep verbatim**: copy as-is; add `<!-- from <source> -->` marker if helpful.

**Adapt:**
- Naming: rename to verb-noun if not (matches `watch-video`, `read-book`, `paste`)
- Tool swaps: their generic kanban → `pm`, their video tool → `watch-video`, their note system → `second-brain`, their decision framework → `decide`
- Voice: apply your voice rules — direct, conviction-coded. For social-adjacent skills, apply link-placement rule.
- Paths: their `~/outputs/` → your `~/Documents/<skill>-<...>/` convention; their config → your `references/` pattern
- Names + context: generic examples → your portfolio context where the skill needs it

**Add:**
- Cross-references to existing sibling skills
- Composition notes (which other skills this calls or feeds)
- Your conventions (frontmatter version, references/ subdir structure, BACKLOG entry if it spawns sub-ideas)

### Step 6 — Attribution file

Write `references/attribution.md`:

```markdown
# Attribution

- **Source**: <original SKILL.md URL>
- **Repository**: <repo URL>
- **Author**: <name + handle>
- **Commit SHA**: <SHA at time of adapt>
- **License**: <license name + URL>
- **Adapted**: <YYYY-MM-DD>

## What was kept verbatim
- ...

## What was adapted
- <old> → <new>

## What was added
- ...

## License compliance
<upstream LICENSE text if MIT/BSD/Apache requires it, OR reference where in this repo it lives>

## Upgrade path
Run `git ls-remote <repo-url> HEAD`. If SHA differs from above, re-run `/skillify <same-url>` for a 3-way merge.
```

For MIT / Apache / BSD, LICENSE text either gets copied into this file or the source LICENSE file gets copied to the skill dir.

### Step 7 — Scaffold + commit

Same as CREATE Steps 6–7. Commit message: `"Adapt <name> skill from <source-name>"`.

### Step 8 — Report + offer follow-ups

- Commit hash + new skill path
- Show three-bucket classification one more time so the diff is clear
- Offer:
  - *"Flesh out the adaptations? Some defaults may still need your touch."*
  - *"Run `compound-engineering:heal-skill` for a QA pass?"*
  - *"Set up an upstream-check reminder via `loopify`?"*

---

## Mode: UPDATE

Improve existing skill(s) from learnings.

### Step 1 — Confirm sub-mode

| Sub-mode | When |
|---|---|
| **from-chat** (default) | Scan recent conversation for learnings, identify affected skill(s) |
| **from-dump** | User provides a brief, feedback, transcript, postmortem |
| **targeted** | User names the skill + change directly. Skip discovery. |
| **usage** | Review recent runs of the named skill, identify gaps |

Default when invoked mid-conversation with substantive recent activity: **from-chat**.

### Step 2 — Extract learning(s)

For from-chat / from-dump / usage: look for change-worthy signals (full taxonomy in `references/update-change-types.md`):

- **Corrections** — "no, don't do that anymore"
- **Validations** — "yes that worked — bake it in"
- **New patterns** — user just did an undocumented workflow; encode it
- **Voice / tone updates** — like the spoken-aloud rule for slide-deck
- **Tool changes** — switched defaults
- **Architectural decisions** — naming conventions, file layout, frontmatter
- **Gaps** — something the skill should have handled but didn't

Output: a clear list of *N learnings*, each phrased as a single change.

For **targeted**: skip extraction — user already named the change.

### Step 3 — Identify affected skills

For each learning, search across all SKILL.md + references/ in the current repo (and optionally all sibling repos from your `repos.yaml` with `--cross-repo`):

```bash
grep -rln "<key terms>" ~/code/makerskills/skills/ --include="*.md"

# Across all sibling repos (list yours in $MAKERSKILLS_CONFIG/skillify/repos.yaml):
config="${MAKERSKILLS_CONFIG:-$HOME/.config/makerskills}/skillify/repos.yaml"
for raw in $(yq -r '.repos[].path' "$config"); do
  repo="${raw/#\~/$HOME}"  # expand leading ~ to $HOME so grep resolves the real path
  grep -rln "<terms>" "$repo/skills/" --include="*.md" 2>/dev/null
done
```

Classify by confidence:

| Confidence | What | Action |
|---|---|---|
| **High** | Direct keyword match + clearly same topic | Propose change |
| **Medium** | Adjacent topic — rule *might* apply | Surface for explicit approval |
| **Low** | Tangential — rule could be stretched | Mention but don't propose |

See `references/update-propagation.md` for the cross-skill propagation playbook.

### Step 4 — Memory-vs-skill check

For each learning: **is this skill-specific or a broader principle?**

| Type | Where it goes |
|---|---|
| Skill-specific rule | Edit the SKILL.md / references file directly |
| Cross-cutting principle | `~/.claude/memory/feedback_<topic>.md` |
| Both | Write the memory file AND update the skill(s) that immediately apply |

Example: *"links go in first comments, not body"* → applies to `jab-hook` AND is a broader social principle → both update jab-hook AND save `feedback_social_link_placement.md`.

Offer the memory write explicitly: *"This looks like a principle, not just a skill rule. Save to memory as `feedback_<slug>.md`?"*

### Step 5 — Propose diffs per file

For each affected file, show change as before/after or unified diff:

```markdown
### `skills/<skill>/SKILL.md` — proposed change

**Before** (lines NN–NN):
> <existing text>

**After**:
> <new text>

**Why**: <one-line rationale>

**Version bump**: 0.2.0 → 0.2.1 (PATCH — clarification)

**Approve / edit / skip?**
```

Per-file approval. Don't batch — small changes are easy to OK; bundling forces all-or-nothing.

See `references/update-versioning.md` for semver rules.

### Step 6 — Apply approved changes

1. Use `Edit` to apply the exact change
2. Bump `metadata.version` per the suggested level
3. If the change involves a rename, follow the cross-reference update pattern (grep all files, update all references)

Batch multiple file changes within one skill into a single commit.

### Step 7 — Commit + push

Group by skill. Examples:

- One-skill update: `"slide-deck: emphasize spoken-aloud voice (write for the ear, not the page)"`
- Multi-skill propagation: `"jab-hook, marketingskills:social: link placement (no inline URLs)"`
- Cross-repo: one commit per repo. Don't atomic-commit across repos.

### Step 8 — Report

Show:
- Learnings extracted
- Skill(s) updated (with version bumps)
- Memory files written
- Whether `compound-engineering:heal-skill` would be a useful QA pass
- Anything flagged but skipped

### When NOT to use UPDATE mode

Don't add ceremony to surgical edits. If the user says "add this one bullet to X.md," just Edit. UPDATE mode earns its keep when:

1. **Multiple skills are affected** by one learning (cross-skill propagation)
2. **Bulk extraction** from a long session
3. **Memory-vs-skill decision** is unclear (need explicit triage)
4. **Version discipline matters** (about to commit and want sane semver)

For one-line updates with no cross-skill implications: just Edit.

---

## Composes with

- **`watch-video`** — load-bearing for CREATE / from-video. Visual-mode output (transcript + key visual moments + summary) is the input for skill synthesis. Always call in `visual` mode for process recordings — UI state matters as much as words.
- **`second-brain`** — optionally capture source video/dump as `raw/call-<slug>.md` or `raw/note-<slug>.md` so the source artifact lives alongside the skill it produced.
- **`toolify`** — sibling in the `-ify` trifecta. Use `toolify` when the goal is adding an integration/MCP/API, not authoring a skill.
- **`loopify`** — sibling in the `-ify` trifecta. Use `loopify` for agent-loop setup rather than a skill.
- **`compound-engineering:create-agent-skill`** (agent) — call for format and best-practices expertise
- **`compound-engineering:skill-creator`** (skill) — deeper best-practices reference
- **`compound-engineering:heal-skill`** (skill) — QA pass after any mode

## Notes on quality

- **Cite the source.** Whether chat, video, dump, external URL, or user-named learning — the SKILL.md body should reference where each decision came from. Makes revising easier.
- **Don't over-engineer v0.1.** Ship a minimal SKILL.md + 1–2 references files. Iterate after first use. Most generated skills are over-scoped.
- **Verb-noun naming** where possible (matches `watch-video`, `read-book`, `paste`). Single-word noun names are fine for distinctive concepts (`decide`, `pm`, `paste`, `skillify`).
- **Always reference Anthropic's official guidance** for the schema — don't invent format conventions.
- **Attribution is non-negotiable** for ADAPT mode. Every adapted skill ships with `references/attribution.md`.
- **License is a hard gate.** Don't proceed on GPL/proprietary without explicit approval.
- **Per-file approval in UPDATE mode.** Small changes are easy to OK; bundling forces all-or-nothing.
