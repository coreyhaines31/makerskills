# OpenSCAD headless CLI reference

Everything needed to run the render loop without opening the GUI.

## Install (macOS)

```bash
brew install --cask openscad          # stable (2021.01) — linked to /opt/homebrew/bin/openscad
xattr -rd com.apple.quarantine /Applications/OpenSCAD-*.app   # required: cask is unsigned
```

Gatekeeper symptom: `openscad -o out.png file.scad` exits 1 with **no output and no file**. That's quarantine, not a script error. If a "Apple could not verify" dialog appears, click **Done** (not "Move to Trash"), then run the `xattr` line.

`brew install --cask openscad@snapshot` gets a newer dev build (signed, newer language features) if 2021.01 limits bite.

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

## 2021.01 language notes (stable cask)

- No `^` exponent operator — use `pow(x, 2)`.
- `text()` works but font metrics functions (`textmetrics()`) don't exist.
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
