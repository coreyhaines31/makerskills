# Cross-skill propagation

The unique value of `update-skill`. A learning often applies to multiple skills — surface all of them so the user can approve per file.

## Why this matters

Examples from this session where a single learning crossed skills:

| Learning | Affected skills |
|---|---|
| Link placement rule (no URLs in body) | `jab-hook` + memory `feedback_social_link_placement.md` (which also implicitly applies to `cf-skills:x-li` and `marketing-skills:social`) |
| Verb-noun naming convention | `watch-video`, `read-book`, `create-skill`, `adapt-skill`, `update-skill` (rename pass across multiple skills) |
| Anti-AI-slop banned phrases | `slide-deck`, `jab-hook` (both write content; both should ban "dive deep," "leverage," etc.) |
| Spoken-aloud voice rule | `slide-deck` (load-bearing); `jab-hook` partial relevance (social IS read silently usually, but voice still applies) |

Without propagation, these rules drift — one skill knows about it, others don't. Subtle inconsistency creeps in.

## Discovery: how to find affected skills

For each learning, do three passes:

### Pass 1: Keyword search

Grep for terms that signal the topic. Cast a wide net.

```bash
# Example: link placement learning
grep -rln "URL\|link\|outbound\|first comment" ~/code/makerskills/skills/ --include="*.md"

# Across all sibling repos:
for repo in makerskills cf-skills marketingskills nonfictionskills fictionskills youtubeskills; do
  if [ -d ~/code/$repo/skills/ ]; then
    grep -rln "URL\|link\|outbound\|first comment" ~/code/$repo/skills/ --include="*.md" 2>/dev/null
  fi
done
```

### Pass 2: Semantic match (manual)

For each grep hit, read the matching section and ask: *is this rule actually applicable here, or is the keyword match coincidental?*

- **Direct match** — same topic + same activity (e.g., link rule in a social drafting skill): high confidence
- **Adjacent match** — same topic, different activity (link rule mentioned in a research skill that cites URLs): medium confidence
- **Coincidental match** — keyword present but unrelated context: skip

### Pass 3: Adjacent-skill scan (no grep)

Some learnings won't have keyword matches but logically apply. Manually scan the list of all skills and ask: *does this rule apply here even if the keyword isn't present?*

Example: a "voice should be spoken aloud" rule won't grep-match in `pm` (project management skill — no voice content), but it applies in any skill that produces user-facing text (`slide-deck`, `jab-hook`, `read-book` summaries, `create-skill` output).

Use the skill's *output type* as the heuristic:
- **Writes user-facing text** (drafts posts, slides, summaries): voice rules apply
- **Generates structured data** (boards, archives, schemas): voice rules usually don't apply
- **Wraps an external tool** (yt-dlp, ffmpeg, Playwright): tool rules apply

## Output: confidence-tagged candidate list

Present to the user before proposing any diffs:

```markdown
## Learning: <one-line statement>

### High-confidence candidates (propose diff)
- `<skill1>` — at `<file>:<line>` — direct match, same topic + activity
- `<skill2>` — at `<file>:<line>` — direct match

### Medium-confidence candidates (ask before proposing)
- `<skill3>` — at `<file>:<line>` — adjacent topic; rule might apply with adjustment

### Low-confidence (mentioned for awareness, no proposal)
- `<skill4>` — keyword present but in unrelated context

### Memory candidate (cross-cutting principle?)
- Yes / no. If yes, suggested path: `~/.claude/memory/feedback_<slug>.md`

**Proceed with high-confidence diffs? Approve / edit / skip each.**
```

Per-candidate approval (not batch) — small changes are easy to OK individually; bundled changes force all-or-nothing decisions.

## Scope control

Default: search **only the current repo**. Most learnings are repo-local.

Add `--cross-repo` flag when:
- The learning is clearly meta (naming convention, file structure, frontmatter)
- The skills span multiple repos (e.g., voice rule that applies to social skills in `makerskills:jab-hook`, `cf-skills:x-li`, `marketingskills:social`)
- the user explicitly asks ("apply this to all my skills")

Cross-repo propagation: produce one commit per repo. Don't try to atomic-commit across repo boundaries.

## When to skip a candidate

Sometimes a candidate keyword-matches but applying the rule would be wrong. Reasons to skip:
- The skill's context is genuinely different (e.g., `read-book` "summary" mode wants written voice, not spoken)
- The rule has a documented exception (e.g., reading-first density mode in `slide-deck` exempts voice rules)
- Applying it would over-constrain a deliberately flexible area

When skipping, note in the report: *"Considered but skipped: `<skill>` because `<reason>`."* This makes the decision auditable later.

## Frequency heuristic

If the same learning lands in update proposals 3+ times for related skills, it's probably a **principle, not a rule**. Promote to `feedback_*.md` in memory and reference from each affected skill rather than copy-pasting the same text 5 places.
