---
name: paste
description: When you want to clean and reformat content (usually from your terminal) for pasting into Slack, Notion, Twitter/X, LinkedIn, email, GitHub, or plain text. Strips ANSI codes, box-drawing chars, terminal prompt artifacts, and applies destination-specific formatting. Default input is the system clipboard; default output is both the clipboard and a chat preview. Triggers on "/paste", "/paste [destination]", "clean this for X," "format for slack/notion/twitter/linkedin/email/github," "render as markdown," "paste-ready," "strip formatting," "make this copy-pastable." Default destination is plain. Also scans for secrets (API keys, tokens, .env values) and warns before copying anything sensitive.
metadata:
  version: 0.2.0
---

# /paste — Clean content for any destination

Cleans terminal output (ANSI, box-drawing, prompt artifacts, etc.) and reformats per destination rules. Reads clipboard by default, writes back to clipboard + previews in chat.

## Step 1 — Get the content

In order:
1. If the user included content in the prompt (pasted, or referenced from earlier in the conversation), use that.
2. Else, read the clipboard (commands below).
3. If both empty, ask the user what to paste.

**Clipboard commands by platform** (read / write):

| Platform | Read | Write |
|---|---|---|
| macOS | `pbpaste` | `pbcopy < "$f"` |
| Linux (Wayland) | `wl-paste -n` | `wl-copy < "$f"` |
| Linux (X11) | `xclip -selection clipboard -o` | `xclip -selection clipboard < "$f"` |
| Windows | `powershell Get-Clipboard -Raw` | `powershell "Get-Content -Raw '$f' \| Set-Clipboard"` |

`$f` is the temp file from the write procedure in Step 6. Always copy from a file, never from a heredoc or `echo`.

No clipboard (a remote, headless, or chat-bot agent): skip the clipboard, take content from the prompt, and return the cleaned text in a code fence.

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

**Clipboard write procedure** (every destination that writes to the clipboard):

1. **Write the cleaned content to a temp file with your agent's file-write tool**, e.g. `/tmp/paste-<slug>.txt`. Never pipe it through a shell heredoc or `echo`: agent harnesses can hard-wrap heredocs (~70 chars) and indent every line, so the paste comes out broken while the chat looks fine.
2. **Copy from the file** with the write command from Step 1.
3. **Verify the round trip.** Read the clipboard back and compare it to the file, e.g. `pbpaste | cmp -s - "$f" && echo match` (swap in the platform's read command; on Windows, `powershell "(Get-Clipboard -Raw) -eq (Get-Content -Raw '$f')"`). On a mismatch, report it and fall back to showing the text in a code fence.
4. **Build the chat preview from what you read back**, not from what you meant to copy. A preview from memory is how a mangled copy ships looking clean.
5. **Delete the temp file** once verified. It can hold anything the user copied, including text the secret scan let through.

| Destination | Output behavior |
|---|---|
| plain / slack / notion / twitter / linkedin / email / github | (a) Show preview in a code fence in chat. (b) Clipboard write procedure above; preview comes from the read-back. |
| email rich | Render to HTML, write to `/tmp/paste-<timestamp>.html`, open it in the browser (`open` on macOS, `xdg-open` on Linux, `start` on Windows). Skip clipboard (the user copies from browser to preserve rich text). |
| markdown | Render the cleaned markdown directly in chat (most agent UIs render it). Also copy raw markdown to the clipboard via the write procedure. Offer: *"Open as HTML too?"* — if yes, write and open. |
| html | Render to HTML, write to `/tmp/paste-<timestamp>.html`, open it in the browser. Skip clipboard. |

After output, report a one-line summary of what was cleaned (e.g., *"Stripped 12 ANSI codes, 4 box-drawing chars, 1 prompt artifact. Character count: 248 / 280 (X). Clipboard round-trip verified."*).

## Length warnings

Twitter and LinkedIn have practical limits. the user said "let me trim" — don't refuse or auto-truncate.

- **Twitter/X**: warn if >280 chars. Note the overage.
- **LinkedIn**: warn if >400 chars (comfort line, not hard limit).
- Other destinations: no length warning.

## URL handling for social destinations

If the content has URLs and destination is **twitter** or **linkedin**:
- Surface the URLs separately (don't include them in the body)
- Remind the user: links go in a first comment (LinkedIn) or reply (X), not the body
- See `makerskills:jab-hook` and `feedback_social_link_placement.md` in your memory store (your agent's memory, or `${MAKERSKILLS_MEMORY:-${MAKERSKILLS_CONFIG:-$HOME/.config/makerskills}/memory}/`)

## Examples

```
/paste slack
```
→ Reads clipboard, strips ANSI, converts `**bold**` to `*bold*`, copies to clipboard, shows preview.

```
/paste twitter
[pasted error log]
```
→ Uses pasted content (ignores clipboard), strips everything, warns at 412/280 chars, copies, asks if the user wants to trim or pick a different destination.

```
/paste html
[pasted markdown table]
```
→ Renders table as HTML, opens in browser. the user selects + copies into Notion/email with formatting preserved.

```
/paste
[pasted output with sk-anthropic-key in it]
```
→ Stops. *"Spotted what looks like an Anthropic API key: `sk-an...3kf9`. Continue, redact, or abort?"*

## Composes with

- `jab-hook` — clean output for pasting into Typefully drafts when the MCP path doesn't fit; also enforces the link-placement rule for X/LinkedIn destinations
- `social-fetch` — clean a fetched post before quoting it in a draft or newsletter
- `second-brain` — `paste` output can be captured cleanly into `raw/note-<slug>.md` for future compilation
- `watch-video` — transcript / summary output often flows through `paste` for platform-specific reformatting

## Notes on quality

- **The clipboard write procedure is not optional.** File → copy from file → read back and compare → preview from the read-back. Origin: 2026-07-31, a heredoc-piped copy shipped hard-wrapped and indented while the chat preview looked clean; the user caught it, not the verification.
- **Secret detection runs first, always.** Before any formatting or destination logic, `paste` scans for `sk-*`, `AKIA*`, `xoxb-*`, JWT-shaped strings, and long-hex tokens. Prompts before proceeding on any hit. Better to false-positive occasionally than to leak a real key.
- **Destination-aware transforms, not one-size-fits-all.** Slack wants `*bold*`; LinkedIn wants unicode-styled bold; email wants HTML. Same input, 9 different valid outputs. The destination flag is not optional.
- **ANSI codes get stripped for every destination.** Terminal escapes (`\033[31m` etc.) render as garbage everywhere except the source terminal.
- **Character limits are enforced, not warnings.** X at 280, LinkedIn at 3000, Twitter at 25000 — paste refuses to copy over-limit output and offers a trim strategy.
- **Links go in first comments for social destinations** — not the body. Enforced when destination is `twitter` or `linkedin`. Documented in `feedback_social_link_placement.md` in your memory store.
- **HTML destination opens in a browser tab, not the clipboard.** Formatted tables + code blocks need a rendered surface to select-and-copy from with formatting preserved. Copying raw HTML to the clipboard produces garbage in Notion/email.
