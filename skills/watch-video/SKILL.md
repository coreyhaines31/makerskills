---
name: watch-video
description: When Corey wants to extract content from a video — YouTube, Loom, Vimeo, Riverside, Zoom recording, local MP4, X/IG video, anything yt-dlp supports. Three depth modes user picks per invocation — transcript (just words, fast/free), visual (transcript + ffmpeg frame extraction + Claude vision pass on key moments), multimodal (Gemini native video ingestion if $GEMINI_API_KEY set, else dense Claude vision). Uses MLX-Whisper local on Mac for transcription, falls back to platform-provided transcripts when available (Loom, Riverside, YouTube auto-subs). Saves to ~/Documents/videos/<source>-<slug>-<date>/ and optionally captures summary to second-brain raw/ as call-/meeting-/note-. Triggers on "/watch-video <url>," "watch this video," "transcribe this loom," "analyze this video," "summarize this recording," "key moments from this," "what happened in this video." This skill replaces and broadens the prior youtube-transcript skill.
metadata:
  version: 0.2.1
---

# /watch-video — Transcribe and analyze any video at the depth you choose

Replaces and broadens the prior `youtube-transcript` skill. YouTube is now one of many sources; depth is user-controlled.

## Step 1 — Parse input

Accept:
- **YouTube**: full URL, `youtu.be/<id>`, `youtube.com/shorts/<id>`, raw 11-char ID
- **Loom**: `loom.com/share/<id>` or `loom.com/embed/<id>`
- **Vimeo**: `vimeo.com/<id>`
- **Riverside**: download URL or local file
- **Zoom**: local `.mp4` from a downloaded recording
- **X / IG / TikTok video**: URL — defers to `social-fetch` for metadata, uses yt-dlp for the file
- **Local file**: any path to an `.mp4` / `.mov` / `.webm` / `.mkv`

Detect source from URL pattern or file extension. If ambiguous, ask.

## Step 2 — Parse depth mode

| Invocation | Mode | What you get |
|---|---|---|
| `/watch-video <url>` | **transcript** (default) | Clean text, metadata, optional chapters |
| `/watch-video <url> transcript` | transcript | Same as default |
| `/watch-video <url> visual` | visual | Transcript + frames at intervals + Claude vision pass identifying key moments |
| `/watch-video <url> multimodal` | multimodal | Native video to Gemini (if `$GEMINI_API_KEY`), else dense Claude vision frame-by-frame |

If the depth isn't specified and the video is >10 minutes, ask before defaulting (visual/multimodal cost real money on long videos).

## Step 3 — Pull metadata

For URL sources, use yt-dlp:

```bash
yt-dlp --print "%(title)s|%(uploader)s|%(duration_string)s|%(upload_date>%Y-%m-%d)s|%(description)s" \
  --print "%(chapters)j" --skip-download "<url>"
```

Capture: title, uploader/channel, duration, upload date, description (first paragraph), chapters (JSON or null).

For local files, use ffprobe:

```bash
ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 "<file>"
```

## Step 4 — Build workdir

```
~/Documents/videos/<source>-<slug>-<date>/
```

Where:
- `source`: `youtube` / `loom` / `vimeo` / `riverside` / `zoom` / `local`
- `slug`: kebab-case of title (first 4–6 words, max 50 chars)
- `date`: `YYYY-MM-DD`

## Step 5 — Get the transcript

**Backend selection** (in order):

1. **Platform-provided transcript** if it exists and looks complete:
   - YouTube: `yt-dlp --write-sub --write-auto-sub --skip-download --sub-lang en --sub-format vtt`
   - Loom: fetch via `https://www.loom.com/share/<id>` page metadata or Loom API if `$LOOM_API_KEY` set
   - Riverside: built-in transcripts available on the recording's share page
   - If platform transcript exists and has timestamps, use it. Skip Whisper.

2. **MLX-Whisper local** (default fallback — fast on Mac M-series):
   ```bash
   # Install once: pip install mlx-whisper
   python3 -c "import mlx_whisper; mlx_whisper.transcribe('<file>', path_or_hf_repo='mlx-community/whisper-large-v3-turbo')" \
     > "<workdir>/transcript-raw.json"
   ```
   Or via the CLI: `mlx_whisper <file> --model mlx-community/whisper-large-v3-turbo --output-dir <workdir>`

3. **whisper.cpp** (further fallback if MLX unavailable)

Download the video file first if it's a URL (use yt-dlp; Loom/Vimeo/YT all supported):

```bash
yt-dlp -f "bv*[height<=720]+ba/b[height<=720]" -o "<workdir>/video.%(ext)s" "<url>"
```

720p is plenty for transcription and frame analysis (smaller download, faster processing).

**Clean the transcript** (only needed for YouTube auto-subs which have rolling captions; Whisper output is already clean):

```bash
# YouTube VTT cleanup — de-dup rolling captions, strip tags, paragraph-break on cue gaps >2s
awk '
  /^WEBVTT/ || /^Kind:/ || /^Language:/ || /^NOTE/ { next }
  /-->/ { in_cue = 1; last = ""; next }
  /^$/ { if (last) print last; in_cue = 0; last = ""; next }
  in_cue { gsub(/<[^>]+>/, "", $0); last = $0 }
  END { if (last) print last }
' "<workdir>/transcript.en.vtt" | awk '!seen[$0]++' > "<workdir>/transcript.txt"
```

Save final to `<workdir>/transcript.txt`.

## Step 6 — If `transcript` mode: stop here

Output:
- `transcript.txt`
- `metadata.json`
- One-line summary in chat: title, source, duration, word count
- Path to workdir
- (Optional) Step 9 — offer to capture to second-brain

## Step 7 — If `visual` mode: extract frames + vision pass

### Frame extraction (ffmpeg)

Cadence by source heuristic:

| Source type | Frame cadence |
|---|---|
| Screen-share / Loom / demo | 1 frame per **5s** (UI changes fast) |
| Talking head / podcast | 1 frame per **30s** (slow change) |
| Slide presentation | 1 frame per **10s** + force a frame on each detected scene change |
| Default if unsure | 1 frame per **15s** |

```bash
mkdir -p "<workdir>/frames"
ffmpeg -i "<workdir>/video.mp4" -vf "fps=1/15" "<workdir>/frames/frame-%04d.png" -y
```

For scene-change detection (slide decks especially):

```bash
ffmpeg -i "<workdir>/video.mp4" -vf "select='gt(scene,0.3)',showinfo" -vsync vfr "<workdir>/frames/scene-%04d.png" 2> "<workdir>/scene-detection.log"
```

### Vision pass

Pair each frame with the transcript chunk for the same timestamp window. Then batch-send to Claude vision for synthesis.

**Per-frame batch prompt** (up to ~10 frames per call):

> Here are N frames from a video at timestamps T1..TN. For each frame, describe what's on screen in 1–2 sentences. Flag: (a) UI changes from previous frame, (b) text visible on screen, (c) any moment that looks like a decision, action, or notable event. Also note the transcript text spoken during this window.

Save the output as `<workdir>/moments.md`:

```markdown
# Key moments — <title>

## 00:00:15 (frame-001.png)
**On screen**: Login form, email field focused
**Transcript**: "So you just open it up and..."
**Note**: Beginning of UI demo

## 00:00:45 (frame-002.png)
**On screen**: Dashboard with 4 cards
**Transcript**: "And here's where you see all your projects."
**Note**: Major view change — first time the dashboard appears
```

### Generate summary

After moments are identified, synthesize the whole video into `<workdir>/summary.md`:

```markdown
# Summary — <title>

**Source:** <source URL / file>
**Duration:** <hh:mm:ss>
**Watched at:** <date>
**Mode:** visual

## TL;DR
<2–4 sentences>

## Key moments
- 00:00:15 — <one-line>
- 00:00:45 — <one-line>

## Action items flagged
- <item> [timestamp]

## Decisions flagged
- <decision> [timestamp] — consider routing to /decide

## Quotes worth keeping
- "..." [timestamp]

## Open questions
- <question raised but not answered>
```

## Step 8 — If `multimodal` mode

### Backend selection

1. **Gemini native** if `$GEMINI_API_KEY` is set (much cheaper + faster than per-frame for long videos):
   ```bash
   # Upload via Files API
   curl -X POST "https://generativelanguage.googleapis.com/upload/v1beta/files?key=$GEMINI_API_KEY" \
     -H "X-Goog-Upload-Command: start, upload, finalize" \
     -H "Content-Type: video/mp4" \
     --data-binary "@<workdir>/video.mp4"
   # Get file URI from response, then call generateContent with file_data + text prompt
   ```

2. **Dense Claude vision fallback** if no Gemini key:
   - Frame cadence: 1 frame per **3s** (much denser than visual mode)
   - Batch through Claude vision with the multimodal-analysis prompt
   - Slower and more expensive than Gemini for long videos — warn Corey before running on >10min content

### Multimodal output

Same `summary.md` template as Step 7 + an extended section:

```markdown
## Multimodal observations
- **Body language / delivery**: <observations on talking-head video>
- **Pacing**: <fast/slow/uneven>
- **Visual style**: <brand audit, ad review, design observations>
- **Audio quality / atmosphere**: <music, silence, background>
```

Exact extra sections depend on the use case (brand audit, ad review, talk delivery review, client-call read). Use case is inferred from the source + the user's verbal framing when invoking.

## Step 9 — Optional: capture to second-brain

After any mode completes, offer:

> *"Want to capture this to second-brain? I'll write a `call-<slug>.md` (or `meeting-` / `note-` / `resource-`) to `~/SecondBrain/raw/` with the summary, source URL, and transcript link."*

Type prefix by source:

| Source | Prefix |
|---|---|
| Loom / Zoom / Riverside / Otter / call recording | `call-` |
| Meeting (own notes, not a transcript) | `meeting-` |
| Talk / keynote / conference | `note-` |
| Ad / landing-page video / marketing reference / competitor video | `resource-` |

File body: 1-line source, the summary, link to full workdir.

## Step 10 — Report

In chat:

- One-line headline: `<source> · <title> · <duration> · <mode> · <word count> words`
- Workdir path
- For `visual` / `multimodal`: brief list of top 3 key moments
- For all modes: any action items / decisions flagged for triage
- If captured to second-brain: that path too

## Sources reference

| Source | Download | Built-in transcript | Notes |
|---|---|---|---|
| YouTube | `yt-dlp` | Auto-subs (`--write-auto-sub`) | Same as the prior youtube-transcript skill |
| Loom | `yt-dlp` (Loom supported) | Yes — fetch via embed metadata or Loom API | Async screenshare focus — prime use case |
| Vimeo | `yt-dlp` | Sometimes | Marketing/embed videos |
| Riverside | Direct URL from export, or local file | Yes — Riverside generates them | Factory Floor pod episodes |
| Zoom | Local `.mp4` (downloaded recordings) | Sometimes (Zoom audio transcript file) | Client calls |
| X / IG / TikTok | Defer to `social-fetch` for metadata, yt-dlp for file | No | Short-form |
| Local file | n/a | n/a | Drop a path |

## Composes with

- `social-fetch` — for X/IG/TikTok URL metadata (engagement, author, replies) before video processing
- `second-brain` — capture summary as `raw/call-<slug>.md`, `meeting-`, `note-`, or `resource-` per source type
- `decide` — when a video contains a flagged decision, route to `/decide` for structured capture
- `pm` — action items flagged in summary can be triaged to project boards
- `cf-blog` (in `cf-skills`) — Factory Floor episodes: this skill replaces inline yt-dlp; outputs feed cf-blog's draft pipeline
- `slide-deck` — talk recordings → outline extraction → deck draft (loop)
- `my-social` — quotes + clip-worthy moments from podcast/talk videos feed BIP/promo posts

## Error handling

| Failure | Response |
|---|---|
| Video unavailable / private / region-locked | Report and stop |
| No subtitles + Whisper not installed | Tell Corey: `pip install mlx-whisper` (Mac) |
| ffmpeg missing (for visual/multimodal) | Tell Corey: `brew install ffmpeg` |
| Vision pass returns empty / unclear | Lower the frame count, retry, or fall back to transcript-only with a note |
| Multimodal requested but no `$GEMINI_API_KEY` and >30min video | Warn cost, offer to fall back to visual mode |
| `yt-dlp` binary missing | `brew install yt-dlp` |
