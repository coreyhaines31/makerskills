# Prompt templates

Castmates run in the same working directory as the host. They can read files and run git themselves. Point them to files by path instead of pasting the contents; inline only a short snippet that frames the question, like an error message or a function signature.

## Delegate (one castmate does a job)

```markdown
# Task

[One paragraph: what to produce, and why.]

## Scope
- Files to read first: [paths]
- Files you may change: [paths or "none — answer only"]
- Out of scope: [what to leave alone]

## Done means
- [Concrete acceptance check, e.g. "rspec spec/models/user_spec.rb passes"]
- [Output shape, e.g. "reply with a summary of changes and anything you were unsure about"]

## Constraints
- Follow the existing patterns in [path].
- Don't add dependencies, rename public APIs, or reformat unrelated code.
- If something blocks you, stop and say what. Don't guess.
```

## Review (one or more castmates give an independent opinion)

```markdown
# Review request

## Question
[The user's question, in their words.]

## Context
- Files: [paths]
- Recent changes: [one line; tell them to run `git diff <base>` themselves]
- What we already believe: [omit for a blind review]

## Instructions
You are giving an independent review. Be critical and direct; don't hedge.
- Read the referenced files before answering.
- Identify risks, tradeoffs, and blind spots, and suggest a better approach if you see one.
- For each finding, give the file path and function, the evidence, the impact, and the smallest fix.
- Skip style nits unless they hide a bug.
- Use clear headings.

[Paste a preset from presets/ here for a focused hunt.]
```

## Round 2+ addendum (rounds mode)

Append this to the base prompt, followed by the prior outputs inlined under one heading per castmate and round. Keep only the most recent 8 outputs, and cut each to about 1,500 words if needed.

```markdown
## Prior round outputs

Use these to improve quality, not just to avoid duplicates.
- Don't repeat a finding unless you add meaningful new evidence.
- Challenge prior findings: try to invalidate, narrow, or refine the high-impact claims.
- Treat prior findings as leads: follow adjacent code paths, shared utilities, and similar patterns.
- Label any overlapping finding confirmed, refined, invalidated, or duplicate, and say what is new.

### Round 1: codex-sol-high
[output]

### Round 1: fable-high
[output]
```
