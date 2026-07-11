# Woodworking reference — stock sizes, cut lists, board feet

## Nominal vs actual dimensional lumber (softwood, surfaced S4S)

Model the ACTUAL size. Cut lists built on nominal sizes don't fit.

| Nominal | Actual (in) | Nominal | Actual (in) |
|---|---|---|---|
| 1x2 | 0.75 × 1.5 | 2x2 | 1.5 × 1.5 |
| 1x3 | 0.75 × 2.5 | 2x3 | 1.5 × 2.5 |
| 1x4 | 0.75 × 3.5 | 2x4 | 1.5 × 3.5 |
| 1x6 | 0.75 × 5.5 | 2x6 | 1.5 × 5.5 |
| 1x8 | 0.75 × 7.25 | 2x8 | 1.5 × 7.25 |
| 1x10 | 0.75 × 9.25 | 2x10 | 1.5 × 9.25 |
| 1x12 | 0.75 × 11.25 | 2x12 | 1.5 × 11.25 |
| — | | 4x4 | 3.5 × 3.5 |

Common stud/board lengths at the yard: 8', 10', 12', 16' (studs also 92-5/8").
Hardwood is sold rough by the quarter (4/4 ≈ 1" rough → ~13/16" surfaced; 8/4 ≈ 2" rough → ~1-3/4" surfaced) — confirm actuals with the supplier.

## Sheet goods

Standard sheet: **48 × 96** (4'×8'). Common thicknesses (plywood actuals run slightly under):

| Nominal | Typical actual |
|---|---|
| 1/4" | 7/32 (0.22") |
| 1/2" | 15/32 (0.47") |
| 3/4" | 23/32 (0.72") |

Sanded hardwood ply often measures a hair under even that (3/4" nominal ≈ 0.70" measured) — for snug dados, measure the actual sheet and parameterize the thickness.

MDF and baltic birch run closer to true; baltic birch often comes in 60×60 (5'×5') sheets.

## Board feet

`bf = (thickness_in × width_in × length_ft) / 12`

- **Softwood dimensional lumber**: use NOMINAL thickness and width (the one place nominal is correct) — though yards mostly price per stick, not per board foot.
- **Hardwood (random width)**: use quarter thickness (4/4 = 1", 8/4 = 2") × ACTUAL measured width × length; suppliers round per their own policy, so treat estimates as ±10%.
- Sheet goods are priced per sheet, not per board foot.

## Cut list format

| Part | Qty | Stock | Cut length | Notes |
|---|---|---|---|---|
| Leg | 4 | 2x4 | 16" | |
| Seat slat | 5 | 1x4 | 48" | rip to 3" |
| Stretcher | 2 | 2x4 | 41" | half-lap both ends |

Below the table: stock shopping list (e.g. "three 8' 2x4s, one 8' 1x4 ×5 — or two 10' 1x4s and…") computed by packing cut lengths into stock lengths **with kerf**.

## Kerf and layout rules

- Saw kerf ≈ **1/8"** per cut. N parts from one board = N−1 (or N) kerfs of loss.
- Never plan a layout where parts + kerfs land within **1"** of stock length — boards have checked/split ends that get trimmed. Flag it and add a board.
- Sheet-goods layouts: keep parts 0.5" from factory edges when a clean edge matters; factory edges aren't reference-straight.

## Ergonomic defaults (when the user doesn't specify)

| Thing | Default |
|---|---|
| Seat height (bench/chair) | 17–18" |
| Table/desk height | 29–30" |
| Counter height | 36" |
| Bar height | 42" |
| Bench/seat depth | 15–18" |
| Bookshelf depth | 10–12" (11.25" = 1x12) |
| Shelf span before sag (3/4" ply, books) | ≤ 32" |
| Workbench height | user's knuckle height, ~34–38" |

## Joinery quick guide (for assembly notes)

- **Butt + screws**: fastest; fine for shop furniture. Pre-drill near ends.
- **Pocket screws**: hidden-ish, strong for face frames and aprons.
- **Half-lap**: strong, easy on a table saw or with a circular saw + chisel; great for stretchers.
- **Dado/rabbet**: shelves into case sides; depth = 1/3 of stock thickness.
- **Dowels/dominoes/mortise-tenon**: furniture-grade; call out only when the user signals fine-furniture intent.
