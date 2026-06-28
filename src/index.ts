#!/usr/bin/env node
/**
 * MCP server for deck-4hum-ai.
 *
 * Exposes save_deck, update_deck, create_deck, list_decks, get_deck, delete_deck
 * as MCP tools. Claude (the AI agent) generates deckJson directly using the
 * slide-scene-graph v0.4.0 schema â€” these tools only persist and retrieve decks
 * via the REST API. No backend LLM is invoked here.
 *
 * Auth: reads ~/.open-academy/config.json (written by the Python auth.py
 * device flow). Run `python skills/deck-4hum-ai/scripts/auth.py` once to
 * authenticate, then start this server.
 */
import { readFileSync, existsSync } from 'node:fs';
import { homedir } from 'node:os';
import { join } from 'node:path';
import https from 'node:https';
import http from 'node:http';

import { Server } from '@modelcontextprotocol/sdk/server/index.js';
import { StdioServerTransport } from '@modelcontextprotocol/sdk/server/stdio.js';
import {
  CallToolRequestSchema,
  ListToolsRequestSchema,
  type Tool,
} from '@modelcontextprotocol/sdk/types.js';

// ---------------------------------------------------------------------------
// Config
// ---------------------------------------------------------------------------

const API_URL = process.env.OPEN_ACADEMY_API_URL ?? 'https://open-academy-api-mz4xquo5lq-as.a.run.app';
const APP_URL = process.env.OPEN_ACADEMY_APP_URL ?? 'https://deck.4hum.ai';
const CONFIG_PATH = join(homedir(), '.open-academy', 'config.json');

interface Credentials {
  token: string;
  workspace_id: string;
}

function loadCredentials(): Credentials {
  const token = process.env.OPEN_ACADEMY_TOKEN ?? '';
  const workspace_id = process.env.OPEN_ACADEMY_WORKSPACE_ID ?? '';
  if (token && workspace_id) return { token, workspace_id };

  if (!existsSync(CONFIG_PATH)) {
    throw new Error(
      `Not authenticated. Run: python skills/deck-4hum-ai/scripts/auth.py\n` +
        `Then restart this MCP server.`
    );
  }
  const cfg = JSON.parse(readFileSync(CONFIG_PATH, 'utf-8')) as Partial<Credentials>;
  if (!cfg.token || !cfg.workspace_id) {
    throw new Error(`Invalid credentials in ${CONFIG_PATH}. Re-run auth.py.`);
  }
  return { token: cfg.token, workspace_id: cfg.workspace_id };
}

// ---------------------------------------------------------------------------
// HTTP helpers
// ---------------------------------------------------------------------------

function request(
  method: string,
  path: string,
  body: unknown,
  creds: Credentials
): Promise<unknown> {
  return new Promise((resolve, reject) => {
    const url = new URL(`${API_URL}${path}`);
    const lib = url.protocol === 'https:' ? https : http;
    const payload = body ? JSON.stringify(body) : undefined;

    const req = lib.request(
      url,
      {
        method,
        headers: {
          Authorization: `Bearer ${creds.token}`,
          'x-workspace-id': creds.workspace_id,
          'Content-Type': 'application/json',
          ...(payload ? { 'Content-Length': Buffer.byteLength(payload) } : {}),
        },
      },
      (res) => {
        const chunks: Buffer[] = [];
        res.on('data', (c: Buffer) => chunks.push(c));
        res.on('end', () => {
          const text = Buffer.concat(chunks).toString('utf-8');
          if ((res.statusCode ?? 0) >= 400) {
            reject(new Error(`HTTP ${res.statusCode}: ${text}`));
            return;
          }
          try {
            resolve(JSON.parse(text));
          } catch {
            resolve(text);
          }
        });
      }
    );
    req.on('error', reject);
    if (payload) req.write(payload);
    req.end();
  });
}

// ---------------------------------------------------------------------------
// Tool definitions
// ---------------------------------------------------------------------------

const TOOLS: Tool[] = [
  {
    name: 'generate_image',
    description:
      'Generate an AI image from a text prompt and store it in the workspace media library. ' +
      'Use this to create custom illustrations, backgrounds, or hero images for slides. ' +
      'Returns a file_url you can use directly as the "src" field on an image object in the deck JSON. ' +
      'Call this BEFORE building the deckJson so you have real URLs to embed.',
    inputSchema: {
      type: 'object',
      properties: {
        prompt: {
          type: 'string',
          description:
            'Detailed visual description of the image. Include subject, style, mood, lighting, color palette. ' +
            'Example: "A futuristic server room with blue neon lighting, dramatic perspective, photorealistic, 4K"',
        },
        size: {
          type: 'string',
          description:
            'Output dimensions as WIDTHxHEIGHT. Common sizes: ' +
            '"1920x1080" (full-bleed slide), "960x1080" (half-split), "800x600" (card). ' +
            'Default: "1920x1080".',
        },
        style: {
          type: 'string',
          description:
            'Optional style hint for the generation model, e.g. "photorealistic", "illustration", "flat design", "watercolor".',
        },
      },
      required: ['prompt'],
    },
  },
  {
    name: 'save_deck',
    description:
      'Save a Claude-generated deckJson as a new deck on deck-4hum-ai. ' +
      'Call this after you have generated the complete deckJson object using the ' +
      'slide-scene-graph v0.4.0 schema (see SKILL.md for the full schema reference). ' +
      'Returns the deck_id and a direct edit URL.',
    inputSchema: {
      type: 'object',
      properties: {
        title: {
          type: 'string',
          description: 'Title of the deck (shown in the deck list)',
        },
        deck_json: {
          type: 'object',
          description:
            'The complete deckJson envelope: ' +
            '{ "schema": "open-academy.slide-scene-graph", "schemaVersion": "0.4.0", "deck": { ... } }',
        },
      },
      required: ['title', 'deck_json'],
    },
  },
  {
    name: 'update_deck',
    description:
      'Replace the deckJson of an existing deck with an improved version. ' +
      'Use this to update a deck after evaluating and refining the JSON structure.',
    inputSchema: {
      type: 'object',
      properties: {
        deck_id: {
          type: 'string',
          description: 'UUID of the deck to update',
        },
        deck_json: {
          type: 'object',
          description: 'The updated deckJson envelope (slide-scene-graph v0.4.0)',
        },
      },
      required: ['deck_id', 'deck_json'],
    },
  },
  {
    name: 'create_deck',
    description: 'Create a blank slide deck with a given title. Use this when the user wants an empty deck to fill in manually.',
    inputSchema: {
      type: 'object',
      properties: {
        title: { type: 'string', description: 'Title for the new deck' },
      },
      required: ['title'],
    },
  },
  {
    name: 'list_decks',
    description: 'List the most recent decks in the workspace.',
    inputSchema: {
      type: 'object',
      properties: {
        limit: {
          type: 'number',
          description: 'Number of decks to return (default 20, max 100)',
        },
      },
    },
  },
  {
    name: 'get_deck',
    description:
      'Fetch full deck details including deckJson (title, sections, slides, objects, theme). ' +
      'Use this to inspect a deck for evaluation or before generating an update.',
    inputSchema: {
      type: 'object',
      properties: {
        deck_id: { type: 'string', description: 'UUID of the deck to fetch' },
      },
      required: ['deck_id'],
    },
  },
  {
    name: 'delete_deck',
    description: 'Permanently delete a deck. This cannot be undone.',
    inputSchema: {
      type: 'object',
      properties: {
        deck_id: { type: 'string', description: 'UUID of the deck to delete' },
      },
      required: ['deck_id'],
    },
  },
];

// ---------------------------------------------------------------------------
// Tool handlers
// ---------------------------------------------------------------------------

async function handleGenerateImage(args: Record<string, unknown>, creds: Credentials) {
  const prompt = String(args.prompt ?? '');
  const size = String(args.size ?? '1920x1080');
  const style = args.style ? String(args.style) : undefined;

  if (!prompt) throw new Error('prompt is required');

  const body = await request('POST', '/api/media/generate-image', {
    prompt,
    size,
    ...(style ? { style } : {}),
    workspaceId: creds.workspace_id,
  }, creds) as { data?: { id?: string; fileUrl?: string; url?: string } };

  const media = body.data ?? (body as { id?: string; fileUrl?: string; url?: string });
  const media_id = media.id;
  const file_url = media.fileUrl ?? media.url;

  if (!file_url) throw new Error(`Unexpected response from generate-image: ${JSON.stringify(body)}`);

  return {
    content: [{
      type: 'text' as const,
      text: `Image generated: ${file_url}\n${JSON.stringify({ media_id, file_url })}`,
    }],
  };
}

async function handleSaveDeck(args: Record<string, unknown>, creds: Credentials) {
  const title = String(args.title ?? 'New Deck');
  const deck_json = args.deck_json as object;

  if (!deck_json || typeof deck_json !== 'object') {
    throw new Error('deck_json must be the slide-scene-graph v0.4.0 envelope object');
  }

  const body = await request('POST', '/api/decks', {
    workspaceId: creds.workspace_id,
    title,
    deckJson: deck_json,
  }, creds) as { id?: string; data?: { id?: string } };

  const deck_id = body.id ?? body.data?.id;
  if (!deck_id) throw new Error(`Unexpected response: ${JSON.stringify(body)}`);

  const deck_url = `${APP_URL}/app/decks/${deck_id}/edit`;
  return { content: [{ type: 'text' as const, text: `Deck saved: ${deck_url}\n${JSON.stringify({ deck_id, deck_url })}` }] };
}

async function handleUpdateDeck(args: Record<string, unknown>, creds: Credentials) {
  const deck_id = String(args.deck_id ?? '');
  const deck_json = args.deck_json as object;

  if (!deck_id) throw new Error('deck_id is required');
  if (!deck_json || typeof deck_json !== 'object') {
    throw new Error('deck_json must be the slide-scene-graph v0.4.0 envelope object');
  }

  await request('PUT', `/api/decks/${deck_id}`, { deckJson: deck_json }, creds);

  const deck_url = `${APP_URL}/app/decks/${deck_id}/edit`;
  return { content: [{ type: 'text' as const, text: `Deck updated: ${deck_url}\n${JSON.stringify({ deck_id, deck_url })}` }] };
}

async function handleCreateDeck(args: Record<string, unknown>, creds: Credentials) {
  const title = String(args.title ?? 'New Deck');
  const body = await request('POST', '/api/decks', {
    workspaceId: creds.workspace_id,
    title,
    deckJson: {
      schema: 'open-academy.slide-scene-graph',
      schemaVersion: '0.4.0',
      deck: {
        id: crypto.randomUUID(),
        title,
        width: 1920,
        height: 1080,
        theme: {
          id: crypto.randomUUID(),
          name: 'Default',
          fonts: { heading: 'Inter', body: 'Inter' },
          colors: { background: '#ffffff', foreground: '#0f172a', primary: '#6366f1' },
        },
        sections: [{ id: crypto.randomUUID(), title: 'Main', slides: [] }],
      },
    },
  }, creds) as { id?: string; data?: { id?: string } };

  const deck_id = body.id ?? body.data?.id;
  if (!deck_id) throw new Error(`Unexpected response: ${JSON.stringify(body)}`);

  const deck_url = `${APP_URL}/app/decks/${deck_id}/edit`;
  return { content: [{ type: 'text' as const, text: JSON.stringify({ deck_id, deck_url }) }] };
}

async function handleListDecks(args: Record<string, unknown>, creds: Credentials) {
  const limit = Number(args.limit ?? 20);
  const params = new URLSearchParams({
    workspaceId: creds.workspace_id,
    limit: String(Math.min(limit, 100)),
    orderBy: 'updatedAt',
    order: 'desc',
  });
  const data = await request('GET', `/api/decks?${params}`, null, creds);
  const decks = Array.isArray(data) ? data : (data as { data?: unknown[] }).data ?? [];
  const result = (decks as Array<{ id?: string; title?: string; status?: string }>).map((d) => ({
    id: d.id,
    title: d.title ?? 'Untitled',
    status: d.status,
    url: `${APP_URL}/app/decks/${d.id}/edit`,
  }));
  return { content: [{ type: 'text' as const, text: JSON.stringify({ decks: result }) }] };
}

async function handleGetDeck(args: Record<string, unknown>, creds: Credentials) {
  const deck_id = String(args.deck_id ?? '');
  const data = await request('GET', `/api/decks/${deck_id}`, null, creds);
  return { content: [{ type: 'text' as const, text: JSON.stringify(data) }] };
}

async function handleDeleteDeck(args: Record<string, unknown>, creds: Credentials) {
  const deck_id = String(args.deck_id ?? '');
  await request('DELETE', `/api/decks/${deck_id}`, null, creds);
  return { content: [{ type: 'text' as const, text: JSON.stringify({ success: true, deck_id }) }] };
}

// ---------------------------------------------------------------------------
// Server boot
// ---------------------------------------------------------------------------

const server = new Server(
  { name: 'slide-deck-mcp', version: '1.2.0' },
  { capabilities: { tools: {} } }
);

server.setRequestHandler(ListToolsRequestSchema, async () => ({ tools: TOOLS }));

server.setRequestHandler(CallToolRequestSchema, async (request) => {
  const { name, arguments: args = {} } = request.params;
  const creds = loadCredentials();
  const a = args as Record<string, unknown>;

  switch (name) {
    case 'generate_image': return handleGenerateImage(a, creds);
    case 'save_deck':    return handleSaveDeck(a, creds);
    case 'update_deck':  return handleUpdateDeck(a, creds);
    case 'create_deck':  return handleCreateDeck(a, creds);
    case 'list_decks':   return handleListDecks(a, creds);
    case 'get_deck':     return handleGetDeck(a, creds);
    case 'delete_deck':  return handleDeleteDeck(a, creds);
    default:
      throw new Error(`Unknown tool: ${name}`);
  }
});

const transport = new StdioServerTransport();
await server.connect(transport);

