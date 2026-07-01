# Install

`makerskills` is a Claude Code plugin — a collection of skills you load into Claude Code. Skills work out of the box; some need a one-time config (your Typefully workspace, your social-portfolio properties, your vault path) before they're useful.

## 1. Install the plugin

In Claude Code:

```
/plugin marketplace add coreyhaines31/makerskills
/plugin install makerskills@makerskills
```

Or symlink for local dev:

```bash
git clone https://github.com/coreyhaines31/makerskills ~/code/makerskills
ln -s ~/code/makerskills ~/.claude/plugins/makerskills
```

## 2. Configure your environment

Add to `~/.zshenv` (or `~/.bashrc`). Defaults usually work; override only what's different for you:

```bash
# Where personal config / archives live (gitignored, on disk only)
export MAKERSKILLS_CONFIG="$HOME/.config/makerskills"

# Where the slide-deck skill writes branded React decks (only if you have one)
export SLIDE_DECK_REPO="$HOME/code/your-personal-site-repo"

# Where the second-brain skill reads/writes your personal wiki vault
export SECOND_BRAIN_VAULT="$HOME/Documents/SecondBrain"

# Where the company-brain skill reads/writes your team's shared vault
export COMPANY_BRAIN_VAULT="$HOME/Documents/CompanyBrain"

# Where the company-cfo skill reads/writes company financial workflow (reports, projector, config)
export COMPANY_CFO_ROOT="$HOME/code/company-cfo"

# Optional: dev-server URL pattern for slide-deck preview (default: localhost:3000)
export SLIDE_DECK_DEV_HOST="localhost:3000"
```

## 3. Set up personal config files

These contain your real data and are stored under `$MAKERSKILLS_CONFIG/` (default `~/.config/makerskills/`). They're gitignored — your personal data never leaves your machine.

```bash
mkdir -p ~/.config/makerskills/{jab-hook,pm,decide,business-brainstorm,deep-research,personal-cfo,slide-deck}

# Copy example configs and edit them with your real values
cp ~/code/makerskills/skills/jab-hook/references/typefully-config.example.yaml \
   ~/.config/makerskills/jab-hook/typefully.yaml
cp ~/code/makerskills/skills/jab-hook/references/properties.example.yaml \
   ~/.config/makerskills/jab-hook/properties.yaml

# Edit these with your real Typefully social set ID + your portfolio properties
```

## 4. Install runtime dependencies

Each skill has its own dependencies. Install only what the skills you use need:

```bash
# Core (used by multiple skills)
brew install yt-dlp ffmpeg pandoc git-filter-repo

# Python tool runner (for MLX-Whisper and other Python tools)
brew install uv
uv tool install mlx-whisper                 # transcription on Mac

# Optional: for PDF rendering from read-book / second-brain
brew install --cask basictex
sudo tlmgr update --self && sudo tlmgr install collection-fontsrecommended

# Optional: for EPUB/MOBI conversion in read-book
brew install --cask calibre                 # for ebook-convert
```

## 5. API keys

All skills work without these (free fallbacks); these unlock premium capability:

```bash
# In ~/.zshenv
export NOTION_API_KEY="..."                 # pm Notion adapter, deep-research
export TYPEFULLY_API_KEY="..."              # jab-hook drafts
export GEMINI_API_KEY="..."                 # watch-video multimodal mode
export SCRAPECREATORS_API_KEY="..."         # social-fetch full data (X, IG, TikTok, LinkedIn posts)
export BRAVE_API_KEY="..."                  # deep-research / last30days web search
export PLANE_API_KEY="..."                  # pm Plane adapter (if you use Plane)
export LINEAR_API_KEY="..."                 # pm Linear adapter (if you use Linear)
export DOMAINR_API_KEY="..."                # domain — Domainr aggregation (free at rapidapi.com/domainr/api/domainr)
export NAMECHEAP_API_USER="..."             # domain — Namecheap availability + prices
export NAMECHEAP_API_KEY="..."              # domain — pair with NAMECHEAP_API_USER
export NAMECHEAP_CLIENT_IP="..."            # domain — must be whitelisted in Namecheap dashboard
```

Free tiers exist for most. See each skill's `references/` directory for setup details.

## 6. Verify

```bash
# Should see 18 skills listed
ls ~/code/makerskills/skills/

# In Claude Code, try:
/skillify                                   # should respond with mode selection (CREATE / ADAPT / UPDATE)
/decide                                     # should ask for the decision context
/paste                                      # should read clipboard
/company-brain                              # should route to a mode (needs COMPANY_BRAIN_VAULT set)
/company-cfo                                # should route to a mode (needs COMPANY_CFO_ROOT set)
/domain                                     # domain-hunt workflow (needs Vercel CLI + whois; Domainr + Namecheap keys optional)
```

## What's next

Read the `README.md` for the skill catalog + composition map. Each skill's `SKILL.md` has its own usage docs. Most skills work the first time you invoke them; a few (`jab-hook`, `pm`, `personal-cfo`, `second-brain`) need the personal config from Step 3 before they're fully useful.

## Architecture: where personal data lives

This repo is **public + generic**. Your real data lives in two places, both gitignored / off-disk-from-repo:

| Location | What |
|---|---|
| `~/.config/makerskills/<skill>/` | Personal config (Typefully IDs, properties list, board mappings, voice overlays) |
| `~/Documents/<skill>/` | Generated outputs (video transcripts, book notes, slide exports, etc.) |

To migrate to a new machine: copy `~/.config/makerskills/` and your `~/.zshenv` env vars. The repo + your config = your full setup.
