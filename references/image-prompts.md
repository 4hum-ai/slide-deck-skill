# Image Prompt Templates

Proven prompt patterns for `scripts/generate_image.py`. Each template was
refined through real deck production — copy, fill in the `[PLACEHOLDERS]`, and
adjust style adjectives to match your theme.

## Portrait — person / player / speaker

Best size: `--size 720x900` (4:5) for a portrait card column; `--size 600x800`
for narrower layouts.

```
Photorealistic digital art portrait of [FULL NAME], [NATIONALITY] [ROLE/SPORT]
[player/executive/speaker], wearing [TEAM/BRAND] kit/attire, confident
[athletic/professional] pose, studio lighting with soft rim light,
[BACKGROUND_COLOR e.g. "deep navy gradient"] background, ultra-detailed face,
sharp focus, sports photography style, 8K resolution
```

**Tips:**
- Name the person explicitly — models handle famous athletes and public figures well.
- Match background color to your theme's `surface` or `background` token so the
  portrait card blends naturally.
- Add `"no watermark, no text overlay"` at the end to prevent logo artifacts.
- For fictional/composite characters add `"character concept art, illustrated"`.

## Hero background — full-slide (16:9)

Best size: `--size 1920x1080`. Place at `x=0 y=0 width=1920 height=1080` with
`"fit":"cover"`. Then add a low-opacity shape overlay (`opacity: 0.55`) so text
is readable.

```
[SCENE DESCRIPTION], dramatic [golden hour / dusk / neon night] lighting,
wide-angle cinematic composition, ultra high resolution photography,
[MOOD: e.g. "electric atmosphere", "serene landscape", "futuristic city"],
no people, no text, no watermarks, 16:9 aspect ratio
```

**Examples:**
- Football stadium: `"Aerial view of a packed 80 000-seat football stadium at sunset, electric atmosphere, green pitch, crowd wave motion blur, no text"`
- Tech office: `"Modern open-plan tech office, soft natural light, glass walls, city skyline background, cinematic depth of field, no people"`
- Nature: `"Misty mountain valley at dawn, golden light rays through pine trees, ultra-wide angle, National Geographic style photography"`

## Section divider / accent strip

Best size: `--size 1920x400`. Useful for section title slides where the image
fills the lower half.

```
Abstract [THEME: geometric / fluid / organic] pattern in [COLOR PALETTE],
minimalist, no text, suitable as a presentation slide background strip,
ultra high resolution
```

## Icon / illustration

Best size: `--size 600x600` (square).

```
Flat vector icon of [OBJECT/CONCEPT], [STYLE: minimal / outlined / filled],
[COLOR: "in brand blue"] on white background, clean SVG-style illustration,
no text, no shadow, no gradient, icon design
```

## Data visualization / infographic element

Best size: `--size 960x540` (half-slide).

```
[CHART/DIAGRAM CONCEPT e.g. "upward trend bar chart", "global network map"],
clean infographic style, [COLOR PALETTE matching theme], white background,
no labels, no text, suitable for a slide deck graphic, vector illustration
```

## Retry and rate-limit notes

- The API enforces a rate limit (~1 req/2 s). If you see a 429, wait 15 s and retry.
- Generate portrait images **sequentially** (not in parallel) to avoid 429s.
- For 4+ images on a slide, generate them one at a time, collecting `file_url` values, then build the slide JSON.
- Use `--size` that matches the intended display region — the renderer crops to fit, so oversizing wastes generation time without quality gain.
