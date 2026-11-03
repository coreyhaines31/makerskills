---
name: castmate
description: "When you want to pull in the right AI model for the right job: hand a task to another agent CLI (Codex, Claude, Gemini, Amp, OpenCode, Cursor, Kiro, Antigravity), or send one prompt to several at once for independent opinions, then synthesize. Delegate mode gives one castmate the job, optionally with write access ('have codex write the migration'). Fan-out mode runs read-only reviews in parallel. Rounds mode lets castmates build on and challenge each other's findings. Calls the official CLIs you already have installed and logged in (Gemini CLI needs an API key on personal accounts); no MCP. Triggers on '/castmate,' 'ask codex,' 'have gemini do this,' 'get a second opinion,' 'what would other models say,' 'fan this out,' 'cross-check this with another model,' 'delegate this to codex.' Advisor personas for founder questions go to maker-council. Personal models, casting rules, and run outputs live in ~/.config/makerskills/castmate/."
metadata:
  version: 0.1.0
---

# /castmate — the right model for the right job

You are the host agent. Castmates are other AI coding CLIs installed on this machine. A small script, `scripts/castmate.py` in this skill's folder, runs them. You decide who gets cast, write the prompt, read what comes back, and tell the user what it means.

Adapted from [counselors](https://github.com/aarondfrancis/counselors) by Aaron Francis (MIT). Discovery, prompt writing, and synthesis moved from code into this workflow, and the model list moved into config so it doesn't go stale.

```bash
python3 <skill-dir>/scripts/castmate.py list            # castmates, groups, install + read-only status
python3 <skill-dir>/scripts/castmate.py test codex fable # each must reply "OK"
python3 <skill-dir>/scripts/castmate.py run -c codex-sol-high,fable-high -f prompt.md --json
```

`<skill-dir>` is this skill's install folder. In Claude Code it is the skill's base directory.

## First run

**Before the first cast in a session, run `castmate.py test` on the castmates you plan to use.** It takes 5–15 seconds. `list` only shows that a CLI is installed, not that it's logged in or that the account has the model. If nothing is installed, or a test fails, set the user up first. **`references/cli-setup.md` is the setup guide.** Walk through it rather than reciting it:

1. Ask which agent CLIs they already use. One logged-in CLI is enough to start. Suggest Codex if they have none: it's the only one that confines `--write` to `--cwd`.
2. Give the install and login commands for their pick. Login is interactive, so the user runs it in their own terminal (in Claude Code they can type `! codex login` in the prompt). Then restart the agent if PATH or the shell profile changed.
3. Run `castmate.py test <castmate>`. Use `gemini-flash` for a first Gemini check, since not every key has `gemini-argon`. On failure, relay the `hint:` line it prints and the matching guide section.
4. **Never ask the user to paste an API key into chat.** For Gemini CLI, have them put `GEMINI_API_KEY` in their shell profile and restart the agent, or enter it in `gemini` directly. If they already tried Google sign-in, the key alone won't work until the saved `oauth-personal` auth type is switched. Use the one-liner in the guide's Gemini step 2. If a key does get pasted, say so, tell them to rotate it, and point to the guide's rotation steps.

Mention the gotchas that apply before they hit them. Gemini CLI no longer accepts Google sign-in on personal accounts. Antigravity's installer edits shell profiles, and its read-only mode is best-effort.

## Config (user state, outside the install folder)

`CONFIG=${MAKERSKILLS_CONFIG:-$HOME/.config/makerskills}/castmate`

- `$CONFIG/config.json` uses the same shape as `references/tools.json` and is merged on top of it. Add a castmate alias, a group, or a new CLI adapter here.
- `$CONFIG/casting.local.md` holds the user's own "use X for Y" rules. Read it before `references/casting.md`.
- `$CONFIG/runs/` is the default output folder, one subfolder per run.

**A new model needs no config at all.** `-c codex:gpt-5.7@high` or `-c claude:some-new-model` passes the model ID straight to the CLI. Offer to save an alias in `config.json` once it proves useful:

```json
{"castmates": {"sol7": {"tool": "codex", "model": "gpt-5.7", "effort": "high", "note": "GPT-5.7, high"}},
 "groups": {"review": ["fable-high", "sol7"]}}
```

## Step 1 — Pick the mode

| Mode | Castmates | Access | Use when |
|---|---|---|---|
| **Delegate** | 1 | read-only answer, or `--write` | A job to hand off: "have codex write the migration," "get haiku to summarize these logs" |
| **Fan-out** | 2–4 | read-only | Independent second opinions on a plan, diff, or decision |
| **Rounds** | 2–4, 2–4 rounds | read-only | Broad hunts (bugs, security, performance) where later rounds build on earlier ones |

If the request is vague, default to fan-out with two castmates. A named castmate plus a task ("ask codex to…") means delegate.

## Step 2 — Cast

1. Run `castmate.py list`. Show the user the castmates that matter for this job, not the whole table.
2. Read `$CONFIG/casting.local.md` (if present), then `references/casting.md`. Recommend a cast with a one-line reason for each.
3. Flag `unverified` adapters and `best-effort` read-only levels before dispatching. If an adapter has never been tested here, run `castmate.py test <name>` first.
   - **`enforced`** means the CLI's own sandbox or permission settings stop file writes, shell commands, MCP tools, and repo-level config such as hooks. Claude, Codex, and Gemini have been tested against a repo that plants hooks and MCP servers.
   - **`best-effort`** means the castmate is asked to stay read-only, but repo or user config can still give it more access. **Don't cast `best-effort` castmates on code the user didn't write** (a cloned repo, a contributor's PR) without saying so first.
4. **Confirm the exact list before dispatch:** "Casting: **codex-sol-high**, **fable-high**, read-only. OK?" Always confirm `--write` runs, and name the working directory.

Groups expand to their members, so show the expanded list. If the user names a group that doesn't exist, say so and don't guess.

## Step 3 — Write the prompt

Use `references/prompt-template.md`: the **Delegate** template for delegate mode, and the **Review** template for fan-out and rounds. For a focused hunt, paste a preset from `references/presets/` into the Instructions section.

- Gather context first: files named in the request, `git status` and `git diff`, and up to 5 related files found by search. **Reference files by path. Don't paste their contents.** Castmates read files themselves.
- **Paste the diff into the prompt** when the review is about changes. Claude castmates have no shell in read-only mode, so they can't run git.
- In a blind review, leave out your own conclusion. A castmate given your hypothesis tends to confirm it.
- Save the prompt to a temporary file, or pipe it with `-f -`.

## Step 4 — Dispatch

```bash
python3 <skill-dir>/scripts/castmate.py run -c <castmates> -f <prompt-file> [--write] [--cwd <repo>] [--timeout 540] --json
```

- Castmates can take 2–15 minutes each. Tell the user the ETA, then run the command in the background if the host supports it, so you can keep talking while it runs. The script prints a `still running: … (pid, elapsed)` line every 30 seconds on stderr; pass those along when the user asks or a run goes long.
- If a castmate goes well past its ETA, check the PID (`ps -p <pid>`) and tell the user. Don't wait silently.
- `--write` takes exactly one castmate. Before running it, check that the working tree is committed or stashed, so the castmate's changes form a clean diff.
  - **Only Codex limits writes to `--cwd`**, using its workspace sandbox. Claude, Gemini, Antigravity, and the others run with the user's full file access and are only *asked* to stay in `--cwd`. Say this when you confirm a non-Codex write run.
- Exit codes:
  - **0:** at least one castmate succeeded.
  - **1:** all castmates failed.
  - **2:** setup error, such as an unknown castmate, a missing binary, a refused `--write`, or a bad path.
  - **130 / 143:** interrupted by Ctrl+C or SIGTERM. Running castmates are stopped, queued ones never start, and `run.json` marks them `aborted` with their partial output.
- `--out` must be a new or empty folder. A read-only run refuses an `--out` inside `--cwd`, so it can't write into the tree it reviews. Without `--out`, each run gets a unique folder under `$CONFIG/runs/`.

## Step 5 — Read results

`run.json` in the output folder lists each castmate's `status`, `durationS`, `words`, `outputFile`, `stderrFile`, and the exact `command`.

- `success`: read `outputFile`.
- `timeout`: `outputFile` holds partial output. Use it, labeled as partial.
- `error` or `empty`: if the report has a `hint`, relay it first; it names the fix and the `cli-setup.md` section. Otherwise read `stderrFile`. Common causes are an expired login, a model the account can't use, or a flag a newer CLI version renamed. Report it and carry on with the rest. Antigravity returns `empty` whenever headless mode denies one of its tool calls, even after a long run, and drops the whole answer. If that happens, rerun with a narrower prompt or cast someone else.

## Step 6 — Present

**Delegate.** Review the castmate's work before calling it done. For `--write`, read `git diff`, run the project's tests and lint, and report what changed, what passed, and anything that looks off. You are accountable for code you hand back, whoever wrote it. For a read-only answer, relay it, and correct anything you can check that is wrong.

**Fan-out and rounds.** Synthesize; don't just concatenate:

```markdown
## Castmate review: [topic]
**Cast:** codex-sol-high, fable-high (read-only) · [N] succeeded, [N] failed
**Agree on:** [the key points castmates reached independently]
**Disagree on:** [each position and its reasoning]
**Risks flagged:** [anything one castmate raised that others missed]
**Blind spots:** [what no castmate covered that seems important]
**Recommendation:** [your call, weighing their evidence instead of counting votes]
Reports: [output folder]
```

Then offer the top 2–3 actions. If the user wants to act, plan before editing.

## Rounds mode

The host runs the rounds itself. Each round is one `castmate.py run` call into its own new folder (`--out <run>/round-N`, outside the reviewed repo).

1. Round 1: the base prompt.
2. Round N: the base prompt plus the **Round 2+ addendum** from `references/prompt-template.md`, with the prior outputs inlined (the most recent 8, about 1,500 words each).
3. Stop when you hit the preset's default round count or the user's limit, when time runs out, or when a round adds nothing beyond confirmed or duplicate labels. That last check is a judgment call: read the new findings rather than comparing word counts.
4. Write a final synthesis across all rounds in the Step 6 format, marking which findings survived challenge.

Each round costs as much as a full fan-out. State the expected total (rounds × castmates × minutes) before starting.

## Learning the cast

When a castmate is notably good or bad at a kind of job, offer to append a dated line to `$CONFIG/casting.local.md`. Ask before writing. That file is how casting improves over time.

## Adding an adapter

A CLI that isn't listed can be added in `$CONFIG/config.json` with no code change. Copy a similar entry from `references/tools.json`. Its fields:

- `binary`, `args` (before the mode args), and `argsAfter` (last).
- `prompt`: `stdin`, or `arg` together with `{prompt}` in `argsAfter`.
- `model` and `effort` flag templates.
- `readOnly`, with a `level` of `enforced` or `best-effort`, plus `args` and/or `env`. Claim `enforced` only after a planted repo hook and MCP server fail to run. Overrides in `config.json` merge key by key, so `{"readOnly": {"env": {...}}}` keeps the shipped args.
- `write` args.
- `output: last_message` with `{last_message}`, for CLIs that write their final answer to a file.

Leave `"verified": false` until `castmate.py test` passes.

## Errors

| Symptom | Do |
|---|---|
| `not found on PATH` | Walk through that CLI's section of `references/cli-setup.md`, or suggest another castmate |
| Test fails with an auth message | Relay the `hint:`. For Claude, Codex, or Antigravity, the user logs in again in their own terminal. For Gemini CLI, check the API key: Google sign-in won't work on personal accounts |
| Gemini says "no longer supported for Gemini Code Assist for individuals" | Gemini CLI needs an API key on personal accounts since 2026-06. Follow `references/cli-setup.md#gemini-cli`, or cast `antigravity` |
| Model rejected | Run `list` to find a valid alias, or ask which model their account has |
| Every castmate fails | Show the first lines of each `stderrFile`, then run `castmate.py test` on each |
