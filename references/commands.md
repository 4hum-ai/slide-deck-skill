# Python Commands and API Scripts

All operational tooling in this skill is Python.

## Authentication

```bash
python scripts/auth.py
```

Credentials are saved to `~/.open-academy/config.json`.

Environment overrides:

| Variable | Purpose |
|---|---|
| `OPEN_ACADEMY_TOKEN` | API token override |
| `OPEN_ACADEMY_WORKSPACE_ID` | Workspace UUID override |
| `OPEN_ACADEMY_API_URL` | API base URL |
| `OPEN_ACADEMY_APP_URL` | App base URL |

## Validate

```bash
python examples/agent_skills_marketplace.py | python scripts/deck_validator.py
```

`save_deck.py` also runs this validator automatically before auth/network calls.

## Save

```bash
python scripts/save_deck.py "My Deck Title" < deck.json
```

Prints JSON to stdout (human-readable lines go to stderr):

```text
{"deck_id":"<id>","deck_url":"https://deck.4hum.ai/app/decks/<id>/edit"}
```

## Update

```bash
python scripts/update_deck.py "<deck-id>" < deck.json
```

## Generate Image

```bash
python scripts/generate_image.py "Futuristic server room, dark neon lighting" --size 1920x1080
```

Use the returned `file_url` as an image object's `src`.

## Generate Video

```bash
python scripts/generate_video.py "PROMPT" [--size 1280x720] [--duration 5] [--provider qwen]
```

Prints JSON to stdout: `{"media_id":"...","file_url":"...","duration_seconds":5}`  
Use `file_url` as the `src` field on a `video` object. Always also layer an `image()` at the same position as a poster fallback (VideoRenderer shows an error box in headless — see objects-guide.md).

**Provider / size / duration options:**

| Provider | `--provider` | Best sizes | Durations | Credits/sec |
|---|---|---|---|---|
| Qwen Wan 2.2 (default) | `qwen` | 1280x720, 1920x1080 | 5s | 2 |
| BytePlus Seedance | `byteplus` | 1280x720, 1920x1080 | 5s, 10s | 2 |
| OpenAI Sora 2 | `openai` | 1280x720 | 4s, 8s, 12s | 5 |
| Google Veo 3 | `gemini-veo` | 1280x720, 1920x1080 | 8s (fixed) | 8 |

**Image-to-video** (animate from a still image):
```bash
python scripts/generate_video.py "PROMPT" --image https://your-image-url.png
```

**Typical workflow for a video slide:**
```python
# 1. Generate a poster image (used as visual fallback in headless):
poster = run("python scripts/generate_image.py 'POSTER PROMPT' --size 1280x720")
poster_url = json.loads(poster)["file_url"]

# 2. Generate the video:
vid = run("python scripts/generate_video.py 'VIDEO PROMPT' --size 1280x720 --duration 5")
video_url = json.loads(vid)["file_url"]

# 3. In the slide JSON — image behind, video on top:
objects = [
    image(poster_url, x=200, y=200, w=1080, h=608),   # always visible (headless fallback)
    video(src=video_url, x=200, y=200, w=1080, h=608,
          poster=poster_url, controls=True),            # plays in production browser
]
```

Rate limit: allow ~30s between `generate_video` calls to avoid 429 errors.

## Background Music (Deck-level)

```bash
# Add from a URL (royalty-free MP3 recommended):
python scripts/set_deck_music.py <deck-id> --url "https://…/music.mp3" \
    --loop --volume 0.15 --name "Background music"

# Pipe generate_audio.py output as ambient track:
python scripts/generate_audio.py "Ambient text…" --voice-id <uuid> | \
    python scripts/set_deck_music.py <deck-id> --add-track - --loop --volume 0.12

# List current deck mediaTracks:
python scripts/set_deck_music.py <deck-id> --list

# Remove all tracks:
python scripts/set_deck_music.py <deck-id> --clear

# Remove a specific track by id:
python scripts/set_deck_music.py <deck-id> --remove-track <track-uuid>
```

**DeckMediaTrack fields:**

| Field | Default | Notes |
|---|---|---|
| `url` | — | Required. MP3/WAV/MP4 direct file URL |
| `loop` | `false` | Set `true` for music beds that fill the full deck duration |
| `volume` | `1.0` | Gain 0.0–1.0. Use 0.1–0.2 to keep music under narration |
| `startMs` | `0` | Offset from deck start in ms |
| `name` | — | Label shown in the timeline UI |
| `kind` | `"audio"` | `"audio"` or `"video"` (for video overlays) |

**Typical pattern — ambient bed under narration:**
```bash
# 1. Generate ambient audio at slow pace:
python scripts/generate_audio.py "Slide Deck Agent. Building with precision." \
    --default-voice --speed 0.75 > ambient.json

# 2. Add as looping background at 12% volume:
python scripts/set_deck_music.py <deck-id> --add-track ambient.json \
    --loop --volume 0.12 --name "Ambient bed"
```

Note: For real background music, use royalty-free audio from a direct MP3 URL.
TTS tracks at low volume and slow speed work as atmospheric narration beds,
not as music. A music generation endpoint is on the roadmap.

## Generate Audio

```bash
# List available voices first:
python scripts/generate_audio.py --list-voices

# Generate narration with a specific voice:
python scripts/generate_audio.py "Quantum entanglement links two particles." --voice-id <uuid>

# Use the first available system voice (quick prototyping):
python scripts/generate_audio.py "Text here." --default-voice

# Read from stdin (long scripts):
echo "Long narration text…" | python scripts/generate_audio.py --voice-id <uuid>

# Speed control (0.5 = slow, 1.0 = normal, 2.0 = fast):
python scripts/generate_audio.py "Text." --voice-id <uuid> --speed 0.85
```

Prints JSON to stdout: `{"audio_url":"...","duration_ms":4800,"voice_id":"...","text_hash":"..."}`

**Attaching to a slide (two patterns):**

Pipe directly to `patch_slide.py` — `patch_slide` auto-converts the audio output format to a `NarrationTrack`:
```bash
python scripts/generate_audio.py "Slide 2 narration." --default-voice | \
  python scripts/patch_slide.py <deck-id> 1 --add-narration-track -
```

Save and attach in two steps:
```bash
python scripts/generate_audio.py "Narration…" --voice-id <uuid> > audio.json
python scripts/patch_slide.py <deck-id> 1 --add-narration-track audio.json
```

**Text limits:** 1–8 000 characters per call. For longer narration, split across slides and generate separately.

**Typical narration workflow:**
```python
# In your generator — compute narration text per slide:
NARRATIONS = [
    "Welcome to the deck. Today we cover quantum computing fundamentals.",
    "A qubit differs from a classical bit because it can exist in superposition.",
    "Quantum entanglement links two particles regardless of distance.",
]

# After saving the deck, attach narration tracks:
result = save_deck(deck)
deck_id = result["deck_id"]

for slide_idx, narration_text in enumerate(NARRATIONS):
    audio = run(f'python scripts/generate_audio.py "{narration_text}" --default-voice')
    audio_data = json.loads(audio)
    run(f"python scripts/patch_slide.py {deck_id} {slide_idx} "
        f"--add-narration-track '{json.dumps(audio_data)}'")
```

## Preview / Inspect

```bash
# Fetch a saved deck by ID and print a per-slide structural summary:
python scripts/preview_deck.py "<deck-id>"

# Include WCAG contrast check for the theme:
python scripts/preview_deck.py "<deck-id>" --theme-check

# Inspect fresh JSON from a generator without saving:
python my_generator.py | python scripts/preview_deck.py
```

The script prints:
- Theme name + WCAG contrast report (with `--theme-check`)
- Per-slide: headline text, object-type counts (e.g. `2×text  1×image  1×chart`)
- Bounding-box warnings (non-positive sizes, canvas overflow)
- Edit URL
- **Per-slide render URLs** for browser-based screenshot evaluation:
  `https://deck.4hum.ai/slides/<deck-id>/<n>/render`

### Screenshot slides to PNG

`scripts/screenshot_slides.py` captures all slides (or a specific range) to PNG files
against the **production render route** at `https://deck.4hum.ai` (no local dev server needed).
Auth is read from `~/.open-academy/config.json` (run `python scripts/auth.py` to sign in first).

**One-time setup:**
```bash
pip install playwright
python -m playwright install chromium
```

**Capture all slides:**
```bash
python scripts/screenshot_slides.py <deck-id> <slide-count> <output-dir>
```

**Capture from slide N onwards (0-based):**
```bash
python scripts/screenshot_slides.py <deck-id> <slide-count> <output-dir> --start 5
```

**Capture specific slide indices only:**
```bash
SLIDE_INDICES=0,3,9 python scripts/screenshot_slides.py <deck-id> <slide-count> <output-dir>
```

Prints `SAVED:<path>` on stdout for each captured file; all progress and warnings go to stderr.
Exit code 2 if zero slides were saved (auth failure, wrong deck ID).

Auth and API env overrides:

| Variable | Purpose |
|---|---|
| `OPEN_ACADEMY_TOKEN` | Override the token from config |
| `OPEN_ACADEMY_API_URL` | Override the API host used for route interception |
| `SLIDE_INDICES` | Comma-separated 0-based indices to capture |

### Visual evaluation via browser tools

Each render URL renders a single slide at 1920×1080 with no chrome:

```
1. mcp__claude-in-chrome__navigate  → https://deck.4hum.ai/slides/<id>/<n>/render
2. mcp__claude-in-chrome__javascript_tool → wait for renderReady signal:
   await new Promise(r => {
     const iv = setInterval(() => {
       if (document.body.dataset.renderReady === 'true') { clearInterval(iv); r(); }
     }, 100)
   })
3. mcp__claude-in-chrome__computer  → screenshot
```

### Windows / PowerShell notes

On Windows, `echo '{...}' | python scripts/merge_deck.py` may fail because
PowerShell's `echo` outputs UTF-16 (with BOM). The scripts now handle BOMs
automatically, but if you still hit encoding issues:

```powershell
# Option A (recommended) — use Bash tool instead of PowerShell for piping:
# In Claude Code, prefix with `bash -c` or use the Bash tool directly.
echo '{"deck":{"title":"New"}}' | python scripts/merge_deck.py "<id>"

# Option B — write JSON to a UTF-8 temp file then pipe:
Set-Content -Path patch.json -Value '{"deck":{"title":"New"}}' -Encoding utf8
Get-Content -Raw patch.json | python scripts/merge_deck.py "<id>"
```

## Patch a Single Slide

```bash
# Replace objects on slide 7 (0-based global index):
echo '[{"type":"text",...}]' | python scripts/patch_slide.py <deck-id> 7

# Delete slide 3:
python scripts/patch_slide.py <deck-id> 3 --delete

# Insert a new slide after slide 4 (stdin = full slide JSON object):
echo '{"id":"...","background":{},"objects":[...]}' | python scripts/patch_slide.py <deck-id> 4 --insert-after
```

Fetches the live deck, applies the change, validates locally, then PUTs the
updated deck. Faster than regenerating and replacing the full deck.

## Image Sizing Guide

Pass `--size WxH` to `generate_image.py`. Match the size to the display region
so the renderer crops to fit without quality loss.

| Use case | Width | Height | Aspect | `--size` flag |
|---|---|---|---|---|
| Hero background (full slide) | 1920 | 1080 | 16:9 | `1920x1080` |
| Half-slide panel (left or right half) | 960 | 1080 | 9:16 | `960x1080` |
| Portrait card (player / speaker) | 720 | 900 | 4:5 | `720x900` |
| Square thumbnail / icon | 600 | 600 | 1:1 | `600x600` |
| Wide banner / accent strip | 1920 | 400 | — | `1920x400` |
| Section title background | 1920 | 540 | 32:9 | `1920x540` |

**Rate limit:** The API enforces ~1 req/2 s. Generate portrait images
sequentially (not in parallel) to avoid 429 errors. Retry after 15 s on a 429.

See `references/image-prompts.md` for proven prompt templates per image type.

## Python Layout Helpers

`scripts/block_builder.py` includes schema-safe block builders for:

**Themes:**
- `dark_tech_theme(overrides=None)`, `light_corporate_theme(overrides=None)`

**Primitive objects:**
- `text(role, x, y, w, h, content)`, `rich_text(role, x, y, w, h, runs)`
- `shape(x, y, w, h, fill_token)`, `line(x, y, w)`
- `image(seed_or_url, x, y, w, h)`
- `video(src, x, y, w, h)` — native video file
- `audio(src, x, y, w, h)` — audio player control (for canvas-visible audio; use `narrationTracks` for timeline-sync)
- `embed(url, x, y, w, h)` — YouTube / Vimeo / iframe
- `frame(x, y, w, h, frameKind=…, src=…)` — device/picture-frame mockup
- `qr_code(url, x, y, size)`, `qr_vcard(contact, x, y, size)` — QR codes
- `latex_text(formula, x, y, w, h)` — KaTeX equation

**Data objects:**
- `chart(x, y, w, h, categories, series, chart_type="bar")`
- `table(x, y, w, h, rows)` — 2D list of strings
- `diagram(x, y, w, h, source)` — Mermaid source string

**List objects (prefer these over repeating card() for 4+ items):**
- `bullet_list(items, x, y, w, h)` — single text object with "•" bullets; keeps object count low
- `numbered_list(items, x, y, w, h)` — same but with "1.", "2.", …
- `items` can be plain strings or `{"title": "…", "body": "…"}` dicts

**Composite layouts:**
- `card(x, y, w, h, heading, body)` → list of objects (use max 4 cards/slide)
- `title_chip(label, x, y, width)`, `portrait_card(…)`, `kpi_card(…)`
- `process_flow(items, x, y, w, h)`, `comparison_columns(columns, x, y, w, h)`
- `grid(items, cols, x, y, total_w, total_h)` — use cols=2 (max 4 items) for feature grids

**Slide structure:**
- `slide(objects, notes="", speaker_notes="", animate=True)`
- `section(title, slides)`, `deck(title, sections, theme=…)`

Pass `animate=False` to `slide()` for reference-style decks where entrance
animations would be distracting.

See `references/objects-guide.md` for full field reference and design patterns.

Use the example generator as a template:

```bash
python examples/agent_skills_marketplace.py
```
