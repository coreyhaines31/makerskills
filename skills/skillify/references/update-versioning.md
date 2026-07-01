# Versioning — semver for skills

Per-skill `metadata.version` follows semantic versioning. Bumps are small signals, but they matter for "what changed since I last looked at this skill."

## The rules

| Bump | When | Example |
|---|---|---|
| **PATCH** (0.1.0 → 0.1.1) | Clarification, typo fix, minor wording improvement, reference doc update, error-message tweak. Behavior unchanged. | Tightening a description, fixing a broken link, rewording a step for clarity. |
| **MINOR** (0.1.0 → 0.2.0) | New capability — new mode, new reference file, new option, expanded scope. Backward-compatible. | Adding `from-chat` mode to `create-skill`. Adding density modes to `slide-deck`. New `--with-replies` flag on `social-fetch`. |
| **MAJOR** (0.1.0 → 1.0.0) | Breaking change — rename, removed mode, incompatible output format change, removed reference file callers rely on. | Renaming `add-skill` → `create-skill`. Removing the `transcript` mode from `watch-video`. Renaming output JSON keys in `social-fetch`. |

## Pre-1.0 nuance

Most skills start at `0.1.0`. While in 0.x, breaking changes can bump MINOR instead of MAJOR (e.g., `0.1.0` → `0.2.0` for a rename, as we did for `jab-hook`). This signals "still iterating, expect changes." Move to `1.0.0` when:
- The skill has been used successfully ~10+ times
- The interface is stable
- the user explicitly says "lock it in"

After `1.0.0`, the standard rules apply strictly.

## What NOT to bump

- **Rewording the same idea** without changing behavior → don't bump (just commit)
- **Adding a comment** → don't bump
- **Fixing a typo in a non-load-bearing section** → don't bump (or PATCH if you must)

Bumps should be meaningful. If every commit bumps, the version stops carrying information.

## Multi-file changes

When an update touches multiple files within the same skill (SKILL.md + a references/ file), bump the version once for the skill — not per file.

When an update spans multiple skills (cross-skill propagation), bump each affected skill independently per its own change scope. Example:
- Slide-deck adds a new voice rule (MINOR for slide-deck)
- Jab-hook adopts the same voice rule (PATCH for jab-hook — clarification, not new behavior)

## Where the version lives

```yaml
---
name: <skill-name>
description: <...>
metadata:
  version: 0.2.0          # ← here
---
```

If `metadata.version` is missing, treat as `0.1.0` and add it explicitly during the next update.

## What to put in the commit message

Mention the bump:

```
slide-deck: add ppt + export modes (0.1.0 → 0.2.0 — MINOR)

<details>
```

This makes the changelog grep-able:

```bash
git log --oneline | grep -E "MAJOR|MINOR|PATCH"
```

## Bumping versions on rename

Cross-skill renames (e.g., `video-watch` → `watch-video`, `add-skill` → `create-skill`) are MAJOR by definition — they break callers. Bump accordingly.

For internal-only renames (a section heading inside SKILL.md, never referenced externally), no bump needed.

## When you're not sure

Default to PATCH. It's better to undersell a change than oversell.
