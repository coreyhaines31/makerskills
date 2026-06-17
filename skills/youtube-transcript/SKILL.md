---
name: youtube-transcript
description: When Corey wants to extract a clean transcript from a YouTube video — pasted URL, short URL (youtu.be), or video ID. Uses yt-dlp to pull auto-generated or manual subtitles, cleans the VTT to plain text (default), markdown, or JSON. Also pulls metadata (title, channel, duration, upload date, chapters). Saves to a generic workdir at ~/Documents/transcripts/<channel>-<slug>-<date>/ so other skills can reference. Triggers on "/youtube-transcript," "/yt-transcript," "transcript for [url]," "transcribe this video," "pull the transcript from," "youtube transcript." This is a pure utility — cf-skills:cf-blog, cf-skills:swipefiles, deep-research, and business-brainstorm should call this skill instead of running yt-dlp inline.
metadata:
  version: 0.1.0
---

# /youtube-transcript — Extract clean YouTube transcripts

Pure utility. Hands back clean text + metadata; opinions about what to do next belong in the calling skill.

## Step 1 — Parse input

Accept any of:
- Full URL: `https://www.youtube.com/watch?v=<id>`
- Short URL: `https://youtu.be/<id>`
- Shorts URL: `https://www.youtube.com/shorts/<id>`
- Raw ID: `<id>` (11 chars, alphanumeric + `_-`)

Normalize to canonical form: `https://www.youtube.com/watch?v=<id>`

## Step 2 — Pull metadata

Run:

```bash
yt-dlp --print "%(title)s|%(channel)s|%(duration_string)s|%(upload_date>%Y-%m-%d)s|%(description)s" --print "%(chapters)j" --skip-download "<url>"
```

Capture:
- **title**
- **channel** (used in workdir slug)
- **duration_string** (HH:MM:SS or MM:SS)
- **upload_date** (YYYY-MM-DD)
- **description** (first paragraph)
- **chapters** (JSON array: `[{start_time, end_time, title}, ...]` or null)

## Step 3 — Build the workdir

Slug components:
- `channel`: kebab-case the channel name
- `slug`: kebab-case the first 4–6 words of the title (max 50 chars)
- `date`: `YYYY-MM-DD`

Workdir path: `~/Documents/transcripts/<channel>-<slug>-<date>/`

Create if missing. If it already exists (re-runs), reuse it and overwrite.

## Step 4 — Pull the transcript

Prefer manual subs over auto-generated when both exist:

```bash
yt-dlp --write-sub --write-auto-sub --skip-download \
  --sub-lang en --sub-format vtt \
  -o "<workdir>/transcript" \
  "<url>"
```

If `en` subs don't exist, fall back: try the original language (yt-dlp will pick), then any. If nothing is available, report: *"No subtitles or auto-captions available for this video."* and stop.

Result: a `.vtt` file in the workdir (manual preferred filename: `transcript.en.vtt`; auto-generated: `transcript.en.vtt` as well — yt-dlp writes the same name).

## Step 5 — Clean the VTT

YouTube auto-subs have rolling captions: each cue repeats text from the previous cue + adds a few words. Naïve concatenation produces 5× the actual content.

**Cleaning rules:**
1. Strip WEBVTT header, `Kind:`, `Language:`, `NOTE`, position/styling tags
2. Strip timestamp lines (`00:00:00.000 --> 00:00:03.000`)
3. Strip inline tags (`<c>`, `</c>`, `<00:00:01.000>`, etc.)
4. **De-duplicate the rolling captions**: for each cue block, keep only the last (most complete) line; or process line-by-line and only keep text that didn't appear in the previous cue
5. Collapse multiple spaces, normalize line endings, trim
6. Paragraph-break on cue gaps >2 seconds (silence) OR on chapter boundaries (if chapters exist)

The cleaning can be done with `awk`/`sed`/`python3` — pick whatever is cleanest. A starter pipeline that handles most YouTube auto-sub patterns:

```bash
# Strip headers, timestamps, tags; take last line of each cue block
awk '
  /^WEBVTT/ || /^Kind:/ || /^Language:/ || /^NOTE/ { next }
  /-->/ { in_cue = 1; last = ""; next }
  /^$/ { if (last) print last; in_cue = 0; last = ""; next }
  in_cue { gsub(/<[^>]+>/, "", $0); last = $0 }
  END { if (last) print last }
' "<workdir>/transcript.en.vtt" \
  | awk '!seen[$0]++' \
  > "<workdir>/transcript.txt"
```

This is "good enough" for most videos. For pathological cases (heavy overlapping), Claude should inspect the output and re-clean with a smarter approach (e.g., compare each line to a sliding window of previous lines, drop strict prefixes).

## Step 6 — (Optional) paragraph segmentation

If the cleaned text is one wall of text, segment into paragraphs by:
1. Chapter boundaries (if chapters exist) — paragraph break + chapter title as a `## <chapter>` header (markdown only)
2. Cue gap >2s (silence) — paragraph break
3. Every ~150 words as fallback

## Step 7 — Format output

Pick from these formats (default = **plain**):

### plain (default)
- Pure text, paragraph breaks, no metadata header
- Write to `<workdir>/transcript.txt`

### markdown
- YAML frontmatter with metadata
- Chapter headers (`##`) if chapters exist
- Paragraph segmentation
- Write to `<workdir>/transcript.md`

```markdown
---
title: <title>
channel: <channel>
url: <url>
duration: <hh:mm:ss>
upload_date: <YYYY-MM-DD>
extracted: <YYYY-MM-DD>
---

# <title>

## <chapter 1 title>
<paragraphs>

## <chapter 2 title>
<paragraphs>
```

### json
- Structured output, machine-readable
- Write to `<workdir>/transcript.json`

```json
{
  "video": { "id": "...", "url": "...", "title": "...", "channel": "...", "duration_seconds": 1234, "upload_date": "2026-06-01" },
  "chapters": [{"start": 0, "end": 120, "title": "Intro"}, ...],
  "transcript": {
    "plain": "...",
    "segments": [{"start": 0, "end": 120, "text": "..."}, ...]
  }
}
```

### timestamps (optional add-on to plain or markdown)
- If user asks for timestamps, prepend each paragraph with `[hh:mm:ss] `
- Useful when the calling skill wants to identify specific moments (e.g., cf-skills clip extraction)

## Step 8 — Report

Print to chat:
- One-line summary: title, channel, duration, word count
- Workdir path
- Files written
- First 200 chars of transcript as a sanity check

If the calling skill needs the transcript inline, return the path so it can `Read` it.

## Files written to workdir

```
~/Documents/transcripts/<channel>-<slug>-<date>/
├── transcript.txt        # cleaned plain (always)
├── transcript.en.vtt     # raw VTT (kept for debugging / re-clean)
├── metadata.json         # parsed metadata
├── transcript.md         # only if format=markdown
└── transcript.json       # only if format=json
```

## Error handling

| Failure | Response |
|---|---|
| Video unavailable / private / age-restricted | Report and stop. No retry. |
| No subtitles in any language | Report and stop. Suggest: paste a manual transcript, or use Whisper (out of scope for this skill). |
| yt-dlp binary missing | Tell Corey: `brew install yt-dlp` |
| VTT cleaning produced empty output | Surface raw VTT for inspection; ask if Corey wants to retry with a different language or format. |

## Composes with

- `cf-skills:cf-blog` — should call this to get the transcript, then do its own topic-extraction + drafting
- `cf-skills:swipefiles` — same pattern
- `deep-research` — when a YouTube URL is a source, call this to add the transcript to the corpus
- `business-brainstorm` — for researching a market via founder/operator interviews on YouTube
- `paste` — if Corey pastes a YouTube URL with `/paste`, optionally route through this skill first
