---
name: paste
description: When Corey wants to clean and reformat content (usually from his terminal) for pasting into Slack, Notion, Twitter/X, LinkedIn, email, GitHub, or plain text. Strips ANSI codes, box-drawing chars, terminal prompt artifacts, and applies destination-specific formatting. Default input is the clipboard (read via `pbpaste`); default output is both the clipboard (`pbcopy`) and a chat preview. Triggers on "/paste", "/paste [destination]", "clean this for X," "format for slack/notion/twitter/linkedin/email/github," "render as markdown," "paste-ready," "strip formatting," "make this copy-pastable." Default destination is plain. Also scans for secrets (API keys, tokens, .env values) and warns before copying anything sensitive.
metadata:
  version: 0.1.0
---

# /paste — Clean content for any destination

Cleans terminal output (ANSI, box-drawing, prompt artifacts, etc.) and reformats per destination rules. Reads clipboard by default, writes back to clipboard + previews in chat.

## Step 1 — Get the content

In order:
1. If the user included content in the prompt (pasted, or referenced from earlier in the conversation), use that.
2. Else, read clipboard: `pbpaste`
3. If both empty, ask Corey what to paste.

## Step 2 — Parse destination

| Invocation | Destination |
|---|---|
| `/paste` | **plain** (default) |
| `/paste plain` | plain |
| `/paste slack` | slack |
| `/paste notion` | notion |
| `/paste twitter` or `/paste x` | twitter |
| `/paste linkedin` or `/paste li` | linkedin |
| `/paste email` | email (plain) |
| `/paste email rich` or `/paste email html` | email (rich/HTML) |
| `/paste github` or `/paste gh` | github |
| `/paste markdown` or `/paste md` | markdown render |
| `/paste html` | render to HTML file + open in browser |

If ambiguous, ask. Per-destination rules live in `references/destinations.md`.

## Step 3 — Scan for secrets

Before any cleaning or copying, scan against patterns in `references/secret-patterns.md`.

If any match:
1. **Stop.** Don't copy yet.
2. Report what was detected with the value **masked** (first 4 + last 4 chars only — e.g. `sk-12...wxyz`).
3. Ask: *"Spotted [type] in the content. Continue, redact (replace with `[REDACTED]`), or abort?"*
4. Default to **abort** if no clear answer.

## Step 4 — Universal cleaning

Strip from the content:

- **ANSI escape codes** — `\x1b\[[0-9;]*[a-zA-Z]` and related (color codes, cursor movement, screen control)
- **Box-drawing chars** — `╭ ─ ╮ │ ╰ ╯ ╞ ╡ ╤ ╧ ┌ ┐ └ ┘ ├ ┤ ┬ ┴ ┼ ━ ┃ ┏ ┓ ┗ ┛` etc. Replace with simpler equivalents (`-`, `|`) or remove entirely depending on context.
- **Terminal prompt artifacts** — leading `$ `, `> `, `❯ `, `% `, `# ` (when first non-whitespace on a line that looks like a shell prompt)
- **Carriage returns** (`\r`) — replace with `\n` or delete
- **Trailing whitespace** per line
- **Excess blank lines** — collapse 3+ consecutive blank lines to 2

## Step 5 — Apply destination rules

Read `references/destinations.md` and apply the relevant transform.

## Step 6 — Output

| Destination | Output behavior |
|---|---|
| plain / slack / notion / twitter / linkedin / email / github | (a) Show preview in a code fence in chat. (b) Copy clean version to clipboard via `pbcopy`. |
| email rich | Render to HTML, write to `/tmp/paste-<timestamp>.html`, `open` it in browser. Skip clipboard (Corey copies from browser to preserve rich text). |
| markdown | Render the cleaned markdown directly in chat (Claude Code renders it). Also copy raw markdown to clipboard. Offer: *"Open as HTML too?"* — if yes, write and open. |
| html | Render to HTML, write to `/tmp/paste-<timestamp>.html`, `open` it. Skip clipboard. |

After output, report a one-line summary of what was cleaned (e.g., *"Stripped 12 ANSI codes, 4 box-drawing chars, 1 prompt artifact. Character count: 248 / 280 (X)."*).

## Length warnings

Twitter and LinkedIn have practical limits. Corey said "let me trim" — don't refuse or auto-truncate.

- **Twitter/X**: warn if >280 chars. Note the overage.
- **LinkedIn**: warn if >400 chars (comfort line, not hard limit).
- Other destinations: no length warning.

## URL handling for social destinations

If the content has URLs and destination is **twitter** or **linkedin**:
- Surface the URLs separately (don't include them in the body)
- Remind Corey: links go in a first comment (LinkedIn) or reply (X), not the body
- See `corey-skills:my-social` and `~/.claude/projects/-Users-coreyhaines/memory/feedback_social_link_placement.md`

## Examples

```
/paste slack
```
→ Reads clipboard, strips ANSI, converts `**bold**` to `*bold*`, copies to clipboard, shows preview.

```
/paste twitter
[pasted error log]
```
→ Uses pasted content (ignores clipboard), strips everything, warns at 412/280 chars, copies, asks if Corey wants to trim or pick a different destination.

```
/paste html
[pasted markdown table]
```
→ Renders table as HTML, opens in browser. Corey selects + copies into Notion/email with formatting preserved.

```
/paste
[pasted output with sk-anthropic-key in it]
```
→ Stops. *"Spotted what looks like an Anthropic API key: `sk-an...3kf9`. Continue, redact, or abort?"*
