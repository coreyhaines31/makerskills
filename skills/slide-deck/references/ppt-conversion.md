# PPT conversion reference

Convert a legacy PowerPoint deck (client deck, conference template, vendor pitch) into Corey's React system. Preserves text, structure, speaker notes, and images.

## Prerequisites

```bash
pip install python-pptx
```

## Step 1 — Extract content

Save the script at `~/Documents/slide-conversions/_scripts/extract_pptx.py`:

```python
#!/usr/bin/env python3
"""Extract titles, body text, speaker notes, and image refs from a PPTX."""
import json
import sys
from pathlib import Path
from pptx import Presentation
from pptx.util import Emu

def extract(pptx_path: str, out_dir: str) -> None:
    out = Path(out_dir)
    assets = out / "assets"
    out.mkdir(parents=True, exist_ok=True)
    assets.mkdir(exist_ok=True)

    p = Presentation(pptx_path)
    slides = []

    for i, slide in enumerate(p.slides):
        title = ""
        bodies = []
        images = []

        for shape in slide.shapes:
            if shape.has_text_frame:
                text = shape.text_frame.text.strip()
                if not text:
                    continue
                # Heuristic: first non-empty text on a slide is the title
                if not title:
                    title = text
                else:
                    bodies.append(text)
            elif shape.shape_type == 13:  # PICTURE
                image = shape.image
                ext = image.ext
                fname = f"slide-{i:03d}-{len(images)}.{ext}"
                (assets / fname).write_bytes(image.blob)
                images.append({
                    "filename": fname,
                    "alt": "",
                })

        notes = ""
        if slide.has_notes_slide:
            notes = slide.notes_slide.notes_text_frame.text.strip()

        slides.append({
            "index": i,
            "title": title,
            "bodies": bodies,
            "notes": notes,
            "images": images,
        })

    (out / "extracted.json").write_text(json.dumps(slides, indent=2))
    print(f"Extracted {len(slides)} slides → {out}/extracted.json")
    print(f"Assets ({sum(len(s['images']) for s in slides)} images) → {assets}/")

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: extract_pptx.py <input.pptx> <output-dir>")
        sys.exit(1)
    extract(sys.argv[1], sys.argv[2])
```

Run:

```bash
python3 ~/Documents/slide-conversions/_scripts/extract_pptx.py \
  "<path-to-pptx>" \
  ~/Documents/slide-conversions/<slug>-from-pptx/
```

## Step 2 — Confirm summary with Corey

Read `extracted.json`. Present a one-line-per-slide summary:

```
Slide 1: "Title — Brand Name"
Slide 2: "Agenda" — 4 bullets
Slide 3: "Problem statement" — 2-paragraph body, 1 image
...
Slide 18: "Thank you" — speaker notes only
```

Get confirmation before generating the React file (the LLM should sanity-check, not assume the extraction is perfect — PPTX is messy).

## Step 3 — Map to React primitives

For each extracted slide, choose a primitive composition based on its shape:

| Extracted shape | React mapping |
|---|---|
| Title-only (no body) | Title slide pattern OR section divider |
| Title + 1 paragraph | `Heading + Body` |
| Title + bullet list (3–6 items) | `Heading + BulletList` |
| Title + 2 columns | `Heading + TwoCol` |
| Title + image, no body | `Heading + <img>` centered |
| Title + image + body | `TwoCol` with image on one side, body other |
| Big quote | Pull quote pattern (see `template.md`) |
| Final / thank-you slide | Close/CTA pattern |

## Step 4 — Generate the React file

Write to `${SLIDE_DECK_REPO:-$HOME/code/your-slide-deck-site}/src/app/slides/<slug>/`:
- `layout.tsx` (use the deck title from slide 1)
- `page.tsx` (full Slide[] array)

For images:
1. Copy from `~/Documents/slide-conversions/<slug>-from-pptx/assets/` to `${SLIDE_DECK_REPO:-$HOME/code/your-slide-deck-site}/public/slide-assets/<slug>/`
2. Reference in slides via `<img src="/slide-assets/<slug>/<filename>" alt="..." className="max-h-[60vh] mx-auto" />`

## Step 5 — Speaker notes

Speaker notes in the PPTX → `notes` array on the corresponding Slide. Split notes on sentence boundaries or empty lines; aim for 3–5 lines per slide per Corey's voice rules.

If a PPTX slide has no notes, generate 3 starter notes lines based on the slide's content. Mark these with a `// TODO: review` comment so Corey can refine in his voice.

## Step 6 — Apply voice + density rules

The extracted content is in whatever voice the original deck had — likely corporate. After mapping to primitives, do a voice pass:

- Apply Corey's anti-AI-slop rules (`references/narrative-and-voice.md`)
- Rewrite generic headings into specific, take-coded ones
- Trim wordy bullets — aim for 3–6 words each
- Honor the chosen density mode (speaker-led vs reading-first)

This is the most subjective step. When in doubt, show Corey the original and proposed rewrite side by side and let him pick.

## Step 7 — Archive the conversion

Keep the original PPTX + extracted JSON forever. Never modify the source.

```
~/Documents/slide-conversions/<slug>-from-pptx/
├── original.pptx          # untouched copy
├── extracted.json         # parsed structure
├── assets/                # images extracted from PPTX
│   └── slide-XXX-N.png
└── conversion-notes.md    # any decisions made during mapping (Corey-readable audit)
```

The audit lets future conversions of similar decks reuse the mapping decisions.
