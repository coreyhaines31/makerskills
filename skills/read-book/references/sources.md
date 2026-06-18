# Per-source ingestion

How to get usable text from each input type. Skill picks based on file extension or URL pattern.

---

## PDF

**Native path** — Claude's `Read` tool handles PDFs directly:

```
Read tool with file_path="<pdf>" pages="1-10"
```

Max ~10 pages per call. For longer books, chunk per the chunking plan.

**Get TOC + page count first:**

```bash
# Page count
pdfinfo "<pdf>" 2>/dev/null | awk '/^Pages:/ {print $2}'

# Outline / bookmarks (PDF TOC)
pdftk "<pdf>" dump_data 2>/dev/null | grep -A 2 "BookmarkTitle:" | head -50

# Or with mutool (faster, comes with mupdf):
mutool show "<pdf>" outline 2>/dev/null | head -50

# Fallback: scan the first 5 pages for "Contents" or "Table of Contents"
Read tool with file_path="<pdf>" pages="1-5"
```

**Scanned PDFs (no text layer):**

```bash
# Check if text exists
pdftotext -layout "<pdf>" - 2>/dev/null | wc -c
# If <1000 chars for a 100-page book, it's scanned. Need OCR:
brew install ocrmypdf
ocrmypdf "<pdf>" "<pdf-ocr.pdf>"
# Then proceed with the OCR'd version
```

---

## EPUB

Convert to markdown via pandoc (preserves chapter structure):

```bash
# Install once: brew install pandoc
pandoc "<book.epub>" -o "<workdir>/book.md" --wrap=none
```

The output has `# Chapter X` headers — easy to chunk.

For richer metadata + cover extraction, use calibre's `ebook-convert`:

```bash
# Install once: brew install calibre
ebook-convert "<book.epub>" "<workdir>/book.txt"
# Calibre also extracts metadata.opf alongside
```

---

## MOBI / AZW3

Use `ebook-convert` (calibre) — pandoc doesn't handle MOBI well:

```bash
ebook-convert "<book.mobi>" "<workdir>/book.epub"
# Then pandoc as above:
pandoc "<workdir>/book.epub" -o "<workdir>/book.md" --wrap=none
```

Or directly to txt:

```bash
ebook-convert "<book.mobi>" "<workdir>/book.txt"
```

---

## Markdown / .txt

Just `Read` it. No conversion. Chunk by character count (30K per chunk).

---

## Pasted text

Use what was pasted. Treat like a single chunk if short (<30K chars), or chunk by character count if long.

If Corey pastes only a section of a book ("read this chapter for me"), treat as 1-chunk and skip the per-chapter aggregation.

---

## URL (public-domain text)

```bash
# WebFetch the URL
# Project Gutenberg pattern: https://www.gutenberg.org/files/<id>/<id>-0.txt
# Archive.org pattern: https://archive.org/stream/<id>/<id>_djvu.txt
```

For Project Gutenberg, prefer the `.txt` URL over HTML — clean text, easy to chunk.

---

## Metadata extraction

For every source, extract these into the workdir's `metadata.json`:

```json
{
  "title": "<book title>",
  "author": "<author>",
  "year": "<year if available>",
  "source": "<original path or URL>",
  "type": "pdf" | "epub" | "mobi" | "markdown" | "text" | "url",
  "page_count": 287,
  "word_count": 95000,
  "has_toc": true,
  "captured_at": "YYYY-MM-DD"
}
```

For PDFs: `pdfinfo` gives title, author, page count out of the box.
For EPUB: `unzip -p <file> META-INF/container.xml` and the OPF file inside have full metadata.
For markdown/text: ask Corey for title + author if not in the filename.
