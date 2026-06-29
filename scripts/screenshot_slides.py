#!/usr/bin/env python3
"""
Screenshot slide render pages with production auth.

Usage:
    python scripts/screenshot_slides.py <deck_id> <slide_count> <out_dir> [base_url] [--start N]

Options:
    --start N            Begin at slide index N (0-based). Default: 0.
    SLIDE_INDICES env    Comma-separated 0-based indices (overrides --start/count).

Requires:
    pip install playwright
    python -m playwright install chromium

Token is NEVER printed to stdout or stderr.
Reads from OPEN_ACADEMY_TOKEN env or ~/.open-academy/config.json.

Exit codes:
    0  — at least one slide saved
    1  — bad arguments or no token found
    2  — all requested slides failed (zero saved)
"""
import json
import os
import sys
from pathlib import Path
from urllib.parse import urlparse

FALLBACK_API_HOST = "open-academy-api-mz4xquo5lq-as.a.run.app"
CONFIG_PATH = Path.home() / ".open-academy" / "config.json"


def _host_from_url(value):
    if not value or not isinstance(value, str):
        return None
    try:
        parsed = urlparse(value)
        if parsed.scheme:
            return parsed.netloc or None
        return value.split("/")[0] or None
    except Exception:
        return None


def main():
    argv = sys.argv[1:]

    # Extract --start N flag before positional arg parsing
    start_index = 0
    if "--start" in argv:
        i = argv.index("--start")
        try:
            start_index = int(argv[i + 1])
            if start_index < 0:
                raise ValueError
        except (IndexError, ValueError):
            print("ERROR: --start requires a non-negative integer", file=sys.stderr)
            sys.exit(1)
        argv = argv[:i] + argv[i + 2:]

    if len(argv) < 3:
        print(
            "Usage: python scripts/screenshot_slides.py"
            " <deck_id> <slide_count> <out_dir> [base_url] [--start N]",
            file=sys.stderr,
        )
        sys.exit(1)

    deck_id = argv[0]
    try:
        slide_count = int(argv[1])
    except ValueError:
        print("ERROR: slide_count must be an integer", file=sys.stderr)
        sys.exit(1)
    out_dir = Path(argv[2])
    base_url = argv[3] if len(argv) > 3 else "https://deck.4hum.ai"

    # Load config (token never printed)
    cfg = {}
    if CONFIG_PATH.exists():
        try:
            cfg = json.loads(CONFIG_PATH.read_text())
        except Exception:
            pass

    token = os.environ.get("OPEN_ACADEMY_TOKEN") or cfg.get("token")
    if not token:
        print(
            "ERROR: No auth token found."
            " Set OPEN_ACADEMY_TOKEN or run `python scripts/auth.py`.",
            file=sys.stderr,
        )
        sys.exit(1)

    api_host = (
        _host_from_url(os.environ.get("OPEN_ACADEMY_API_URL"))
        or _host_from_url(cfg.get("apiUrl"))
        or _host_from_url(cfg.get("api_url"))
        or FALLBACK_API_HOST
    )
    print(f"API host: {api_host}", file=sys.stderr)

    # Resolve which slide indices to capture
    slide_indices_env = os.environ.get("SLIDE_INDICES")
    if slide_indices_env:
        indices = []
        for s in slide_indices_env.split(","):
            try:
                n = int(s.strip())
                if n >= 0:
                    indices.append(n)
            except ValueError:
                pass
        if not indices:
            print(
                "ERROR: SLIDE_INDICES set but contained no valid 0-based indices",
                file=sys.stderr,
            )
            sys.exit(1)
    else:
        indices = list(range(start_index, slide_count))

    out_dir.mkdir(parents=True, exist_ok=True)

    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        print(
            "ERROR: playwright not installed."
            " Run: pip install playwright && python -m playwright install chromium",
            file=sys.stderr,
        )
        sys.exit(1)

    saved_count = 0
    not_found_count = 0

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(viewport={"width": 1920, "height": 1080})

        # Inject Authorization header for all API calls — token never logged
        def _handle_route(route):
            headers = {**route.request.headers, "authorization": f"Bearer {token}"}
            route.continue_(headers=headers)

        context.route(f"**/{api_host}/**", _handle_route)

        for i, n in enumerate(indices):
            url = f"{base_url}/slides/{deck_id}/{n}/render"
            print(f"Slide {n} ({i + 1}/{len(indices)}): {url}", file=sys.stderr)
            page = context.new_page()
            try:
                page.goto(url, wait_until="networkidle", timeout=45000)

                ready = True
                try:
                    page.wait_for_function(
                        "document.body?.dataset?.renderReady === 'true'",
                        timeout=20000,
                    )
                except Exception:
                    ready = False

                if not ready:
                    try:
                        body_text = page.evaluate(
                            "document.querySelector('body')?.innerText || ''"
                        )
                        if "Deck not found" in body_text:
                            print(
                                f"  WARNING: slide {n} — 'Deck not found' error page"
                                " (deck may be private, ID wrong, or auth failed). Skipping.",
                                file=sys.stderr,
                            )
                            not_found_count += 1
                            page.close()
                            continue
                    except Exception:
                        pass
                    print(
                        f"  renderReady timeout on slide {n} — waiting 10s",
                        file=sys.stderr,
                    )
                    page.wait_for_timeout(10000)

                path = out_dir / f"slide_{n + 1:02d}.png"
                page.screenshot(path=str(path))
                print(f"SAVED:{path}")
                saved_count += 1
            except Exception as exc:
                print(f"  Error slide {n}: {exc}", file=sys.stderr)
            page.close()

        browser.close()

    print(
        f"Done: {saved_count} saved, {not_found_count} not-found,"
        f" of {len(indices)} requested.",
        file=sys.stderr,
    )
    if saved_count == 0:
        sys.exit(2)


if __name__ == "__main__":
    main()
