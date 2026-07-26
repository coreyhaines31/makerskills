# Shop workflow — yield optimization, cut sessions, assembly design

How vibecad turns an approved design into a shop package someone can actually
execute: optimized buying, sequenced cutting, dependency-ordered assembly.

## 1. Yield optimization (run DURING design, not after)

`scripts/yieldopt.py` packs the cut list onto purchasable stock (first-fit-
decreasing with kerf + end-trim allowances) and reports shopping counts, cut
patterns, saw-setting batches, yield %, and keepable offcuts.

```bash
python3 scripts/yieldopt.py plan.json          # human shop package
python3 scripts/yieldopt.py plan.json --json   # structured result
```

Write one `plan.json` per material/profile (don't mix cedar 1x2 with PT 4x4).
Input format is documented in the script docstring: stock types with prices,
parts with `label/length/qty/angle`, global `kerf` (default 1/8") and
`end_trim` (default 1/2" per board end, for checked/split ends).

**The feedback loop is the point.** Run the optimizer while dimensions are
still negotiable, and adjust the DESIGN to unlock packings:

- **Bay/span sizing chases stock lengths**: 96" bays = uncut 8' boards,
  144" spans = uncut 12' boards. Unequal bays that pack beat equal bays
  that don't.
- **The stock/2 trap**: two "48-inch" parts do NOT fit one 8' board — end
  trim (0.5"/end) + one kerf eat 1.125", so the pair limit is
  `(96 − 1 − 0.125) / 2 = 47.4375"`. Spec paired parts at **47.25"** for
  practical margin (generally: `(stock − 2·trim − kerf) / 2`, rounded down
  to a friendly fraction). Same logic for thirds: 31.25", not 32".
- **Whole-board parts** (length = raw stock length) are legitimate but get
  flagged: no end-trim budget, so the shopper hand-picks boards with clean
  ends. The optimizer handles this automatically.
- **Check the pairings it finds** — it routinely discovers combos a human
  plan misses (e.g., 96" + 42" on one 12' board leaving a ~4.9" offcut,
  where the "obvious" 2×42-per-8' plan wastes 12" per board).
- Iterate: tweak part lengths → rerun → watch yield %. Above ~85% is good
  for mixed lists; uncut-heavy designs hit 95%+.
- **Buy spares**: add ~5% boards (minimum 2) beyond the optimized count for
  defects and miscuts. The optimizer gives the floor, not the buy.

## 2. Cut session design (the "step-by-step cuts")

Present cutting as a sequenced session, not a parts table:

1. **Inventory + triage**: count boards against the plan; set aside the
   straightest for whole-board and longest parts, knottiest for shortest.
2. **Batch by saw setting, not by part**: all square cuts first, then each
   angle once (the optimizer's SAW-SETTING BATCHES section). Every blade-
   angle change is a chance for error — minimize changes.
3. **Stop blocks for repeats**: any length cut more than twice gets a stop
   block on the miter-saw fence. List these explicitly ("set stop at 42in —
   cut 46 pieces").
4. **Follow the cut patterns**: each board's cuts in listed order (longest
   first), so a mis-cut ruins the shortest remaining piece, not the longest.
5. **Label as you cut**: blue tape + part ID on every piece. A 200-piece
   pile of similar lengths is unsortable by eye.
6. **Keep flagged offcuts** (the ≥12" list) in a labeled bin — they're the
   repair stock and jig material.

## 3. Assembly step design (the "step-by-step assembly")

Extends the LEGO-instruction rules in SKILL.md:

- **Physical dependency is law**: every step's parts must have something
  already built to fasten to. If a step renders parts floating, the order
  is wrong.
- **Each step carries its own fastener schedule**: exact type, size,
  coating, count, and drive direction ("#10 × 3/4in self-drilling pan-head,
  exterior coated, 2 per slat, driven from the steel side so no face
  heads"). Users ask for this every time — never ship a step that just says
  "attach".
- **Wrong-length warnings inline**: when a nearby size fails (1" screws
  poke through a 3/4" slat), say so in the step — that's where the mistake
  happens.
- **Flat-work before ladder-work**: anything assemblable on sawhorses
  (gates, panels, frames) is its own early step; only site-fixed work
  happens in place.
- **Per-step QC check**: end each step with the measurable check — square
  (diagonals equal), plumb, level line, gap gauge. One check per step.
- **Cure/wait steps are real steps**: concrete cure, glue set, finish dry —
  give them a step number so the schedule is honest.
- **Spacers and jigs from scrap**: call out the jig per step (a 2x4 laid
  flat is a 1.5" spacer; a stop block from the offcut bin). A dimension
  that equals common scrap is a design feature.

## 4. Fastener + hardware schedule (project-level)

Beyond per-step callouts, ship one consolidated table: every connection type
→ fastener spec → total count → package size to buy (round up to the box the
store sells). Include the non-fastener smalls users forget: clips, staples,
tension wire, turnbuckles, gloves, cutters, clamps, finish.

## 5. Dimensioned output

With the shop package, render the orthographic set with key dimensions
called out per segment (overall, post spacing, band heights, step drops) —
`--projection=o` views annotated in the accompanying text, or dimension
lines modeled as thin geometry in a `dims` show-group when the user wants
prints for the shop wall.
