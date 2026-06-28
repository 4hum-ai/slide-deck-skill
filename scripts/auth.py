#!/usr/bin/env python3
"""
Device Authorization Flow for deck-4hum-ai CLI.

On first run: initiates an OAuth 2.0 Device Authorization Grant (RFC 8628),
prints a URL for the user to open in their browser, polls until authorized,
then saves the sk-oa- API key and workspace_id to ~/.open-academy/config.json.

On subsequent runs: loads saved credentials and returns them immediately.

Usage:
    from auth import get_credentials
    token, workspace_id = get_credentials()
"""
import json
import os
import sys
import time
import urllib.request
import urllib.error
from pathlib import Path

API_URL = os.environ.get("OPEN_ACADEMY_API_URL", "https://open-academy-api-mz4xquo5lq-as.a.run.app")
APP_URL = os.environ.get("OPEN_ACADEMY_APP_URL", "https://deck.4hum.ai")
CONFIG_PATH = Path.home() / ".open-academy" / "config.json"


def _load_saved() -> tuple[str, str] | None:
    """Return (token, workspace_id) from saved config, or None if missing/invalid."""
    # Allow explicit env override even after auth
    token = os.environ.get("OPEN_ACADEMY_TOKEN", "")
    workspace = os.environ.get("OPEN_ACADEMY_WORKSPACE_ID", "")
    if token and workspace:
        return token, workspace

    if not CONFIG_PATH.exists():
        return None
    try:
        data = json.loads(CONFIG_PATH.read_text())
        t = data.get("token", "")
        w = data.get("workspace_id", "")
        if t and w:
            return t, w
    except (json.JSONDecodeError, OSError):
        pass
    return None


def _save(token: str, workspace_id: str) -> None:
    CONFIG_PATH.parent.mkdir(parents=True, exist_ok=True)
    CONFIG_PATH.write_text(json.dumps({"token": token, "workspace_id": workspace_id}, indent=2))
    # Restrict permissions so only the owner can read it (Unix/macOS).
    try:
        CONFIG_PATH.chmod(0o600)
    except OSError:
        pass


def _api_post(path: str, body: dict, token: str | None = None) -> dict:
    payload = json.dumps(body).encode("utf-8")
    headers: dict[str, str] = {"Content-Type": "application/json"}
    if token:
        headers["Authorization"] = f"Bearer {token}"
    req = urllib.request.Request(f"{API_URL}{path}", data=payload, headers=headers, method="POST")
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        body_text = e.read().decode("utf-8", errors="replace")
        try:
            return json.loads(body_text)
        except json.JSONDecodeError:
            raise RuntimeError(f"HTTP {e.code}: {body_text}") from e


def _initiate() -> dict:
    return _api_post("/api/auth/device/initiate", {})


def _poll(device_code: str, interval: int, expires_in: int) -> tuple[str, str]:
    """Poll /api/auth/device/token until authorized. Returns (token, workspace_id)."""
    deadline = time.time() + expires_in
    while time.time() < deadline:
        time.sleep(interval)
        resp = _api_post("/api/auth/device/token", {"device_code": device_code})
        err = resp.get("error", "")

        if not err:
            token = resp.get("access_token", "")
            workspace_id = resp.get("workspace_id", "")
            if token and workspace_id:
                return token, workspace_id
            raise RuntimeError(f"Unexpected token response: {resp}")

        if err == "authorization_pending":
            continue
        if err == "slow_down":
            interval = min(interval + 5, 30)
            continue
        if err == "expired_token":
            raise RuntimeError("Device code expired. Please run the command again.")
        raise RuntimeError(f"Auth error: {resp.get('error_description', err)}")

    raise RuntimeError("Authorization timed out. Please run the command again.")


def get_credentials(force_reauth: bool = False) -> tuple[str, str]:
    """
    Returns (token, workspace_id).

    On first run (or when force_reauth=True), performs the device authorization
    flow: prints a URL, waits for the user to authorize in the browser, then
    saves the long-lived API key to ~/.open-academy/config.json.
    """
    if not force_reauth:
        saved = _load_saved()
        if saved:
            return saved

    print("deck-4hum-ai: authorization required.", file=sys.stderr)
    print("", file=sys.stderr)

    try:
        flow = _initiate()
    except Exception as e:
        print(f"Error starting auth flow: {e}", file=sys.stderr)
        sys.exit(1)

    user_code = flow.get("user_code", "")
    verification_url = flow.get("verification_url", f"{APP_URL}/auth/device")
    device_code = flow.get("device_code", "")
    interval = int(flow.get("interval", 5))
    expires_in = int(flow.get("expires_in", 900))

    print(f"  Open this URL in your browser:", file=sys.stderr)
    print(f"  {verification_url}", file=sys.stderr)
    print("", file=sys.stderr)
    print(f"  Confirmation code: {user_code}", file=sys.stderr)
    print("", file=sys.stderr)
    print("  Waiting for authorization...", file=sys.stderr)

    try:
        token, workspace_id = _poll(device_code, interval, expires_in)
    except RuntimeError as e:
        print(f"Auth failed: {e}", file=sys.stderr)
        sys.exit(1)

    _save(token, workspace_id)
    print("  Authorized! Credentials saved to ~/.open-academy/config.json", file=sys.stderr)
    print("", file=sys.stderr)
    return token, workspace_id


def logout() -> None:
    """Remove saved credentials."""
    if CONFIG_PATH.exists():
        CONFIG_PATH.unlink()
        print("Logged out. Credentials removed.", file=sys.stderr)
    else:
        print("Not logged in.", file=sys.stderr)


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "logout":
        logout()
    else:
        token, workspace_id = get_credentials(force_reauth="--reauth" in sys.argv)
        print(f"token={token[:12]}...  workspace_id={workspace_id}")
