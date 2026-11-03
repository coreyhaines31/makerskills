# Casting: which castmate for which job

These are default heuristics. The user's own rules in `${MAKERSKILLS_CONFIG:-$HOME/.config/makerskills}/castmate/casting.local.md` come first, because they are based on what the user has actually seen. Model strengths change with every release, so treat these defaults as a starting point to replace.

## Principles

1. **Diversity beats ranking for opinions.** A second opinion is worth most from a different model family than the one that wrote the work. If the host is Claude, cast a Codex or Gemini castmate first, and the reverse for other hosts.
2. **Match cost to stakes.** Use a fast tier (`haiku`, `codex-luna`, `gemini-flash`) for mechanical jobs: summarize a log, rename across files, draft boilerplate, answer a lookup. Use a top tier with high effort (`fable-high`, `codex-sol-high`) for architecture, security, or anything that is costly to get wrong.
3. **One writer, many readers.** Hand a write job to a single castmate. Fan out only read-only work.
4. **Prefer enforced read-only for reviews.** `castmate.py list` shows the read-only level for each castmate. A `best-effort` castmate can still edit files, so say so before you use it on a review.
5. **Unverified adapters fail loudly at first.** Run `castmate.py test <name>` once before relying on one.

## Starting defaults by job

| Job | Default cast | Why |
|---|---|---|
| Second opinion on a plan or diff | 1–2 castmates outside the host's model family, top tier | Independent blind spots |
| Broad bug or security hunt | `review` or `wide` group, 2–3 rounds with a preset | Each round builds on the last |
| Delegate a scoped coding task | One castmate with `--write`, top tier | One writer; the host reviews the diff |
| Mechanical, bulk, or cheap task | One fast-tier castmate | Saves the host's context and budget |
| Tie-breaker when the host and user disagree | One castmate that hasn't seen the argument, given only the facts | Unanchored read |
| Research a library or API | A castmate with web search (claude, codex, gemini) | Reads current docs |

## Recording what works

When a castmate does notably well or badly on a kind of job, offer to append a line to `casting.local.md`:

```markdown
- Migrations in Rails apps → codex-sol-high (clean, ran the tests itself). 2026-11-03
- Long-doc summarizing → haiku is enough; fable was overkill. 2026-11-03
```

Keep each line dated. Prefer the newer line when two disagree.
