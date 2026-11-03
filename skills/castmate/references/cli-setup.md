# Setting up castmates

castmate drives the official agent CLIs you already use. Each one needs to be installed and logged in once. After that, `castmate.py test <name>` confirms it works.

**Quick start:** install one CLI below, log in, then run:

```bash
python3 <skill-dir>/scripts/castmate.py list          # what's installed, and each read-only level
python3 <skill-dir>/scripts/castmate.py test codex    # must print "ok"
```

| CLI | Castmates | Read-only | Writes confined to `--cwd` | Login |
|---|---|---|---|---|
| [Claude Code](#claude-code) | `fable`, `opus`, `sonnet`, `haiku` | enforced | no | Anthropic account |
| [Codex](#codex) | `codex`, `codex-sol-*`, `codex-terra`, `codex-luna`, `codex-research` | enforced | **yes** | ChatGPT account or API key |
| [Gemini CLI](#gemini-cli) | `gemini-argon`, `gemini-pro`, `gemini-flash` | enforced | no | **API key** (personal Google sign-in ended) |
| [Antigravity](#antigravity) | `antigravity` | best-effort | no | Google account |
| [Others](#other-clis) | `amp-smart`, `opencode`, `cursor`, `kiro` | best-effort, untested | no | varies |

**Read-only levels:**
- **enforced:** the CLI's own sandbox or permission settings block file writes, shell commands, MCP tools, and repo-level config such as hooks. This was tested against a repo that plants hooks and MCP servers.
- **best-effort:** the castmate is asked to stay read-only, but repo or user config can still give it more access. Don't use these on code you didn't write.

---

## Claude Code

```bash
curl -fsSL https://claude.ai/install.sh | bash   # or see docs.anthropic.com/en/docs/claude-code
claude auth login
claude auth status                               # confirm
```

- **Read-only runs skip project config.** They run in safe mode, so the reviewed repo's hooks, MCP servers, and **`CLAUDE.md` / `AGENTS.md`** don't load. Name those conventions files in the prompt when they matter.
- **Write mode edits files but can't run shell commands,** so it can't run tests itself. Use Codex when the castmate must run tests.
- `fable` is Claude Fable 5. If your plan doesn't include it, use `opus` or `sonnet`, or any model ID with `-c claude:<model>`.

## Codex

```bash
npm install -g @openai/codex
codex login                                      # ChatGPT sign-in
# or: printenv OPENAI_API_KEY | codex login --with-api-key
codex login status                               # confirm
```

- **The only CLI that confines `--write` to `--cwd`,** through its workspace sandbox. It can also run tests inside that sandbox. Prefer it for delegated coding jobs.
- **Read-only runs ignore `~/.codex/config.toml`.** Your MCP servers and app connectors don't load, which is deliberate: some MCP servers run code outside the sandbox. If you rely on a custom model provider set in that file, read-only runs won't see it.
- **Live web search is off by default.** Cast `codex-research` when the job needs current docs.
- The `codex-sol-*`, `codex-terra`, and `codex-luna` models depend on your plan. `-c codex:<model>@<effort>` takes any model your account has.

## Gemini CLI

**Since June 2026, Gemini CLI no longer accepts Google sign-in for personal (unpaid or Google One) accounts.** Signing in fails with *"This client is no longer supported for Gemini Code Assist for individuals."* Use an API key, or use [Antigravity](#antigravity) instead.

```bash
npm install -g @google/gemini-cli
```

1. **Create a key** at [aistudio.google.com/apikey](https://aistudio.google.com/apikey). A free tier is available.
2. **Make it available to Gemini CLI**, either way:
   - **Environment:** add `export GEMINI_API_KEY="..."` to `~/.zshenv` (zsh) or `~/.bashrc` (bash), then open a new terminal **and restart your agent** so it inherits the variable.
   - **Interactive:** run `gemini`, choose **Use Gemini API Key**, and paste it there. Gemini CLI saves the key in the system keychain (on macOS, service `gemini-cli-api-key`; on Linux, the desktop keyring when one is running) and uses it even when `GEMINI_API_KEY` isn't set.
3. **Set the auth type** if you tried Google sign-in first. That attempt saves `oauth-personal`, which keeps failing. In `~/.gemini/settings.json`:
   ```json
   {"security": {"auth": {"selectedType": "gemini-api-key"}}}
   ```
4. **Confirm:** `castmate.py test gemini-argon`.

- **Never paste the key into an agent chat.** It ends up in the transcript.
- **To rotate the key:** revoke it in AI Studio, update `~/.zshenv`, **and** delete the saved copy, or the old key keeps being used. On macOS:
  ```bash
  security delete-generic-password -s gemini-cli-api-key
  ```
  On Linux, remove `gemini-cli-api-key` with your keyring tool (for example `secret-tool` or Seahorse), or rerun `gemini` and choose a new key.
- **Models:** `gemini-argon` is Gemini 4 Argon. To see what your key can use:
  ```bash
  curl -s -H "x-goog-api-key: $GEMINI_API_KEY" "https://generativelanguage.googleapis.com/v1beta/models?pageSize=200" | grep '"name"'
  ```
- Read-only runs use plan mode plus castmate's own admin-tier policy (`gemini-readonly-policy.toml`), which blocks writes, shell commands, MCP tools, and leaving plan mode. Plan mode alone let writes through in testing.

## Antigravity

Google's supported path for personal accounts. It uses Google sign-in and needs no API key.

```bash
curl -fsSL https://antigravity.google/cli/install.sh | bash
agy                                              # first run opens the browser to sign in; then /quit
agy models                                       # the models your account can use
```

- **The installer edits your shell profiles.** It appends a PATH line to `~/.zshrc` and `~/.profile`, even if `~/.local/bin` is already on your PATH. Remove the duplicates if you like.
- **Model choice:** the `antigravity` castmate uses `gemini-3.8-flash-high`. If `agy models` lists something better for you, add an alias in `config.json`. For example, Gemini 3.1 Pro isn't offered on every account.
- **Read-only is best-effort.** Plan mode blocked file writes in testing, but Antigravity loads your user MCP servers and has no flag to turn them off.
- **An `empty` result means a tool was denied.** When headless mode denies a tool call, Antigravity drops its whole answer. castmate tells it shell commands are unavailable, but a prompt that needs one can still come back empty.
- It updates itself in the background.

## Other CLIs

These adapters are ported from counselors' open PRs and **haven't been tested yet**. Run `castmate.py test <name>` first, and expect to adjust flags in `config.json`.

| CLI | Install | Notes |
|---|---|---|
| Amp | [ampcode.com](https://ampcode.com) | Read-only uses castmate's `amp-readonly-settings.json`, but workspace settings can override it |
| OpenCode | [opencode.ai/docs](https://opencode.ai/docs/) | Project `opencode.json` can override the read-only permissions |
| Cursor | [cursor.com/cli](https://cursor.com/cli) | Needs a build with `--mode ask`; older builds (2025) reject it. Update with `cursor-agent update` |
| Kiro | [kiro.dev/docs/cli](https://kiro.dev/docs/cli/) | Tool names changed in Kiro V3, so the read-only list may need updating |

## First-run problems

| You see | Fix |
|---|---|
| `not found on PATH` | Install the CLI (above). If it's installed, open a new terminal or restart your agent so PATH updates |
| Gemini: "no longer supported for Gemini Code Assist for individuals" | [Gemini CLI](#gemini-cli) steps 1–3, or switch to Antigravity |
| Gemini: "Please set an Auth method" | Set `GEMINI_API_KEY` or pick API key in `gemini`, then step 3 |
| Model rejected / unknown model | Your plan doesn't include it. Run `castmate.py list` and pick another, or pass `-c <tool>:<model>` |
| Login or 401 errors | Log in again (`claude auth login`, `codex login`, `agy`) |
| Antigravity returns `empty` | See [Antigravity](#antigravity). Narrow the prompt or cast another model |
| `test` fails with a model saying something other than OK | Usually a refusal or an account limit. Read the `stderr` file it prints |
