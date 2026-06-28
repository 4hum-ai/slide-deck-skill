# slide-deck-skill

**Claude Code skill** + **MCP server** for creating professional AI-powered slide decks on [deck-4hum-ai](https://deck.4hum.ai).

Claude generates the full deck JSON directly from the [slide-scene-graph v0.4.0 schema](SKILL.md), saves it via the API, and returns a live edit URL. Supports AI-generated images, animations, narration scripts, web search citations, charts, tables, diagrams (Mermaid), and video embeds.

## Quick start (Claude Code skill)

```bash
# Add to your project
gh skill add 4hum-ai/slide-deck-skill

# Or reference directly in a prompt
/deck-4hum-ai create a 10-slide introduction to quantum computing
```

## Quick start (MCP server)

```bash
npx @4humai/slide-deck-skill
```

Add to your MCP client config (`~/.config/claude/claude_desktop_config.json`):

```json
{
  "mcpServers": {
    "slide-deck": {
      "command": "npx",
      "args": ["-y", "@4humai/slide-deck-skill"],
      "env": {
        "OPEN_ACADEMY_API_URL": "https://open-academy-api-mz4xquo5lq-as.a.run.app",
        "OPEN_ACADEMY_APP_URL": "https://deck.4hum.ai"
      }
    }
  }
}
```

On first use the server will prompt you to authorize via browser (device flow). Credentials are saved to `~/.open-academy/config.json`.

## MCP tools

| Tool | Description |
|---|---|
| `save_deck` | Save a new deck from generated JSON |
| `update_deck` | Replace the JSON of an existing deck |
| `generate_image` | AI-generate an image and get a hosted URL for use in a slide |
| `create_deck` | Create a blank deck |
| `list_decks` | List recent decks in the workspace |
| `get_deck` | Fetch a deck's full JSON for inspection |
| `delete_deck` | Delete a deck |

## Python scripts (CLI)

```bash
# Authenticate once
python scripts/auth.py

# Generate an image for a slide
python scripts/generate_image.py "NVIDIA RTX 5060, dark background, neon lighting" --size 1920x1080

# Save a deck (pipe JSON)
python scripts/save_deck.py "My Deck Title" < deck.json

# Update an existing deck
python scripts/update_deck.py "<deck-id>" < deck.json
```

## Skill reference

See [`SKILL.md`](SKILL.md) for the full schema, theme presets, object types, animations, narration scripts, and web search integration.

## License

MIT



