# Properties — rotation methodology

**Personal property list lives at `${MAKERSKILLS_CONFIG:-$HOME/.config/makerskills}/jab-hook/properties.yaml`** — not in this repo (gitignored, on disk only).

This file documents the rotation methodology that operates on whatever properties you configure.

## Setup (one-time)

```bash
mkdir -p ~/.config/makerskills/jab-hook
cp skills/jab-hook/references/properties.example.yaml \
   ~/.config/makerskills/jab-hook/properties.yaml

# Edit ~/.config/makerskills/jab-hook/properties.yaml — add your real properties
```

See `properties.example.yaml` for the full schema with comments.

## Rotation methodology

- **N slots, equal weight.** Each slot = one of your things to promote.
- Default cadence: **~1 promo every 3 weeks per slot, ~2 promos/week total.**
- When picking the "most overdue" slot, count from the date of the last **promo** post that mentioned it (BIP / educational mentions don't reset the timer).

## How the skill uses your properties config

1. Reads `${MAKERSKILLS_CONFIG:-$HOME/.config/makerskills}/jab-hook/properties.yaml`
2. For each slot, tracks "days since last promo" against Typefully history
3. Picks next promo based on Eisenhower-like priority (overdue + currently-most-promotable)
4. Drafts using the slot's voice notes + angle ideas
5. For "rotating" slots (e.g., ebooks where one slot cycles through N items), advances internal rotation per call

## Adding / removing slots

Edit `~/.config/makerskills/jab-hook/properties.yaml` and re-run `/jab-hook` — no other change needed. The skill picks up the new config on every run.
