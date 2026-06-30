# slide-deck-skill

An agent skill that creates, edits, and publishes professional slide decks on
[deck.4hum.ai](https://deck.4hum.ai) — straight from a plain-English request like
*"make me a 10-slide pitch deck on our solar startup."*

Your AI agent does the work: it designs a custom theme, writes the slide JSON,
validates it, generates any images/video/narration, saves the deck, and hands
you back a link. Works with **Claude Code, Claude Desktop / claude.ai, Codex,
Cursor, and any agent that can read files and run shell commands.**

## What it does

- Designs a custom theme matched to your topic's tone and audience
- Generates charts, tables, diagrams (Mermaid), AI images, video, and narration
- Validates every deck locally before it touches the network
- Previews rendered slides as screenshots so the agent can self-check and iterate
- Saves to deck.4hum.ai and returns the edit URL — and updates existing decks later

---

## Requirements (read this first — it's short)

You only need two things:

1. **Python 3.8 or newer.** Check with `python --version` (or `python3 --version`).
   The core scripts use **only the Python standard library — there is nothing to
   `pip install`.** (One optional extra, `playwright`, is needed *only* if you want
   the agent to screenshot slides locally.)
2. **A free [deck.4hum.ai](https://deck.4hum.ai) account.** You sign in once, in
   your browser, the first time the agent saves a deck (see [Sign in](#3-sign-in-once)).

That's it. No API keys to copy, no `.env` file to edit, no build step.

---

## Install

Pick the path for your agent. **Every path is the same two ideas:** put this
folder where your agent can find it, then let the agent read `SKILL.md`.

### Easiest: just ask your agent

Open a chat with your coding agent and paste:

> Clone `https://github.com/4hum-ai/slide-deck-skill` and set it up as a skill I
> can use. Then read its `SKILL.md` so you know how to use it.

Most agents will figure out the right location and finish the setup themselves.
If you'd rather do it by hand, use the matching section below.

### Claude Code

Claude Code auto-discovers skills — just clone into a skills folder and restart:

```bash
# Available in every project (recommended):
git clone https://github.com/4hum-ai/slide-deck-skill ~/.claude/skills/slide-deck-skill

# …or only in the current project:
git clone https://github.com/4hum-ai/slide-deck-skill .claude/skills/slide-deck-skill
```

Start a new session. Claude picks it up automatically — just ask for a deck.

### Claude Desktop / claude.ai (web)

Skills are uploaded through the UI (available on Pro, Max, Team, and Enterprise plans):

1. Download this repo as a ZIP
   ([Code → Download ZIP](https://github.com/4hum-ai/slide-deck-skill/archive/refs/heads/main.zip)),
   or `git clone` it and re-zip the `slide-deck-skill` folder.
2. In Claude, go to **Settings → Capabilities → Skills → Upload skill** and select
   the ZIP (it must contain `SKILL.md` at the top level).
3. Start a new chat and ask for a deck. *(Claude runs the bundled Python scripts in
   its code environment; the one-time browser sign-in still applies.)*

### Codex, Cursor, Windsurf, or any other agent

These don't have a built-in "skills" folder, but they don't need one — the skill
is just Markdown + Python. Two steps:

```bash
# 1. Clone it somewhere on your machine:
git clone https://github.com/4hum-ai/slide-deck-skill
```

2. Point your agent at it. Either tell it directly each time —

   > Read `slide-deck-skill/SKILL.md` and follow it to build me a deck about X.

   — or make it permanent by adding one line to your agent's instructions file
   (e.g. `AGENTS.md` for Codex, `.cursorrules` for Cursor):

   ```
   To create or edit slide decks, read and follow ./slide-deck-skill/SKILL.md.
   ```

Any agent that can run `python` and read files in that folder can now use the skill.

---

## Use it

### 1. Ask for a deck

Once the skill is installed, just describe what you want:

> Create a slide deck on the benefits of microservices architecture.

The agent plans the slides, designs a theme, writes and validates the JSON,
generates any images, saves the deck, and returns a link like
`https://deck.4hum.ai/app/decks/<id>/edit`.

### 2. Keep iterating in plain English

> Make the cover darker, add a chart of adoption by year, and cut slide 4.

The agent edits only what changed and re-saves to the same URL.

### 3. Sign in (once)

The **first time** the agent saves a deck, it will print a sign-in prompt:

```
deck-4hum-ai: authorization required.
  Open this URL in your browser:
  https://deck.4hum.ai/auth/device
  Confirmation code: ABCD-1234
  Waiting for authorization...
```

Open the URL, enter the code, approve — and you're done. Your credentials are
saved to `~/.open-academy/config.json` and reused automatically from then on. No
key copying, no config files. (To sign out: `python scripts/auth.py logout`.)

---

## Troubleshooting

| Problem | Fix |
|---|---|
| `python: command not found` | Install Python 3.8+ from [python.org](https://www.python.org/downloads/). On macOS/Linux the command may be `python3`. |
| Agent can't find the skill | Make sure you started a **new** session after installing, and that `SKILL.md` sits at the top level of the folder. |
| Stuck on "Waiting for authorization" | Finish the browser sign-in (open the URL, enter the code, approve). The code expires after ~15 min — re-run if so. |
| "Authorization required" keeps reappearing | Delete `~/.open-academy/config.json` and let the agent re-run sign-in. |
| Slide screenshots fail | Screenshots are optional and need `pip install playwright && python -m playwright install chromium`. The deck still saves fine without them. |
| Windows piping / encoding errors | Use the Bash tool/Git Bash for piping JSON, or write JSON to a UTF-8 file first. See the *Windows / PowerShell notes* in [`references/commands.md`](references/commands.md). |

---

## Updating

### Get the latest version of the skill

```bash
cd ~/.claude/skills/slide-deck-skill   # or wherever you cloned it
git pull origin main
```

See [CHANGELOG.md](CHANGELOG.md) for what changed. (Claude Desktop / web users:
re-download the ZIP and re-upload it.)

### Update an existing deck's content

You normally just ask the agent ("update my microservices deck — add a slide on
costs"). Under the hood it uses:

```bash
python scripts/update_deck.py "<deck-id>" < updated-deck.json
```

The deck URL doesn't change — reload `https://deck.4hum.ai/app/decks/<id>/edit`.

---

## Structure

```
slide-deck-skill/
├── SKILL.md                  # Agent instructions (loaded when the skill activates)
├── scripts/                  # Pure-stdlib Python tools the agent runs
│   ├── auth.py               #   one-time browser sign-in (device flow)
│   ├── block_builder.py      #   schema-safe block builders: card, kpi, grid, chart, table…
│   ├── deck_validator.py     #   local preflight validation (--strict quality pass)
│   ├── save_deck.py / update_deck.py / patch_slide.py / merge_deck.py / get_deck.py
│   ├── generate_image.py / generate_video.py / generate_audio.py / set_deck_music.py
│   └── preview_deck.py / screenshot_slides.py   # inspect & screenshot (screenshot needs playwright)
├── references/               # Schema + design guides the agent loads on demand
│   ├── scene-graph.md  theme-presets.md  objects-guide.md  commands.md  image-prompts.md
└── examples/                 # Complete generator scripts to learn from
```

## License

MIT — see [LICENSE](LICENSE).
