# slide-deck-skill

**Claude Code skill** + **MCP server** for creating professional AI-powered slide decks on [deck-4hum-ai](https://deck.4hum.ai).

Claude generates the full deck JSON directly from the [slide-scene-graph v0.4.0 schema](SKILL.md), saves it via the API, and returns a live edit URL. Supports AI-generated images, animations, narration scripts, web search citations, charts, tables, diagrams (Mermaid), and video embeds.

---

## Install

### Smithery (recommended)

```bash
# Add to Claude Code
npx -y @smithery/cli install @4humai/slide-deck-skill --client claude-code

# Add to Claude Desktop
npx -y @smithery/cli install @4humai/slide-deck-skill --client claude

# Add to Cursor
npx -y @smithery/cli install @4humai/slide-deck-skill --client cursor

# Update to latest version
npx -y @smithery/cli update @4humai/slide-deck-skill
```

### Skills.sh

```bash
# Add the skill to your agent
npx -y skills add 4hum-ai/slide-deck-skill --agent claude-code

# Update to latest
npx -y skills update 4hum-ai/slide-deck-skill
```

### Claude Code CLI (direct)

```bash
# Add as MCP server
claude mcp add slide-deck -- npx -y @4humai/slide-deck-skill

# With explicit API URL override
claude mcp add slide-deck -e OPEN_ACADEMY_API_URL=https://open-academy-api-mz4xquo5lq-as.a.run.app -- npx -y @4humai/slide-deck-skill

# Remove
claude mcp remove slide-deck
```

### Claude Desktop (manual config)

Add to `~/.config/claude/claude_desktop_config.json` (macOS/Linux) or `%APPDATA%\Claude\claude_desktop_config.json` (Windows):

```json
{
  "mcpServers": {
    "slide-deck": {
      "command": "npx",
      "args": ["-y", "@4humai/slide-deck-skill"]
    }
  }
}
```

### Other MCP clients (Cursor, Windsurf, Zed…)

```json
{
  "mcp": {
    "slide-deck": {
      "command": "npx",
      "args": ["-y", "@4humai/slide-deck-skill"]
    }
  }
}
```

---

## Authenticate

Run once after installing — opens your browser automatically:

```bash
npx @4humai/slide-deck-skill auth
```

Credentials are saved to `~/.open-academy/config.json`. To re-authenticate:

```bash
npx @4humai/slide-deck-skill auth --reauth
```

Alternatively, set env vars directly (useful in CI or Docker):

```bash
export OPEN_ACADEMY_TOKEN=sk-oa-...
export OPEN_ACADEMY_WORKSPACE_ID=<uuid>
```

---

## Use

Once installed and authenticated, just ask Claude:

```
Create a 10-slide deck introducing the NVIDIA RTX 5060
```

```
Make a presentation on the history of the internet, with a dark neon theme
```

```
Build a product launch deck for our new mobile app, include AI-generated hero images
```

The skill generates the full deck, uploads images, and returns a live edit URL on [deck.4hum.ai](https://deck.4hum.ai).

---

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

---

## Marketplace listings

| Marketplace | Install command / link |
|---|---|
| **Smithery** | `npx -y @smithery/cli install @4humai/slide-deck-skill --client claude-code` |
| **Skills.sh** | `npx -y skills add 4hum-ai/slide-deck-skill --agent claude-code` |
| **npm** | [@4humai/slide-deck-skill](https://www.npmjs.com/package/@4humai/slide-deck-skill) |
| **Official MCP Registry** | [registry.modelcontextprotocol.io](https://registry.modelcontextprotocol.io) |
| **Glama** | [glama.ai/mcp](https://glama.ai/mcp) — auto-indexed |
| **ClawHub** | [clawhub.ai](https://clawhub.ai) — auto-indexed |

---

## Python scripts (CLI fallback)

```bash
# Authenticate (device flow — fallback when browser-callback is unavailable)
python scripts/auth.py

# Generate an image for a slide
python scripts/generate_image.py "NVIDIA RTX 5060, dark background, neon lighting" --size 1920x1080

# Save a deck (pipe JSON)
python scripts/save_deck.py "My Deck Title" < deck.json

# Update an existing deck
python scripts/update_deck.py "<deck-id>" < deck.json
```

---

## Skill reference

See [`SKILL.md`](SKILL.md) for the full schema, theme presets, object types, animations, narration scripts, and web search integration.

## License

MIT
