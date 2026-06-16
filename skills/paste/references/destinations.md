# Destination rules

After universal cleaning (Step 4 in SKILL.md), apply the transform below per destination.

---

## plain

Strip all markdown syntax. Result: text + line breaks only.

- `**bold**`, `*italic*`, `_italic_`, `~~strike~~` → remove the marks, keep the text
- `# Heading`, `## Heading` → keep text, drop the `#`
- `> blockquote` → drop the `>`
- `[link text](url)` → `link text (url)` or just `link text` if URL is noise
- Inline `` `code` `` → drop the backticks
- Triple-backtick code blocks → keep content as plain text (drop the fences and language hint)
- Tables → convert to bulleted lists (one row per bullet, columns separated by `: ` or `, `)
- Bullets and numbered lists → keep, normalize to `- ` and `1. ` style

---

## slack

Slack uses its own markdown subset.

- `**bold**` → `*bold*`
- `*italic*` → `_italic_`
- `~~strike~~` → `~strike~`
- `# H1` / `## H2` / `### H3` → bold text on its own line (Slack has no headers): `*Heading*`
- `[link text](https://url)` → `<https://url|link text>` (Slack auto-link format)
- Inline `` `code` `` → keep (Slack renders inline code)
- Triple-backtick code blocks → keep
- Bullet lists → keep with `• ` or `- `
- Numbered lists → keep
- Tables → convert to bulleted list. Slack tables look terrible. Example:
  ```
  | Name  | Role |
  | Alice | PM   |
  | Bob   | Eng  |
  ```
  →
  ```
  • Alice — PM
  • Bob — Eng
  ```

---

## notion

Notion's paste handler parses markdown natively. Keep everything.

- Keep all markdown syntax (`**bold**`, `*italic*`, `_underline_`, `~~strike~~`)
- Keep headers (`#`, `##`, `###`)
- Keep tables (Notion renders them as databases on paste)
- Keep code blocks with language hint (Notion preserves syntax highlighting)
- Keep links inline `[text](url)` — Notion handles them
- Keep blockquotes (`>`)
- Result: clean, idiomatic markdown

---

## twitter (X)

Strip all formatting. X is plain text.

- Strip all markdown (`**`, `*`, `_`, `~`, `#`, `>`, backticks)
- Strip headers entirely (no flat headers in tweets — they look weird)
- Strip code fences; keep the code contents (or note: "this is code, doesn't fit a tweet, want me to paste-bin it?")
- Tables → flatten to a short list
- URLs:
  - Surface them separately
  - Per Corey's voice rule: links don't go in the body — surface for use as a reply
- Char count: warn at >280

---

## linkedin

Strip formatting. LinkedIn is plain text.

- Strip all markdown
- Keep line breaks (LinkedIn rewards whitespace and scannability)
- Strip headers — use a bold-feeling first line instead (no actual bold available)
- URLs:
  - Surface separately, don't include in body
  - Per Corey's voice rule: links go in a first comment, not body
- No hashtags (Corey's voice rule)
- Char count: note at >400 (comfort line, not hard limit)

---

## email (plain)

Plain text email. Most safe across clients.

- Strip markdown syntax (keep the text)
- Convert links to `text (url)` format — most email clients won't auto-link inline markdown
- Keep tables as ASCII (most clients render OK in monospace; otherwise convert to bullets)
- Keep line breaks

---

## email (rich / html)

Render to HTML so Corey can copy from a browser into Gmail/Apple Mail with formatting preserved.

- Convert markdown → HTML (use a simple converter: `pandoc` if installed, else hand-render)
- Style with minimal inline CSS for readability (system font stack, 16px base, 1.5 line height, max-width 640px)
- Write to `/tmp/paste-<timestamp>.html`
- `open /tmp/paste-<timestamp>.html` to launch in default browser
- Skip clipboard — Corey selects + copies from the browser

---

## github

Markdown is native. Keep almost everything.

- Keep all markdown
- Keep code blocks with language hint (`)
- Keep tables (GitHub renders them)
- Strip ANSI from terminal output but **wrap the cleaned output in a fenced code block** with language hint (`bash`, `shell`, or `text` as appropriate)
- Keep links inline
- Keep `> blockquotes` (GitHub renders)
- @-mentions: leave as-is (user can decide whether to break them)

---

## markdown (render in chat)

Render the cleaned markdown directly in chat — Claude Code renders it inline for Corey to read.

- Apply universal cleaning
- Keep markdown structure intact
- Copy raw markdown to clipboard too (in case Corey wants to paste somewhere else)
- After rendering, offer: *"Want me to also open this as HTML in your browser?"* — if yes, write to `/tmp/paste-<ts>.html` and `open`

---

## html (render to file + open browser)

For when Corey wants to copy rich-formatted content from a browser into a rich-text destination (Notion via browser, email composer, Google Docs).

- Convert markdown → HTML
- Minimal inline CSS for clean reading
- Write to `/tmp/paste-<timestamp>.html`
- `open <path>` to launch in default browser
- Skip clipboard
- Tell Corey: *"Open in [Chrome/Safari]. Cmd-A, Cmd-C to grab the formatted version."*
