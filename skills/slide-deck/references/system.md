# Slide-deck system reference

Reference layout for the Next.js repo that hosts your branded React decks. Adopt the file structure below, then point `SLIDE_DECK_REPO` at your repo path.

## Locations

| What | Path |
|---|---|
| **Deck routes** | `${SLIDE_DECK_REPO:-$HOME/code/your-slide-deck-site}/src/app/slides/<slug>/page.tsx` |
| **Per-deck layout** | `${SLIDE_DECK_REPO:-$HOME/code/your-slide-deck-site}/src/app/slides/<slug>/layout.tsx` |
| **Shared primitives** | `${SLIDE_DECK_REPO:-$HOME/code/your-slide-deck-site}/src/components/slides/slide-primitives.tsx` |
| **SlideDeck component** | `${SLIDE_DECK_REPO:-$HOME/code/your-slide-deck-site}/src/components/slides/slide-deck.tsx` |
| **Sections types** | `${SLIDE_DECK_REPO:-$HOME/code/your-slide-deck-site}/src/components/slides/sections.ts` |
| **Brand gradients** | `${SLIDE_DECK_REPO:-$HOME/code/your-slide-deck-site}/src/lib/gradients.ts` (12 cycling, applied automatically) |
| **Existing decks (style refs)** | `${SLIDE_DECK_REPO:-$HOME/code/your-slide-deck-site}/src/app/slides/marketing-like-an-engineer/page.tsx`, `${SLIDE_DECK_REPO:-$HOME/code/your-slide-deck-site}/src/app/slides/skill-for-your-skills/page.tsx` |

## Imports a `page.tsx` typically needs

```typescript
"use client";

import { SlideDeck, type Slide } from "@/components/slides/slide-deck";
import type { SectionRange } from "@/components/slides/sections";
import {
  Eyebrow,
  Heading,
  Accent,
  Body,
  BulletList,
  Divider,
  TwoCol,
  GradientText,
} from "@/components/slides/slide-primitives";
```

Only import the primitives the deck actually uses.

## Primitives

| Primitive | Use | Notes |
|---|---|---|
| `<Eyebrow>` | Small all-caps label above a heading | Section tag, slide kind, "Keynote" / "Chapter 1" etc. |
| `<Heading>` | Slide-level header (`<h2>`-equivalent) | Most slides have one |
| `<Accent>` | Inline keyword styled with the slide's gradient | Use in `<h1>` or `<Heading>`. One per slide max. |
| `<GradientText>` | Same as Accent but takes `className` for custom layout | Use when `<Accent>` doesn't fit |
| `<Body>` | Paragraph text | Soft gray, max-width-2xl, relaxed leading |
| `<BulletList items={[]}>` | Tight 3–7 bullet list | Pass array of strings |
| `<Divider>` | Dashed horizontal rule | Use sparingly to break up content |
| `<TwoCol left={} right={}>` | Two-column grid | Comparison, before/after, problem/solution |

## Title-slide pattern (from `marketing-like-an-engineer`)

```tsx
{
  id: "title",
  content: (
    <div className="flex flex-col justify-center h-full max-w-3xl">
      <p className="text-sm uppercase tracking-[0.08em] font-heading font-medium text-[#4d4d4d]/40 mb-4">
        Keynote
      </p>
      <h1 className="font-heading font-medium text-[4.236rem] leading-[1.05] tracking-[-0.02em] text-[#4d4d4d] mb-6 text-balance">
        Marketing Like an <Accent>Engineer</Accent>
      </h1>
      <p className="text-[#4d4d4d]/50 text-xl font-heading">
        <SPEAKER_NAME>
      </p>
    </div>
  ),
  notes: [
    "Welcome everyone — excited to be here.",
    "This talk is about applying the engineering mindset to marketing.",
    "By the end you'll have a framework you can take home and start building Monday.",
  ],
}
```

Use this as the title slide template. Swap copy + adjust `<Accent>` to the topic's keyword.

## Slide type

```typescript
type Slide = {
  id: string;          // kebab-case, unique per deck (used for anchors)
  content: React.ReactNode;
  notes?: string[];    // 3–5 lines, complete spoken thoughts
};
```

## Sections type + pattern

```typescript
type SectionRange = { name: string; from: number; to: number };
```

`from` / `to` are **zero-indexed slide indices** (slide 1 = index 0).

Example from `marketing-like-an-engineer`:

```typescript
const sections: SectionRange[] = [
  { name: "Title", from: 0, to: 0 },
  { name: "Intro", from: 1, to: 4 },
  { name: "Takeaways", from: 5, to: 6 },
  { name: "Reframe marketing", from: 7, to: 11 },
  { name: "The system", from: 12, to: 18 },
  { name: "All roads lead to Rome", from: 19, to: 19 },
  { name: "Close", from: 20, to: 22 },
];
```

Sections drive the presenter view's "where am I" context. Use them for keynote-length decks. Optional for short decks.

## Component invocation

```tsx
export default function MyDeckPage() {
  return <SlideDeck slides={slides} sections={sections} />;
}
```

`sections` is optional.

## layout.tsx pattern

```tsx
import type { Metadata } from "next";

export const metadata: Metadata = {
  title: "<Deck Title>",
};

export default function <DeckName>Layout({
  children,
}: {
  children: React.ReactNode;
}) {
  return <>{children}</>;
}
```

The `title` becomes the browser tab title when presenting.

## Brand colors used in primitives

- **Text**: `#4d4d4d` (charcoal)
- **Muted text**: `#4d4d4d` with opacity (`/40`, `/45`, `/50`, `/70`, `/80`)
- **Font heading**: `font-heading` (custom class) for display sizes
- **Brand gradients**: 12 in rotation, applied automatically via CSS vars — don't hardcode gradient colors per slide

## Comment patterns from existing decks

Use these horizontal rules as section markers in the slides array — they make the file scan-able:

```typescript
// ─── Slides ───────────────────────────────────────────────────────────────────

// ═══════════════════════════════════════════════════════════════════════════
// ACT 1 — HOOK & FRAME
// ═══════════════════════════════════════════════════════════════════════════

// 1. Title
{ ... },

// 2. Surreal moment
{ ... },
```

Comments aren't strictly necessary but help when editing a 20+ slide deck.
