---
name: vibecad
description: "When you want to design a physical object by describing it in plain English — no CAD UI, ever. Claude writes a parametric OpenSCAD script, renders multi-view previews headless, and iterates on your feedback like vibe coding a web app. Woodworking-first (cut lists, nominal vs actual lumber, board feet, sheet-goods layout) but handles 3D-print parts (STL) and laser/CNC (DXF) too. Triggers on \"/vibecad,\" \"design a [bench/shelf/table/bracket/jig],\" \"vibe cad,\" \"model this in openscad,\" \"make me a cut list,\" \"design something to build,\" \"3d model this part,\" \"woodworking design for X.\" Differs from slide-deck/canvas-design (2D visuals) — this produces buildable 3D geometry and shop-ready outputs."
metadata:
  version: 0.1.0
---

# /vibecad — Conversational parametric CAD via OpenSCAD

Describe the thing → get a rendered preview → say what's wrong → repeat. The user never touches a CAD UI; OpenSCAD is code-based CAD with a headless CLI, so the whole loop runs in the conversation. Every design is a parametric script — changing "make it 6 inches wider" is a one-parameter edit, not a redraw.

## Mental model

You are the CAD operator; the user is the client at your shoulder. They speak in outcomes ("a bench for the entryway, shoe storage underneath"); you translate to geometry, render, and show — never make them read code unless they ask. The script IS the source of truth: every dimension a named parameter at the top, every part a module.

## Step 0 — Environment check

| Tool | Check | Install if missing |
|---|---|---|
| OpenSCAD | `which openscad` | `brew install --cask openscad` (macOS) |

macOS Gatekeeper gotcha: the stable cask is unsigned, and a blocked binary **fails silently** — the render command exits 1 with no output and no PNG. Fix: `xattr -rd com.apple.quarantine /Applications/OpenSCAD-*.app`. If the user sees an "Apple could not verify…" dialog, tell them to click **Done** (not "Move to Trash"), then clear the quarantine flag. See [references/openscad.md](./references/openscad.md) for CLI details.

Project archive lives at `$MAKERSKILLS_CONFIG/vibecad/projects/<slug>/` (default `~/.config/makerskills/vibecad/projects/<slug>/`): `design.scad`, `renders/`, `notes.md`. Create it on first render. To resume a past design, list the projects dir and reload the .scad.

## Step 1 — Intake

Get just enough to draft v1 — don't interrogate. Three things:

1. **What is it and where does it live?** (function drives dimensions: a bench seat is ~17–18" high, a desk ~29–30", a shelf depth follows what it holds)
2. **Rough overall dimensions** — accept vagueness ("about four feet wide") and pick sensible defaults for the rest. State assumptions in the reply rather than asking.
3. **Material + how it gets made** — mode routing:
   - **Woodworking** (default for furniture/shop projects): units = **inches**, stock = dimensional lumber / sheet goods. Load [references/woodworking.md](./references/woodworking.md). Model ACTUAL sizes (a 2x4 is 1.5 × 3.5), never nominal.
   - **3D print**: units = **mm**, output STL, respect printability (overhangs, wall thickness ≥ 2 perimeters).
   - **Laser/CNC flat parts**: units per machine, output DXF via 2D projection.

One clarifying question max if something load-bearing is genuinely ambiguous; otherwise default and move.

## Step 2 — Write the parametric script

Conventions (these make iteration cheap — the whole point):

- **All key dimensions as named parameters at the top**, commented with units. `bench_width = 48; // in`
- **One module per physical part** (`module leg()`, `module seat_slat()`), positioned in an assembly at the bottom. In woodworking mode, each module = one piece of lumber you'd cut.
- **Distinct color per part type** (`color("BurlyWood") leg();`) so renders read at a glance.
- **`explode` parameter** (default 0): translate parts apart along sensible axes so joinery is visible when set. Offer an exploded render whenever assembly is non-obvious.
- Derive, don't repeat: `seat_height - stock_thickness`, never a second hardcoded number.
- Target OpenSCAD 2021.01 language (no fancy recent features) unless a newer version is confirmed — see [references/openscad.md](./references/openscad.md).

## Step 3 — Render loop (the core)

1. Save the script to the project dir.
2. Render the standard 4 views headless (iso + front + top + side; commands in [references/openscad.md](./references/openscad.md)).
3. **Read the PNGs yourself before showing anything.** Self-check: parts colliding or floating? proportions match the spec? joinery plausible? gravity survivable? Fix and re-render until it passes — the user should only see renders you'd stand behind.
4. Show the iso view (plus whichever other view is informative), state key dimensions and any assumptions made, and ask what to change.
5. Take feedback in plain English → edit parameters/geometry → re-render → repeat. Never ask the user to look at code; never describe a change without showing the re-render.

## Step 4 — Shop-ready outputs

When the user approves the design ("lock it in," "that's it," "build it"):

- **Woodworking**: cut list table (part, qty, stock, cut length, notes), board-foot / sheet estimate, hardware list if any, assembly order. Formulas + stock tables in [references/woodworking.md](./references/woodworking.md). Offer a dimensioned orthographic render set.
- **3D print**: `openscad -o part.stl design.scad`, report bounding box + rough volume.
- **Laser/CNC**: `projection()` each flat part → DXF export.

Write `notes.md` in the project dir: what it is, final key dimensions, decisions made and why, date. That's the resume point for "let's revisit the bench."

## Composes with

- **`second-brain`** — capture finished project summaries to the vault if the user asks
- **`skillify`** — pattern-source for this skill's structure

## Notes on quality

- **Never show a render you haven't looked at.** Silent geometry bugs (z-fighting overlaps, floating parts, inverted differences) are obvious in the PNG and embarrassing after.
- **Nominal lumber sizes are lies.** A 2x4 is 1.5 × 3.5 actual. Modeling nominal produces cut lists that don't fit. Always the actual-size table.
- **A failed render with no output usually isn't your code.** Exit 1 + no PNG + no stderr = Gatekeeper quarantine (macOS). Check that before debugging the .scad.
- **Inches for wood, mm for prints.** Mixing units inside one script is the classic vibe-CAD failure; declare the unit in a comment on line 1.
- **Parameters are the contract.** If a user tweak requires restructuring geometry rather than changing a parameter, the initial parameterization was wrong — restructure so next time it's a parameter.
- **Cut lists count kerf.** Parts that sum to exactly a board's length don't fit on that board; flag when a layout is within 1" of stock length.
