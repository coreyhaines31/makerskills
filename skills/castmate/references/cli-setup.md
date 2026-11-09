# Setting up castmates

castmate drives the official agent CLIs you already use. Each one needs to be installed and logged in once, and **one is enough to start**. Pick whichever you already pay for. If you have none, start with [Codex](#codex): it's the only one that keeps write access inside your project folder.

## 1. Find castmate's script

Commands below use `$CASTMATE` for the path to `castmate.py`. Set it once per terminal:

```bash
CASTMATE=$(find ~/.claude ~/.codex ~/.agents -path '*skills/castmate/scripts/castmate.py' 2>/dev/null | head -1)
echo "$CASTMATE"      # should print a path ending in skills/castmate/scripts/castmate.py
```

If it prints nothing, you probably cloned makerskills somewhere else. Use `CASTMATE=<your clone>/skills/castmate/scripts/castmate.py`, or ask your agent where castmate's script is. Agents don't need this step, because they know the skill's folder.

## 2. Pick one CLI and follow its section below

| CLI | Castmates | Read-only | Writes kept in `--cwd` | Sign-in |
|---|---|---|---|---|
| [Claude Code](#claude-code) | `fable`, `opus`, `sonnet`, `haiku` | enforced | no | Anthropic account |
| [Codex](#codex) | `codex`, `codex-sol-*`, `codex-terra`, `codex-luna`, `codex-research` | enforced | **yes** | ChatGPT account or API key |
| [Gemini CLI](#gemini-cli) | `gemini-flash`, `gemini-pro`, `gemini-argon` | enforced | no | **API key** (personal Google sign-in ended) |
| [Antigravity](#antigravity) | `antigravity` | best-effort | no | Google account |
| [Grok](#grok) | `grok` | best-effort | no | **xAI API key** |
| [Others](#other-clis) | `amp-smart`, `opencode`, `cursor`, `kiro` | best-effort, untested | no | varies |

**Read-only levels:**
- **enforced:** the CLI's own sandbox or permission settings block file writes, shell commands, MCP tools, and repo-level config such as hooks. This was tested against a repo that plants hooks and MCP servers.
- **best-effort:** the castmate is asked to stay read-only, but repo or user config can still give it more access. Don't use these on code you didn't write.

**Log in from a normal terminal.** Logins are interactive, so run them in your own terminal, not through an agent. In Claude Code you can also type `! <command>` in the prompt.

## 3. Check a CLI after setting it up

Each section below ends with this check. It works the same for any castmate:

```bash
python3 "$CASTMATE" list                # your CLI should say "installed"
python3 "$CASTMATE" test <castmate>     # e.g. test codex. Prints "ok <castmate>" when the model answers
```

`list` only checks that the CLI is installed; `test` checks that you're logged in and the model is available. If `test` fails, it prints a `hint:` line that points to the right section below. **Restart your agent** after installing a CLI or changing your shell profile, so it picks up the new PATH and variables.

---

## Claude Code

```bash
curl -fsSL https://claude.ai/install.sh | bash   # or see docs.anthropic.com/en/docs/claude-code
claude auth login
claude auth status
python3 "$CASTMATE" test sonnet
```

- **Read-only runs skip project config.** They run in safe mode, so the reviewed repo's hooks, MCP servers, and **`CLAUDE.md` / `AGENTS.md`** don't load. Name those conventions files in the prompt when they matter.
- **Write mode edits files but can't run shell commands,** so it can't run tests itself. Use Codex when the castmate must run tests.
- `fable` is Claude Fable 5. If your plan doesn't include it, use `opus` or `sonnet`, or any model ID with `-c claude:<model>`.

## Codex

```bash
npm install -g @openai/codex
codex login                                      # ChatGPT sign-in
# or: printenv OPENAI_API_KEY | codex login --with-api-key
codex login status
python3 "$CASTMATE" test codex
```

- **The only CLI that keeps `--write` inside `--cwd`,** through its workspace sandbox. It can also run tests inside that sandbox. Prefer it for delegated coding jobs.
- **Read-only runs ignore `~/.codex/config.toml`.** Your MCP servers and app connectors don't load, which is deliberate: some MCP servers run code outside the sandbox. If you rely on a custom model provider set in that file, read-only runs won't see it.
- **Live web search is off by default.** Cast `codex-research` when the job needs current docs.
- `codex-sol-*`, `codex-terra`, and `codex-luna` depend on your plan. `-c codex:<model>@<effort>` takes any model your account has.

## Gemini CLI

**Since June 2026, Gemini CLI no longer accepts Google sign-in for personal (unpaid or Google One) accounts.** Signing in fails with *"This client is no longer supported for Gemini Code Assist for individuals."* You need an API key, or you can use [Antigravity](#antigravity) instead, which still takes Google sign-in.

```bash
npm install -g @google/gemini-cli
```

1. **Create a key** at [aistudio.google.com/apikey](https://aistudio.google.com/apikey). A free tier is available. Never paste the key into an agent chat, because it ends up in the transcript.
2. **If you already tried Google sign-in,** that attempt saved `oauth-personal` and Gemini keeps retrying it. Switch it to API-key auth. This one-liner changes only that setting and keeps the rest of `~/.gemini/settings.json`:
   ```bash
   python3 -c 'import json,pathlib;p=pathlib.Path.home()/".gemini/settings.json";d=json.loads(p.read_text()) if p.exists() else {};d.setdefault("security",{}).setdefault("auth",{})["selectedType"]="gemini-api-key";p.parent.mkdir(exist_ok=True);p.write_text(json.dumps(d,indent=2)+"\n")'
   ```
3. **Give Gemini CLI the key,** either way:
   - **Shell profile:** add `export GEMINI_API_KEY="..."` to `~/.zshenv` (zsh) or `~/.bashrc` (bash). Open a new terminal and restart your agent.
   - **Interactive:** run `gemini`, choose **Use Gemini API Key**, and paste it there. This also sets the auth type for you. Gemini saves the key in the system keychain (macOS service `gemini-cli-api-key`, or the desktop keyring on Linux) and uses it even when `GEMINI_API_KEY` isn't set.
4. **Confirm:**
   ```bash
   python3 "$CASTMATE" test gemini-flash
   python3 "$CASTMATE" test gemini-argon     # Gemini 4 Argon, if your key has it
   ```
   If `gemini-flash` passes but `gemini-argon` fails with a model error, your key doesn't include Argon. Use `gemini-pro`, or pass any model ID with `-c gemini:<model>`.

**To rotate the key:** revoke it in AI Studio and update your shell profile, **and** delete the saved copy, or the old key keeps being used:
- macOS: `security delete-generic-password -s gemini-cli-api-key`
- Linux: remove `gemini-cli-api-key` with your keyring tool (for example Seahorse), or rerun `gemini` and enter the new key.

Read-only runs use plan mode plus castmate's own admin-tier policy (`gemini-readonly-policy.toml`), which blocks writes, shell commands, MCP tools, and leaving plan mode. Plan mode alone let writes through in testing.

## Antigravity

Google's supported path for personal accounts. It uses Google sign-in and needs no API key.

```bash
curl -fsSL https://antigravity.google/cli/install.sh | bash
export PATH="$HOME/.local/bin:$PATH"             # this terminal only; see the note below
agy                                              # first run signs you in; then type /quit
agy models                                       # the models your account can use
python3 "$CASTMATE" test antigravity
```

- **PATH:** the installer puts `agy` in `~/.local/bin` and appends a PATH line to `~/.zshrc` and `~/.profile`. That doesn't affect the terminal you're in. On **Linux with bash**, new terminals read `~/.bashrc` instead, so add `export PATH="$HOME/.local/bin:$PATH"` there too. If `~/.local/bin` was already on your PATH, delete the duplicate lines it added. Restart your agent afterward.
- **Sign-in without a browser** (SSH or a headless box): `agy` prints a sign-in URL. Open it on any machine and paste the code back into the terminal.
- **Picking a model:** the `antigravity` castmate uses `gemini-3.8-flash-high`. If `agy models` lists a model you prefer, add an alias in `~/.config/makerskills/castmate/config.json` (or `$MAKERSKILLS_CONFIG/castmate/config.json`). Create the folder first with `mkdir -p ~/.config/makerskills/castmate`:
  ```json
  {"castmates": {"agy-pro": {"tool": "antigravity", "model": "<id from agy models>", "note": "my Antigravity model"}}}
  ```
  Then run `python3 "$CASTMATE" test agy-pro`. For a one-off, `-c antigravity:<model>` works too.
- **Read-only is best-effort.** Plan mode blocked file writes in testing, but Antigravity loads your user MCP servers and has no flag to turn them off.
- **An `empty` result means a tool was denied.** When headless mode denies a tool call, Antigravity drops its whole answer. castmate tells it shell commands are unavailable, but a prompt that needs one can still come back empty.
- It updates itself in the background.

## Grok

xAI has no official agent CLI, so `grok` runs Grok through OpenCode's xAI provider.

1. Install OpenCode: `brew install opencode`.
2. Create an API key at [console.x.ai](https://console.x.ai) and add `export XAI_API_KEY=...` to your shell profile (`~/.zshenv`), then restart your agent. Never paste the key into chat.
3. `python3 "$CASTMATE" test grok`.

- **Read-only is best-effort.** It uses OpenCode's `plan` agent (see [Other CLIs](#other-clis)).
- **A newer Grok needs no update here.** `-c opencode:xai/<model-id>` works for any model on xAI's [model list](https://docs.x.ai/docs/models).

## Other CLIs

These adapters are ported from counselors' open PRs and **haven't been tested yet**. Run `python3 "$CASTMATE" test <name>` first, and expect to adjust flags in `~/.config/makerskills/castmate/config.json` (same shape as the skill's `references/tools.json`; your entries merge on top).

| CLI | Install | Notes |
|---|---|---|
| Amp | [ampcode.com](https://ampcode.com) | Read-only uses castmate's `amp-readonly-settings.json`, but workspace settings can override it |
| OpenCode | [opencode.ai/docs](https://opencode.ai/docs/) | Tested on 2.2.6. Read-only runs the built-in `plan` agent, which blocked writes and shell commands in testing; a project `opencode.json` can redefine that agent |
| Cursor | [cursor.com/cli](https://cursor.com/cli) | Needs a build with `--mode ask`; older builds (2025) reject it. Update with `cursor-agent update` |
| Kiro | [kiro.dev/docs/cli](https://kiro.dev/docs/cli/) | Tool names changed in Kiro V3, so the read-only list may need updating |

## First-run problems

| You see | Fix |
|---|---|
| `not found on PATH` | Install the CLI (above). If it's installed, open a new terminal and restart your agent so PATH updates |
| Gemini: "no longer supported for Gemini Code Assist for individuals" | [Gemini CLI](#gemini-cli) steps 1–4, or switch to Antigravity. Logging in with Google again won't help |
| Gemini: "Please set an Auth method" | [Gemini CLI](#gemini-cli) step 3 |
| Model rejected / unknown model | Your plan or key doesn't include it. Run `list` and pick another, or pass `-c <tool>:<model>` |
| Login or 401 errors | Claude: `claude auth login`. Codex: `codex login`. Antigravity: run `agy`. Gemini CLI: check the API key; Google sign-in won't work |
| Antigravity returns `empty` | See [Antigravity](#antigravity). Narrow the prompt or cast another model |
| `test` says FAIL but shows no error | The model answered something other than OK, usually a refusal or an account limit. Open the castmate's `.md` output |
