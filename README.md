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
  picks from a list — uses two structural reference themes as a starting point)
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

The easiest way — open a session with your agent and ask it to install the
skill globally:

> "Clone https://github.com/4hum-ai/slide-deck-skill and install it globally
> so the skill is available in all future sessions."

The agent knows where its own global skills directory is and will handle the
rest. Start a new session afterward to activate it.

### Manual install (Claude Code)

If you prefer to do it yourself:

```bash
# Global — available in all Claude Code sessions:
git clone https://github.com/4hum-ai/slide-deck-skill ~/.claude/skills/slide-deck-skill

# Project-local — available only in this project:
git clone https://github.com/4hum-ai/slide-deck-skill .claude/skills/slide-deck-skill
```

Start a new session — Claude Code auto-discovers skills from those locations.
To update: `cd ~/.claude/skills/slide-deck-skill && git pull`

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
validate it, preview the result, and return a link.


## Structure

```
slide-deck-skill/
├── SKILL.md                          # Agent instructions (loaded at activation)
├── scripts/
│   ├── auth.py                       # Credential management
│   ├── block_builder.py              # Block builders: card, portrait_card, kpi_card, grid, chart, table…
│   ├── deck_patterns.py              # Backwards-compat re-export shim (deck_patterns → block_builder)
│   ├── deck_validator.py             # Local preflight validator (--strict quality pass)
│   ├── preview_deck.py               # Structural summary + WCAG contrast check (--theme-check)
│   ├── patch_slide.py                # Targeted single-slide edit / insert / delete
│   ├── generate_image.py             # Image generation
│   ├── save_deck.py                  # Create deck via API
│   └── update_deck.py                # Update existing deck
├── references/
│   ├── scene-graph.md                # Full deckJson schema reference
│   ├── theme-presets.md              # Theme JSON objects, color tokens, font mood table
│   ├── commands.md                   # Script commands, env vars, image sizing guide
│   └── image-prompts.md              # Proven prompt templates (portrait, hero, icon, dataviz)
└── examples/
    └── agent_skills_marketplace.py   # Complete five-slide example
```

## License

MIT — see [LICENSE](LICENSE).
