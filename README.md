# slide-deck-skill

An [Agent Skills](https://agentskills.io) package for creating, editing, and
publishing professional slide decks on [deck.4hum.ai](https://deck.4hum.ai).

The agent generates slide JSON directly from the
[slide-scene-graph v0.4.0](references/scene-graph.md) schema, validates it
locally, then saves it through the deck.4hum.ai REST API via bundled Python
scripts. No backend LLM call is needed for content — the agent writes the deck
JSON itself.

## What it does

- Picks a visual theme from six presets (Dark Tech, Light Corporate, Warm
  Creative, Midnight Minimal, Forest Green, Neon Purple)
- Generates charts, tables, diagrams (Mermaid), images, and rich text objects
- Validates the deck JSON locally before any network call
- Saves to deck.4hum.ai and returns the edit URL
- Iterates on existing decks via `update_deck.py`
- Generates custom hosted images via the API

## Prerequisites

- Python 3.8+
- Network access to the deck.4hum.ai API
- A deck.4hum.ai account (run `python scripts/auth.py` once to authenticate)

## Installation

### Claude Code

```bash
/install https://github.com/4hum-ai/slide-deck-skill
```

Or copy the skill directory into your project's `.claude/skills/` folder:

```bash
cp -r slide-deck-skill ~/.claude/skills/
```

### Other agentskills.io-compatible clients

Copy or reference the skill directory per your client's documentation. See
[agentskills.io/clients](https://agentskills.io/clients) for client-specific
install instructions.

## Quick start

Once installed, just ask your agent:

> "Create a slide deck on the benefits of microservices architecture."

The agent will pick a theme, plan the slides, generate the deck JSON, validate
it, and return a link like:

```
https://deck.4hum.ai/app/decks/<id>/edit
```

## Manual usage

Authenticate once:

```bash
python scripts/auth.py
```

Generate and save a deck:

```bash
python examples/agent_skills_marketplace.py | python scripts/save_deck.py "My Deck"
```

Update an existing deck:

```bash
python scripts/update_deck.py "<deck-id>" < deck.json
```

Generate a hosted image:

```bash
python scripts/generate_image.py "Futuristic server room, dark neon lighting" --size 1920x1080
```

## Structure

```
slide-deck-skill/
├── SKILL.md                          # Agent instructions (loaded at activation)
├── scripts/
│   ├── auth.py                       # Credential management
│   ├── deck_patterns.py              # Schema-safe layout helpers
│   ├── deck_validator.py             # Local preflight validator
│   ├── generate_image.py             # Image generation
│   ├── save_deck.py                  # Create deck via API
│   └── update_deck.py                # Update existing deck
├── references/
│   ├── scene-graph.md                # Full deckJson schema reference
│   ├── theme-presets.md              # Theme JSON objects + color tokens
│   └── commands.md                   # Script commands + env vars
└── examples/
    └── agent_skills_marketplace.py   # Complete five-slide example
```

## License

MIT — see [LICENSE](LICENSE).
