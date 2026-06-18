---
name: create-skill
description: When Corey wants to create a new skill in one of his skill repos (makerskills, cf-skills, marketingskills, nonfictionskills, fictionskills, youtubeskills). Three input modes — from-chat (default when invoked mid-conversation; extract the skill from the workflow we've been discussing), from-dump (Corey pastes a brief / transcript / notes / past chat export), from-scratch (a fresh idea with no source material). Scaffolds SKILL.md frontmatter + body + references/ subdirectory, updates the README skill table, commits, pushes. Defers to Anthropic's skill creator skills (compound-engineering:create-agent-skill agent, compound-engineering:skill-creator skill) and the anthropics/skills GitHub repo for deep schema and best-practices guidance — this skill orchestrates Corey's specific workflow on top of those. Triggers on "/create-skill," "create a skill called X," "make this a skill," "skill from this chat," "skill from this brief," "skill from this dump," "extract a skill from what we've been doing," "let's make this a skill," "scaffold a new skill," "bootstrap a skill."
metadata:
  version: 0.2.0
---

# /create-skill — Turn a workflow, brief, or chat into a skill

Replaces the prior `add-skill`. Primary use case: you've been iterating on a workflow in conversation (like this entire session) and now want to formalize it. Secondary: scaffold from a brief / data dump / fresh idea.

## Step 1 — Pick input mode

| Invocation | Mode | What it means |
|---|---|---|
| `/create-skill` (mid-conversation) | **from-chat** (default) | Extract the skill from the workflow we've been discussing in this session. The most common case. |
| `/create-skill from-dump` + pasted content | **from-dump** | User provides a brief, prior conversation transcript, exported chat, or notes. Skill structures it. |
| `/create-skill from-scratch <name>` | **from-scratch** | Fresh idea with no source material — interactive Q&A to flesh it out (the prior `add-skill` behavior). |

If unspecified and there's substantive recent conversation, default to **from-chat**. If the conversation is empty/short, ask which mode.

## Step 2 — Defer to Anthropic / community guidance for the schema

Don't reinvent SKILL.md format rules. For canonical guidance on frontmatter, description-writing, references/ structure, and skill best practices, this skill leans on:

- **`compound-engineering:create-agent-skill`** (agent) — expert guidance for creating + editing Claude Code skills
- **`compound-engineering:skill-creator`** (skill) — deeper guide for effective skills
- **`compound-engineering:heal-skill`** (skill) — for fixing existing skills
- **[anthropics/skills](https://github.com/anthropics/skills)** — official Anthropic examples
- **[agentskills.io](https://agentskills.io)** — the open Agent Skills specification

Call those skills directly (`Skill({skill: "compound-engineering:create-agent-skill", ...})`) when in doubt about format, or to pressure-test a draft SKILL.md.

This skill (`create-skill`) is the **orchestrator** for Corey's specific workflow: which repo, which conventions, which cross-references. The format expertise lives in the references above.

## Step 3 — Pick target repo

Ask which sibling plugin this belongs in:

| Repo | What lives here | Path |
|---|---|---|
| **makerskills** | Personal cross-cutting operator work | `~/code/makerskills/` |
| **cf-skills** | Conversion Factory agency operations | `~/code/cf-skills/` |
| **marketingskills** | Generic marketing tactics (public) | `~/code/marketingskills/` |
| **nonfictionskills** | Writing a nonfiction book | `~/code/nonfictionskills/` |
| **fictionskills** | Writing fiction | `~/code/fictionskills/` |
| **youtubeskills** | Making YouTube videos | `~/code/youtubeskills/` |

Infer if obvious (a skill about pricing strategy → marketingskills; a skill about Riverside transcript prep → youtubeskills). Ask if ambiguous.

## Step 4 — Synthesize per mode

### from-chat

1. **Read backward through this conversation.** Look for: a workflow Corey did multiple times, a process he keeps explaining, opinions he restated, decisions he made about tooling/voice/output formats.
2. **Identify the load-bearing pieces:**
   - What's the trigger? (When does Corey want this?)
   - What are the steps?
   - What references / sources matter?
   - What does success look like (output format)?
   - What's the voice / convention?
3. **Surface what's *not* in the chat** — gaps that need clarification before scaffolding. Ask 2–4 tight questions before writing.
4. **Draft the SKILL.md from the synthesis.** Cite chat moments inline as you go ("Per your 2026-06-17 message about X…") so Corey can verify.

### from-dump

1. **Parse the dump** — could be a Notion page, a Slack thread, a Loom transcript, a brief from a teammate, an exported ChatGPT conversation.
2. **Apply the same synthesis logic** as from-chat — what's the trigger, steps, references, output, voice.
3. **Cite the dump** in the SKILL.md (where in the dump did each rule come from).

### from-scratch

Interactive Q&A — the prior `add-skill` flow:
1. **Name** — kebab-case, verb-noun preferred (matches `watch-video`, `read-book`, `add-skill`)
2. **One-line purpose**
3. **Trigger phrases**
4. **Initial reference files?**
5. **Composes with which other skills?**

## Step 5 — Generate the frontmatter

```yaml
---
name: <kebab-case>
description: <rich, trigger-rich, ~2–4 sentences. Lead with "When Corey wants to..." Include 4–8 trigger phrases in quotes. Differentiate from adjacent skills if relevant.>
metadata:
  version: 0.1.0
---
```

**Description rules** (load-bearing — Claude routes by description match):
- Lead with the use case ("When Corey wants to X…")
- Include explicit trigger phrases the user might say
- Differentiate from sibling skills if there's overlap
- Mention key references the skill loads
- Keep under ~500 characters

For deeper description-writing guidance, consult `compound-engineering:skill-creator`.

## Step 6 — Scaffold the directory

```
<target-repo>/skills/<name>/
├── SKILL.md            # the synthesized skill
└── references/         # populate based on what the synthesis surfaced
    └── ...
```

Body follows the pattern of existing skills (`pm`, `decide`, `second-brain`, etc.):
- `# /<name> — <one-line purpose>`
- Numbered `## Step N — <phase>` sections
- Composes-with cross-references
- Quality notes at the end

## Step 7 — Update README, commit, push

Append to the target repo's README skill table:

```markdown
| [`<name>`](./skills/<name>/SKILL.md) | <one-line purpose> |
```

Then:

```bash
cd <target-repo> && git add -A && git commit -m "Add <name> skill: <one-line purpose>" && git push
```

Report:
- New skill path
- Commit hash
- Reminder: `/plugin install` or symlink may need a refresh

## Step 8 — Offer follow-ups

After scaffolding:
- *"Want to flesh out a specific Step in the SKILL.md now, or come back to it?"*
- *"Want me to run it through `compound-engineering:heal-skill` for a quality pass?"*
- *"Should this skill compose with [adjacent skill]? Want me to add the cross-reference?"*

## Composes with

- `adapt-skill` — for porting an EXTERNAL skill into your namespace (different job — that's adapting, this is creating). If Corey says "let's borrow that skill from gstack," use `adapt-skill`. If he says "let's encode what we just did," use this.
- `compound-engineering:create-agent-skill` (agent) — call into this for format and best-practices expertise
- `compound-engineering:skill-creator` (skill) — same
- `compound-engineering:heal-skill` (skill) — for QA pass on the generated skill

## Notes on quality

- **Cite the source.** Whether it's chat, dump, or interactive Q&A — the SKILL.md body should reference where each decision came from. This makes it easy to revise later.
- **Don't over-engineer v0.1.** Ship a minimal SKILL.md + 1–2 references files. Iterate after Corey uses it once. Most generated skills are over-scoped.
- **Verb-noun naming** when possible (matches `watch-video`, `read-book`, `add-skill`, etc.). Single-word noun names are fine for distinctive concepts (`decide`, `pm`, `paste`).
- **Always reference Anthropic's official guidance** for the schema — don't invent format conventions.
