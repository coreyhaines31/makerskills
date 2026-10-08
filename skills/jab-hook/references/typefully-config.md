# Typefully config

**Personal config lives at `${MAKERSKILLS_CONFIG:-$HOME/.config/makerskills}/jab-hook/typefully.yaml`** — not in this repo (gitignored, on disk only).

## Setup (one-time)

```bash
# Create your personal config
mkdir -p ~/.config/makerskills/jab-hook
cp skills/jab-hook/references/typefully-config.example.yaml \
   ~/.config/makerskills/jab-hook/typefully.yaml

# Edit ~/.config/makerskills/jab-hook/typefully.yaml with your real Typefully social set ID.
# Find it via the Typefully MCP server's list-social-sets tool
```

## Schema

See `typefully-config.example.yaml` in this directory for the full schema + comments.

## How the skill loads it

1. Read `${MAKERSKILLS_CONFIG:-$HOME/.config/makerskills}/jab-hook/typefully.yaml`
2. If the file doesn't exist, fall back to interactive setup:
   - Call the Typefully MCP server's list-social-sets tool
   - Ask which one is the user's personal workspace
   - Save the answer to the config file for next time

## Other social sets in the same Typefully team

If you're in a team workspace, the config file's `other_social_sets` list documents which sets to AVOID by default when drafting. The skill will not push to those without explicit override.
