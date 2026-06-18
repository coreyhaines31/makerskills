# Output mode templates

Per-mode templates for the final aggregated `notes.md`. Each chapter chunk produces a partial in the same shape, then the aggregator combines them.

---

## notes (default)

Best for: reading nonfiction you want to refer back to.

### Per-chunk template

```markdown
### Chapter <N>: <Chapter Title>

**TL;DR**: <2–3 sentence summary>

**Key concepts**:
- **<concept>** — <1-line explanation>
- **<concept>** — <1-line explanation>
- (3–7 per chapter, no more)

**Quotes worth keeping**:
> "<verbatim quote>" (p. X)
> "<verbatim quote>" (p. Y)

**Action items / Implications**:
- <if I believed this chapter, what would I do differently?>
- <thing to try / experiment to run>

**Frameworks introduced**:
- **<Framework name>**: <1-sentence summary of the structure>

**Open questions / disagreements**:
- <where I push back or want more evidence>
```

### Full-book aggregation

```markdown
# <Book Title> by <Author>

## TL;DR
<2–3 sentences synthesizing the whole book>

## Key takeaways
1. <takeaway>
2. <takeaway>
3. <takeaway>
(3–7 total — the things that survive forgetting)

## Who this is for
<1 sentence>

## Verdict
<recommend? skip? read in this order with other books?>

## Chapter notes
<all per-chunk outputs concatenated>

## Cross-references (suggested for wiki)
- Could connect to [[<existing wiki page>]] (per <chapter ref>)
- Could connect to [[<existing wiki page>]] (per <chapter ref>)

## Source
- File: <path>
- Author: <author>
- Pages: <count>
- Read on: <date>
- Mode: notes
```

---

## summary

Best for: short attention, "did I miss anything important," catching up before a meeting.

### Single-pass template (no per-chunk aggregation)

```markdown
# <Book Title> by <Author> — Summary

**TL;DR (1 paragraph)**: <4–6 sentences>

**Key takeaways**:
1. <takeaway>
2. <takeaway>
3. <takeaway>
(3–5 total, not more)

**Who this is for**: <1 sentence>

**Should you read the whole thing?** <yes / no / just chapters X and Y>

**Source**: <path>, <author>, <pages> pages, read on <date>
```

For books over 100 pages, sample chapters (read intro + 2–3 random middle chapters + conclusion) rather than full chunking — summary doesn't justify full processing.

---

## quotes

Best for: pull-quote mining for talks, social, content drafting.

### Per-chunk template

```markdown
### Chapter <N>: <Chapter Title>

> "<verbatim quote>" — <attribution if not the author> (p. X)
> "<verbatim quote>" — (p. Y)
> "<verbatim quote>" — (p. Z)

(5–15 per chapter for quote-heavy books; 0–3 for sparse chapters — only the keepers)
```

### Full-book aggregation

```markdown
# <Book Title> by <Author> — Quotes

<all quotes from all chunks, grouped by chapter, with page refs>

## Source
- File: <path>
- Read on: <date>
```

No analysis, no commentary — pure verbatim quotes. If you want analysis, use `notes` mode.

---

## study

Best for: deep learning, books you want to retain long-term, prep for talks/teaching.

### Per-chunk template

Notes-mode output + add:

```markdown
**Spaced-repetition Q&A**:
1. **Q**: <question that tests recall of a key concept>
   **A**: <1–2 sentence answer>
2. **Q**: <question>
   **A**: <answer>
(2–4 Q&A pairs per chapter)
```

### Full-book aggregation

Notes-mode aggregation + add at the end:

```markdown
## Spaced-repetition deck (full)

<all Q&A pairs from all chapters, in order, ready to import to Anki/Mochi/RemNote>

## Suggested review cadence
- Week 1: review all Q&A daily
- Week 2-4: every other day
- After that: standard SRS schedule
```

The Q&A format makes the output directly importable to spaced-repetition apps. If Corey wants Anki-importable TSV, add a `--anki` flag (one Q-tab-A per line).

---

## Notes shared across modes

- **Quote attribution**: when the author quotes someone else, the attribution goes after the quote (`— Andy Wilkinson`). When it's the author themselves, no attribution needed.
- **Page numbers**: always include if available. For EPUB-converted books without stable page numbers, use chapter + paragraph approximation (`Ch 3, ¶12`).
- **Frameworks** in the `notes` mode get their own bullet because they're the most reusable — a framework you remember outperforms 10 ideas you forget.
- **Disagreements / pushback** in `notes` mode is mandatory if you have any. Reading critically beats reading reverently — surface the friction.
