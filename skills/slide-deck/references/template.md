# File templates

Drop-in skeletons for `page.tsx` and `layout.tsx`. Substitute `<TOKENS>`.

---

## `layout.tsx`

```tsx
import type { Metadata } from "next";

export const metadata: Metadata = {
  title: "<DECK_TITLE>",
};

export default function <DeckNameCamelCase>Layout({
  children,
}: {
  children: React.ReactNode;
}) {
  return <>{children}</>;
}
```

---

## `page.tsx` — minimal (no sections)

```tsx
"use client";

import { SlideDeck, type Slide } from "@/components/slides/slide-deck";
import {
  Eyebrow,
  Heading,
  Accent,
  Body,
  BulletList,
} from "@/components/slides/slide-primitives";

// ─── Slides ───────────────────────────────────────────────────────────────────

const slides: Slide[] = [
  // 1. Title
  {
    id: "title",
    content: (
      <div className="flex flex-col justify-center h-full max-w-3xl">
        <p className="text-sm uppercase tracking-[0.08em] font-heading font-medium text-[#4d4d4d]/40 mb-4">
          <ROOM_KIND_OR_EYEBROW>
        </p>
        <h1 className="font-heading font-medium text-[4.236rem] leading-[1.05] tracking-[-0.02em] text-[#4d4d4d] mb-6 text-balance">
          <DECK_TITLE_LINE_1> <Accent><DECK_TITLE_KEYWORD></Accent>
        </h1>
        <p className="text-[#4d4d4d]/50 text-xl font-heading">
          <SPEAKER_NAME>
        </p>
      </div>
    ),
    notes: [
      "<OPENING_LINE>",
      "<ONE_LINE_FRAME>",
      "<WHY_THEY_SHOULD_CARE>",
    ],
  },

  // 2. <SLIDE_NAME>
  {
    id: "<slide-id>",
    content: (
      <div className="flex flex-col justify-center h-full max-w-3xl">
        <Eyebrow><SECTION_NAME></Eyebrow>
        <Heading><SLIDE_HEADLINE> <Accent>keyword</Accent></Heading>
        <Body>
          <PARAGRAPH>
        </Body>
      </div>
    ),
    notes: [
      "<OPENER>",
      "<POINT>",
      "<SUPPORT>",
      "<TRANSITION>",
    ],
  },

  // ... more slides
];

// ─── Page ─────────────────────────────────────────────────────────────────────

export default function <DeckNameCamelCase>Page() {
  return <SlideDeck slides={slides} />;
}
```

---

## `page.tsx` — with sections (keynote-length)

```tsx
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
} from "@/components/slides/slide-primitives";

// ─── Slides ───────────────────────────────────────────────────────────────────

const slides: Slide[] = [
  // (slides here — see minimal template)
];

// ─── Sections ─────────────────────────────────────────────────────────────────

const sections: SectionRange[] = [
  { name: "Title", from: 0, to: 0 },
  { name: "<SECTION_NAME>", from: 1, to: 4 },
  { name: "<SECTION_NAME>", from: 5, to: 11 },
  { name: "<SECTION_NAME>", from: 12, to: 18 },
  { name: "Close", from: 19, to: 22 },
];

// ─── Page ─────────────────────────────────────────────────────────────────────

export default function <DeckNameCamelCase>Page() {
  return <SlideDeck slides={slides} sections={sections} />;
}
```

---

## Slide primitives — common compositions

### Section divider (mid-deck)

```tsx
{
  id: "divider-<n>",
  content: (
    <div className="flex flex-col justify-center items-center h-full">
      <Eyebrow>Part <n></Eyebrow>
      <h2 className="font-heading font-medium text-[4rem] leading-[1.05] tracking-[-0.02em] text-[#4d4d4d] text-balance text-center max-w-3xl">
        <SECTION_TITLE>
      </h2>
    </div>
  ),
  notes: [
    "<TRANSITION_FROM_PREVIOUS_SECTION>",
    "<WHAT_WE'RE_ABOUT_TO_COVER>",
  ],
},
```

### Framework / bullet list

```tsx
{
  id: "<slide-id>",
  content: (
    <div className="flex flex-col justify-center h-full max-w-3xl">
      <Eyebrow><SECTION_NAME></Eyebrow>
      <Heading>The <Accent><N></Accent> things</Heading>
      <BulletList items={[
        "<bullet 1>",
        "<bullet 2>",
        "<bullet 3>",
      ]} />
    </div>
  ),
  notes: [
    "<OPENER>",
    "<POINT_ABOUT_THE_FRAMEWORK>",
    "<WHY_THIS_COUNT_MATTERS>",
    "<TRANSITION>",
  ],
},
```

### Two-column comparison

```tsx
{
  id: "<slide-id>",
  content: (
    <div className="flex flex-col justify-center h-full max-w-5xl">
      <Eyebrow><SECTION_NAME></Eyebrow>
      <Heading><SLIDE_HEADLINE></Heading>
      <TwoCol
        left={
          <>
            <p className="text-sm uppercase tracking-wider text-[#4d4d4d]/50 mb-2">Before</p>
            <Body><LEFT_CONTENT></Body>
          </>
        }
        right={
          <>
            <p className="text-sm uppercase tracking-wider text-[#4d4d4d]/50 mb-2">After</p>
            <Body><RIGHT_CONTENT></Body>
          </>
        }
      />
    </div>
  ),
  notes: [
    "<OPENER>",
    "<LEFT_SIDE_EXPLAINED>",
    "<RIGHT_SIDE_EXPLAINED>",
    "<THE_DIFFERENCE_THAT_MATTERS>",
  ],
},
```

### Pull quote / standout

```tsx
{
  id: "<slide-id>",
  content: (
    <div className="flex flex-col justify-center h-full max-w-3xl">
      <p className="text-[2.618rem] leading-[1.15] font-heading font-light text-[#4d4d4d] text-balance">
        "<QUOTE_TEXT>"
      </p>
      <p className="text-[#4d4d4d]/50 text-base mt-6 font-heading">— <ATTRIBUTION></p>
    </div>
  ),
  notes: [
    "<WHY_THIS_QUOTE>",
    "<WHAT_IT_REVEALS>",
  ],
},
```

### Close / CTA

```tsx
{
  id: "close",
  content: (
    <div className="flex flex-col justify-center h-full max-w-3xl">
      <Eyebrow>Close</Eyebrow>
      <Heading>One thing to <Accent>do Monday</Accent></Heading>
      <Body>
        <ONE_SENTENCE_CTA>
      </Body>
      <p className="text-[#4d4d4d]/40 text-base mt-12 font-heading">
        <AUTHOR_HANDLE> · <AUTHOR_SITE>
      </p>
    </div>
  ),
  notes: [
    "<RECAP_THE_TAKE>",
    "<THE_ONE_ACTION>",
    "<HOW_TO_REACH_ME>",
    "<THANK_THE_AUDIENCE>",
  ],
},
```
