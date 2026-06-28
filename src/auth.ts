#!/usr/bin/env node
import { createServer } from 'node:http';
import { exec } from 'node:child_process';
import { readFileSync, writeFileSync, mkdirSync, existsSync, chmodSync } from 'node:fs';
import { homedir } from 'node:os';
import { join } from 'node:path';
import crypto from 'node:crypto';

const API_URL =
  process.env.OPEN_ACADEMY_API_URL ??
  'https://open-academy-api-mz4xquo5lq-as.a.run.app';
const CONFIG_PATH = join(homedir(), '.open-academy', 'config.json');

function openBrowser(url: string): void {
  const platform = process.platform;
  if (platform === 'win32') exec(`start "" "${url}"`);
  else if (platform === 'darwin') exec(`open "${url}"`);
  else exec(`xdg-open "${url}"`);
}

function findFreePort(start: number, end: number): Promise<number> {
  return new Promise((resolve, reject) => {
    const tryPort = (port: number) => {
      if (port > end) {
        reject(new Error('No free port found in range'));
        return;
      }
      const srv = createServer();
      srv.listen(port, '127.0.0.1', () => {
        srv.close(() => resolve(port));
      });
      srv.on('error', () => tryPort(port + 1));
    };
    tryPort(start);
  });
}

export async function runAuth(forceReauth = false): Promise<void> {
  // Check if already authenticated.
  if (!forceReauth && existsSync(CONFIG_PATH)) {
    try {
      const cfg = JSON.parse(readFileSync(CONFIG_PATH, 'utf-8')) as {
        token?: string;
        workspace_id?: string;
      };
      if (cfg.token && cfg.workspace_id) {
        console.error(`Already authenticated. Workspace: ${cfg.workspace_id}`);
        console.error(`Run with --reauth to re-authenticate.`);
        return;
      }
    } catch {
      // Corrupt config — fall through to re-auth.
    }
  }

  const port = await findFreePort(51820, 51830);
  const state = crypto.randomUUID();
  const redirectUri = `http://localhost:${port}/callback`;
  const authUrl = `${API_URL}/api/auth/cli?redirect_uri=${encodeURIComponent(redirectUri)}&state=${encodeURIComponent(state)}`;

  console.error('Opening browser for authentication...');
  console.error(`  ${authUrl}`);
  console.error('');
  openBrowser(authUrl);

  await new Promise<void>((resolve, reject) => {
    const timeout = setTimeout(() => {
      server.close();
      reject(new Error('Authentication timed out after 5 minutes'));
    }, 5 * 60 * 1000);

    const server = createServer((req, res) => {
      const url = new URL(req.url ?? '/', `http://localhost:${port}`);
      if (url.pathname !== '/callback') {
        res.end();
        return;
      }

      const returnedState = url.searchParams.get('state') ?? '';
      if (returnedState !== state) {
        res.writeHead(400, { 'Content-Type': 'text/html; charset=utf-8' });
        res.end(
          `<!DOCTYPE html><html><body style="font-family:sans-serif;text-align:center;padding:4rem">
            <h2>Authentication Error</h2><p>Invalid state parameter. Please try again.</p>
          </body></html>`
        );
        clearTimeout(timeout);
        server.close();
        reject(new Error('State mismatch — possible CSRF'));
        return;
      }

      const token = url.searchParams.get('token') ?? '';
      const workspace_id = url.searchParams.get('workspace_id') ?? '';
      if (!token || !workspace_id) {
        res.writeHead(400, { 'Content-Type': 'text/html; charset=utf-8' });
        res.end(
          `<!DOCTYPE html><html><body style="font-family:sans-serif;text-align:center;padding:4rem">
            <h2>Authentication Error</h2><p>Missing credentials. Please try again.</p>
          </body></html>`
        );
        clearTimeout(timeout);
        server.close();
        reject(new Error(`Missing token or workspace_id in callback`));
        return;
      }

      // Save credentials.
      const dir = join(homedir(), '.open-academy');
      mkdirSync(dir, { recursive: true });
      writeFileSync(
        CONFIG_PATH,
        JSON.stringify({ token, workspace_id }, null, 2),
        'utf-8'
      );
      try {
        chmodSync(CONFIG_PATH, 0o600);
      } catch {
        // chmod not available on all platforms (e.g. Windows) — non-fatal.
      }

      res.writeHead(200, { 'Content-Type': 'text/html; charset=utf-8' });
      res.end(
        `<!DOCTYPE html><html><body style="font-family:sans-serif;text-align:center;padding:4rem">
          <h2 style="color:#22c55e">&#10003; Authenticated!</h2>
          <p>You can close this tab and return to the terminal.</p>
        </body></html>`
      );

      clearTimeout(timeout);
      server.close();
      console.error(`✓ Authenticated! Workspace: ${workspace_id}`);
      console.error(`  Credentials saved to ${CONFIG_PATH}`);
      resolve();
    });

    server.listen(port, '127.0.0.1');
  });
}

// Allow running directly: `node dist/auth.js [--reauth]`
if (process.argv[1] && process.argv[1].includes('auth')) {
  runAuth(process.argv.includes('--reauth')).catch((e: unknown) => {
    const msg = e instanceof Error ? e.message : String(e);
    console.error(`Auth failed: ${msg}`);
    process.exit(1);
  });
}
