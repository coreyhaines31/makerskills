# OpenSCAD headless CLI reference

Everything needed to run the render loop without opening the GUI.

## Install (macOS)

```bash
brew install --cask openscad@snapshot   # preferred: signed + notarized, Apple Silicon native, current language features
```

The snapshot cask is the right default. The `openscad` stable cask (2021.01) is unsigned, Intel-only (Rosetta 2 on Apple Silicon), deprecated by Homebrew, and scheduled to be disabled 2026-09-01. If stable is what's installed anyway:

- Gatekeeper symptom: `openscad -o out.png file.scad` exits 1 with **no output and no file**. That's quarantine, not a script error. Fix: `xattr -rd com.apple.quarantine /Applications/OpenSCAD-*.app`
- If an "Apple could not verify" dialog appears, click **Done** (not "Move to Trash"), then run the `xattr` line.

Either cask links `openscad` into the PATH (e.g. `/opt/homebrew/bin/openscad`).

## Letting the user view the model interactively

Default to opening the rendered PNGs in Preview (`open renders/*.png`) — zero learning curve. If the user wants to orbit the model, `open -a OpenSCAD design.scad` — but warn them upfront: **nothing draws until they press F5** (the viewport shows only bare axes on load), and the default layout buries the 3D view. Tell them: press F5, then View → Hide Editor and View → Hide Console, then drag to orbit. Enable Design → Automatic Reload and Preview so your subsequent file edits appear live in their window.

## Standard 4-view render set

```bash
S=design.scad; R=renders; mkdir -p $R
openscad -o $R/iso.png   --imgsize=1200,900 --viewall --autocenter $S
openscad -o $R/front.png --imgsize=1200,900 --viewall --autocenter --projection=o --camera=0,0,0,90,0,0,0   $S
openscad -o $R/top.png   --imgsize=1200,900 --viewall --autocenter --projection=o --camera=0,0,0,0,0,0,0    $S
openscad -o $R/side.png  --imgsize=1200,900 --viewall --autocenter --projection=o --camera=0,0,0,90,0,90,0  $S
```

- `--camera=tx,ty,tz,rotx,roty,rotz,dist` — with `--viewall` the distance value is recomputed, so `0` is fine.
- `--projection=o` = orthographic (use for front/top/side; leave iso perspective).
- Renders use the fast preview (CSG) pipeline by default — fine for previews. Add `--render` to force full CGAL evaluation when checking that a `difference()`/`intersection()` actually resolves (slower).
- Read the PNGs with the Read tool after every render — self-check before showing the user.

## Exports

```bash
openscad -o part.stl design.scad                 # 3D print
openscad -o part.dxf design.scad                 # requires the script's top level to be 2D (projection())
openscad -D 'explode=1' -o exploded.png --viewall --autocenter design.scad   # -D overrides any top-level parameter
```

`-D` is the iteration cheat code: render dimension variants without editing the file, e.g. `-D 'bench_width=60'`.

## 2021.01 language notes (only if targeting the old stable cask)

- `^` exponent operator works (2021.01 is the version that introduced it); `pow()` only needed pre-2021.01.
- `text()` works but font metrics functions (`textmetrics()`) are not available in stable 2021.01 — development snapshots only.
- Modules can't return values; functions can't create geometry. Pure-math helpers = `function`, geometry = `module`.
- `$fn=64` on cylinders/spheres for smooth previews; leave default for speed while iterating.

## Script skeleton

```openscad
// units: inches
bench_width   = 48;    // overall width
seat_height   = 17.5;  // floor to seat top
stock_2x4     = [1.5, 3.5];   // actual, not nominal
explode       = 0;     // set 1 (or use -D) for exploded view

module leg() { color("BurlyWood") cube([stock_2x4[0], stock_2x4[1], seat_height - stock_2x4[0]]); }
module seat_slat() { color("Peru") cube([bench_width, stock_2x4[1], stock_2x4[0]]); }

// assembly
leg();
translate([bench_width - stock_2x4[0], 0, 0]) leg();
translate([0, 0, seat_height - stock_2x4[0] + explode * 4]) seat_slat();
```
