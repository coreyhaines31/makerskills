---
name: ingest
description: When you paste raw human input — a call transcript (Grain, Zoom, Granola, Fathom), a text or email from a client/partner/friend, a voice-memo dump, or meeting notes — and want it converted into structured work. Extracts decisions, action items (yours vs theirs), bugs/feature requests, and facts worth keeping; files GitHub issues in the right repo, captures to the second-brain vault, and drafts (never sends) the reply. Triggers on "/ingest", "ingest this", "here's my call with X," "here's the transcript," "this is from [person]," "[person] asked me this," "from [person]:", a pasted transcript with speaker labels, or a forwarded client message that clearly expects processing. Person→project routing lives in a private config; unknown senders get asked about once, then remembered.
metadata:
  version: 0.1.0
---

# /ingest — Raw human input → structured work

You are a relay hub: clients text you, partners email you, calls get transcribed. Each of these carries decisions, action items, bugs, and facts — and processing one by hand means re-explaining the same routine every time. This skill is that routine, written down.

**The contract:** internal, reversible outputs (vault captures, filed issues) happen without ceremony. Outward-facing outputs (replies) are always **drafted, never sent**.

## Files

| Path | What |
|---|---|
| `${MAKERSKILLS_CONFIG:-$HOME/.config/makerskills}/ingest/people.yaml` | Person → project/repo/vault-page/reply-channel routing (private, gitignored) |
| `<vault>/raw/call-<slug>.md` / `<vault>/raw/message-<slug>.md` | Captures, in second-brain's schema |
| `references/people.yaml.example` | Config schema with a worked example |

`<vault>` is `${SECOND_BRAIN_VAULT:-$HOME/Documents/SecondBrain}`.

## Step 0 — Get the input and classify it

In order: content in the prompt → clipboard (`pbpaste`) → ask.

Classify by shape, not by what the user called it:

| Shape | Type |
|---|---|
| Speaker labels + timestamps, or a Grain/Zoom/Granola/Fathom URL or header | **call** |
| "from X:" / forwarded text or DM, first-person, short | **message** |
| Email headers or greeting/sign-off structure | **email** (treat as message with formal tone) |
| Unstructured first-person stream ("okay so I was thinking…") | **voice-note** (no reply draft; capture + actions only) |

Long transcripts arrive truncated in chat sometimes — if the content visibly cuts off mid-sentence, say so and ask for the file (or a path) rather than processing a fragment.

## Step 1 — Identify who and which project

Read `people.yaml`. Match participants/senders against `name` and `aliases`.

- **Matched** → you now have the repo, vault page, reply channel, and tone notes. Say which routing you're using in one line ("Routing: Jane → acme-app").
- **Unmatched** → ask once: "Who is this and what project does it belong to?" Then offer to append them to `people.yaml` so the question never repeats. If the user declines to add them, process the input with explicit destinations instead of routed defaults.
- **Multiple projects in one call** (common on partner calls) → split extraction by project; route each piece separately.

## Step 2 — Extract

Read the whole input first. Then pull out, with a short verbatim quote or paraphrase anchoring each:

1. **Decisions made** — anything settled, including "we're NOT doing X."
2. **Action items — mine** — things the user owes someone. Include any stated deadline.
3. **Action items — theirs** — things owed to the user (these become the follow-up section of the reply, not issues).
4. **Bugs & feature requests** — anything that should become a GitHub issue. One issue per item, never a grab-bag.
5. **Questions to answer** — asked but unanswered in the input.
6. **Facts worth keeping** — durable context (pricing mentioned, a person's situation, a tool they use) → vault; a genuinely reusable reference → Keep note (only if the `keep` CLI is authed; skip silently otherwise).

**Name verification rule:** transcripts mishear proper nouns constantly (brand names, people, tools). Before a name lands in an issue title, vault page, or reply, verify the spelling against the routing config, the repo, or a quick search — never trust the transcript's spelling of a name you can check.

## Step 3 — Show the routing plan

One compact table before acting:

| # | Item | Destination |
|---|---|---|
| 1 | "Bulk-export button on the reports page" | Issue → `myorg/acme-app` |
| 2 | Decision: monthly billing default | vault `Projects/Acme.md` |
| 3 | Reply to Jane | draft below |

Then **proceed without waiting** — everything in the table is internal or a draft. Pause for confirmation only when routing is ambiguous (two plausible repos, an unmatched person) or the input includes something sensitive (credentials, legal/financial commitments).

## Step 4 — Execute

**Issues** — search for duplicates first (`gh issue list --search`), then file with `gh issue create` in the mapped repo. Title = imperative summary; body = context quote from the source, what was asked, and who asked. Apply `issue_labels` from config if set. Never assign anyone but the user.

**Vault capture** — one file per ingest, second-brain raw schema:

```markdown
# message-jane-bulk-export (2026-09-04)
source: text message from Jane
project: Acme App

## Summary
…

## Decisions
…

## Action items
- [ ] mine: …
- [ ] theirs: Jane to …

## Filed
- myorg/acme-app#123 — Bulk-export button on the reports page
```

Slug: `call-` or `message-` + person + topic. Follow the vault's auto-commit convention (semantic commit per session).

**Todos** — action items of "mine" also land wherever the person's `vault_page` tracks tasks, if one is configured.

**Reply draft** — in the user's voice for that channel (config `tone` + channel norms: text = brief and casual; email = fuller). Structure when it fits: acknowledge → what I'm doing about it → what I need from you → when they'll hear back. End with the draft in a paste-ready block (compose with `/paste` rules for the channel — e.g. no URLs in an X post body). **Never send it.**

## Step 5 — Report

Close with a compact recap: TLDR of the input (2–3 sentences), decisions, both action-item lists, links to filed issues, the vault file path, and the reply draft. This recap is the deliverable — someone who never saw the input should understand what happened and what's next.

## Composes with

- `second-brain` — captures land in its `raw/` schema for later compile
- `paste` — channel formatting for the reply draft
- `deep-research` — when an extracted question needs real research before it's answerable
- `pm` — when a call produces enough work to deserve a project card, not just issues

## Notes on quality

- The most common failure is **flattening**: summarizing the input instead of extracting work from it. The test: could the user act on your output without rereading the source?
- Second most common: **issue grab-bags**. "Improvements from call with Jane" is not an issue. One item, one issue, one clear title.
- "Theirs" action items are as valuable as "mine" — they're the follow-up ledger. Don't drop them because no tool call captures them.
- A voice-note ingest with zero action items is fine: capture it, say so, stop. Not every input contains work.
