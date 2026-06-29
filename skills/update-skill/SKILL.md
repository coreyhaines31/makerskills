---
name: update-skill
description: When you want to improve / iterate on an existing skill based on a learning from this conversation, a feedback dump, or an explicit targeted change. Cross-skill propagation is the unique value — a single learning often applies to multiple existing skills (e.g., a voice rule for slide-deck might also fit jab-hook), and this skill surfaces all affected files for approval. Four modes — from-chat (default mid-conversation; scan for learnings), from-dump (paste feedback / brief), targeted (you name the skill + change directly), usage (review recent runs and suggest improvements). Bumps semver per skill, commits per-skill or grouped depending on cohesion. Offers to save broader principles to memory as feedback_*.md instead of (or in addition to) skill updates. Triggers on "/update-skill," "update X skill," "apply this to the relevant skills," "propagate this learning," "what should I update based on this chat," "improve [skill]," "fix [skill]," "iterate on [skill]."
metadata:
  version: 0.1.0
---

# /update-skill — Improve existing skills from learnings

Third in the meta-skill trio with `create-skill` (new skills) and `adapt-skill` (external → yours).

Decision tree:
- **Net-new skill** → `create-skill`
- **External skill to port** → `adapt-skill`
- **Existing skill needs an improvement** → `update-skill` (this one)

## Step 1 — Pick input mode

| Invocation | Mode | What it means |
|---|---|---|
| `/update-skill` (mid-conversation) | **from-chat** (default) | Scan recent conversation for learnings, identify affected skill(s) |
| `/update-skill from-dump` + pasted content | **from-dump** | Corey provides a brief, feedback, transcript, postmortem |
| `/update-skill <skill> <change>` | **targeted** | Corey names the skill + the change directly. Skip discovery. |
| `/update-skill usage <skill>` | **usage** | Review recent runs of the named skill, identify gaps / improvements |

Default when invoked mid-conversation with substantive recent activity: **from-chat**.

## Step 2 — Extract the learning(s)

For `from-chat` / `from-dump` / `usage`:

Look for change-worthy signals (full taxonomy in `references/change-types.md`):

- **Corrections** — "no, don't do that anymore" / "this needs to change"
- **Validations** — "yes that worked — let's bake it in"
- **New patterns** — Corey just used a workflow not documented; encode it
- **Voice / tone updates** — like the spoken-aloud rule for slide-deck
- **Tool changes** — switched defaults (e.g., MLX-Whisper as default)
- **Architectural decisions** — naming conventions, file layout, frontmatter
- **Gaps** — something the skill should have handled but didn't

Output: a clear list of *N learnings*, each phrased as a single change ("voice should emphasize spoken-aloud," not "voice").

For `targeted`: skip extraction — Corey already named the change.

## Step 3 — Identify affected skills

For each learning, search across all SKILL.md + references/ files in the current repo (and optionally across all 6 sibling repos with `--cross-repo`):

```bash
# In makerskills:
grep -rln "<key terms from learning>" ~/code/makerskills/skills/ --include="*.md"

# Across all sibling repos:
for repo in makerskills cf-skills marketingskills nonfictionskills fictionskills youtubeskills; do
  grep -rln "<terms>" ~/code/$repo/skills/ --include="*.md" 2>/dev/null
done
```

Classify candidates by confidence:

| Confidence | What | Action |
|---|---|---|
| **High** | Direct keyword match + clearly the same topic | Propose change |
| **Medium** | Adjacent topic — rule might apply | Surface to Corey for explicit approval |
| **Low** | Tangential — rule could be stretched | Mention but don't propose |

Output: per-learning, the list of affected skills with confidence.

See `references/propagation.md` for the cross-skill propagation playbook.

## Step 4 — Memory-vs-skill check

For each learning, ask: **is this skill-specific or a broader principle?**

| Type | Where it goes |
|---|---|
| Skill-specific rule | Edit the SKILL.md / references file directly |
| Cross-cutting principle that applies beyond the skills | `~/.claude/projects/-Users-coreyhaines/memory/feedback_<topic>.md` |
| Both | Both — write the memory file AND update the skill(s) that immediately apply |

Example: "links go in first comments, not body" → applies to `jab-hook` AND is a broader social-content principle → both update jab-hook AND save `feedback_social_link_placement.md` (we already did this earlier in the session).

Offer the memory write explicitly: *"This looks like a principle, not just a skill rule. Want me to also save it to memory as `feedback_<slug>.md`?"*

## Step 5 — Propose diffs per file

For each affected file, show the change as a clear before/after table OR a unified diff:

```markdown
### `skills/<skill>/SKILL.md` — proposed change

**Before** (lines NN–NN):
> <existing text>

**After**:
> <new text>

**Why**: <one-line rationale tying to the source learning>

**Version bump suggestion**: 0.2.0 → 0.2.1 (PATCH — clarification)

**Approve / edit / skip?**
```

Per-file approval. Don't batch — small changes are easy to OK; bundling forces all-or-nothing.

See `references/versioning.md` for the semver rules.

## Step 6 — Apply approved changes

For each approved diff:
1. Use the `Edit` tool to apply the exact change
2. Bump `metadata.version` per the suggested level
3. If the change involves a rename, follow the cross-reference update pattern from prior renames (grep all files, update all references)

If multiple files in the same skill change, batch them — single commit per skill with a descriptive message.

## Step 7 — Commit + push

Group commits by skill. Example commit messages:

- One-skill update: `"slide-deck: emphasize spoken-aloud voice (write for the ear, not the page)"`
- Multi-skill propagation: `"jab-hook, marketing-skills:social: link placement (no inline URLs)"`
- Cross-repo: keep one commit per repo. Don't try to atomic-commit across repos.

After all commits, push.

## Step 8 — Report

Show Corey:
- What learnings were extracted
- Which skill(s) were updated (with version bumps)
- Whether any memory files were written
- Whether `compound-engineering:heal-skill` would be a useful QA pass
- Anything that was *flagged but skipped* (so Corey can revisit)

## Composes with

- `create-skill` — sibling. Use that for NEW skills.
- `adapt-skill` — sibling. Use that for porting EXTERNAL skills.
- `compound-engineering:heal-skill` — optional QA pass after updates. Recommend after large updates.
- `compound-engineering:create-agent-skill` — call into for format expertise if a proposed change touches frontmatter conventions.
- Memory `feedback_*.md` — when learnings are broader than one skill.

## When NOT to use this skill

Don't add ceremony to surgical edits. If Corey says "add this one bullet to X.md," just Edit. The skill earns its keep when:

1. **Multiple skills are affected** by one learning (cross-skill propagation)
2. **Bulk extraction** from a long session ("what did we learn in the last 3 hours that should propagate?")
3. **Memory-vs-skill decision** is unclear (need the explicit triage step)
4. **Version discipline matters** (you're about to commit and want a sane semver bump)

For one-line updates with no cross-skill implications: just Edit. This skill exists for the 10–20% of updates where the discipline pays off, not the 80% that are surgical.
