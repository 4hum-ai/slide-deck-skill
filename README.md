# slide-deck-skill

An agent skill package for creating, editing, and
publishing professional slide decks on [deck.4hum.ai](https://deck.4hum.ai).

The agent generates slide JSON directly from the
[slide-scene-graph v0.4.0](references/scene-graph.md) schema, validates it
locally, then saves it through the deck.4hum.ai REST API via bundled Python
scripts. No backend LLM call is needed for content — the agent writes the deck
JSON itself.

## What it does

- Designs a custom theme matched to the topic's tone and audience (not just
  picks from a list — uses the six built-in presets as inspiration)
- Generates charts, tables, diagrams (Mermaid), images, and rich text objects
- Validates the deck JSON locally before any network call
- Previews rendered slides as screenshots so the agent can evaluate and iterate
- Saves to deck.4hum.ai and returns the edit URL
- Updates existing decks via `update_deck.py`
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

Or copy the skill directory into your user skills folder:

```bash
cp -r slide-deck-skill ~/.claude/skills/
```

### OpenAI Codex

Add the skill to your `codex.json` skills list:

```json
{
  "skills": [
    "https://github.com/4hum-ai/slide-deck-skill"
  ]
}
```

Or clone it locally and point to the path:

```json
{
  "skills": ["./skills/slide-deck-skill"]
}
```

See [OpenAI Codex skills docs](https://developers.openai.com/codex/skills/) for details.

### GitHub Copilot (VS Code)

Copy the skill directory into your workspace or user skills folder:

```bash
mkdir -p .github/skills
cp -r slide-deck-skill .github/skills/
```

Then enable it in `.github/copilot-instructions.md` or via the Copilot skill
loader. See [GitHub Copilot agent skills docs](https://docs.github.com/en/copilot/concepts/agents/about-agent-skills).

### Cursor

Copy the skill directory into the Cursor skills location:

```bash
cp -r slide-deck-skill ~/.cursor/skills/
```

Or add a project-local skill under `.cursor/skills/slide-deck-skill/`.
See [Cursor skills docs](https://cursor.com/docs/context/skills).

### Gemini CLI

```bash
gemini skill add https://github.com/4hum-ai/slide-deck-skill
```

Or clone and reference locally:

```bash
git clone https://github.com/4hum-ai/slide-deck-skill ~/.gemini/skills/slide-deck-skill
```

See [Gemini CLI skills docs](https://geminicli.com/docs/cli/skills/).

### Roo Code

Add to your `.roocode/skills/` directory:

```bash
cp -r slide-deck-skill .roocode/skills/
```

See [Roo Code skills docs](https://docs.roocode.com/features/skills).

### Any other agentskills.io-compatible client

Copy or reference the skill directory per your client's documentation. All
[agentskills.io-compatible clients](https://agentskills.io/clients) use the
same `SKILL.md` format — the install path varies by product.

## Updating the skill

### Update the skill itself (get the latest version)

```bash
# If installed via git clone:
cd ~/.claude/skills/slide-deck-skill   # or wherever you installed it
git pull origin main
```

Check [CHANGELOG.md](CHANGELOG.md) for what changed between versions.

If a new version has schema or script changes, re-authenticate and re-validate
any decks you intend to update:

```bash
python scripts/auth.py
python scripts/deck_validator.py < my-deck.json
```

### Update an existing deck's content

To push new JSON to a deck you already created:

```bash
# By deck ID (printed when you first saved the deck):
python scripts/update_deck.py "<deck-id>" < updated-deck.json

# Or pipe from a generator script:
python my_generator.py | python scripts/update_deck.py "<deck-id>"
```

The update script validates the JSON before sending, same as save. The deck
URL does not change — reload `https://deck.4hum.ai/app/decks/<id>/edit` to
see the new content.

### Bump the skill version (maintainers)

When you make changes to the skill itself (scripts, references, SKILL.md),
update `metadata.version` in `SKILL.md` and add an entry to `CHANGELOG.md`
before tagging a release.

## Quick start

Once installed, just ask your agent:

> "Create a slide deck on the benefits of microservices architecture."

The agent will design a custom theme, plan the slides, generate deck JSON,
validate it, preview the result, and return a link like:

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

Preview rendered slides as screenshots:

```bash
python scripts/preview_deck.py "<deck-id>"
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
│   ├── preview_deck.py               # Screenshot slides for agent evaluation
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
