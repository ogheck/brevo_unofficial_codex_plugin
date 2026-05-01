#!/usr/bin/env python3
"""Smoke test bundled Brevo MCP endpoints without printing credentials."""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MCP_CONFIG = ROOT / "plugins" / "brevo-helper" / ".mcp.json"

INITIALIZE_PAYLOAD = {
    "jsonrpc": "2.0",
    "id": 1,
    "method": "initialize",
    "params": {
        "protocolVersion": "2024-11-05",
        "capabilities": {},
        "clientInfo": {
            "name": "brevo-helper-smoke",
            "version": "0.1.1",
        },
    },
}


def load_servers() -> dict[str, dict[str, str]]:
    config = json.loads(MCP_CONFIG.read_text(encoding="utf-8"))
    servers = config.get("mcpServers", {})
    if not isinstance(servers, dict) or not servers:
        raise ValueError("MCP config does not define mcpServers.")
    return servers


def initialize_server(name: str, url: str, token: str, timeout: float) -> tuple[bool, str]:
    request_body = json.dumps(INITIALIZE_PAYLOAD)
    curl_config = "\n".join(
        [
            f"url = {json.dumps(url)}",
            'request = "POST"',
            f"connect-timeout = {timeout}",
            f"max-time = {timeout}",
            'header = "Content-Type: application/json"',
            'header = "Accept: application/json, text/event-stream"',
            f"header = {json.dumps(f'Authorization: Bearer {token}')}",
            f"data = {json.dumps(request_body)}",
            "",
        ]
    )

    try:
        result = subprocess.run(
            ["curl", "-sS", "-o", os.devnull, "-w", "%{http_code}", "--config", "-"],
            input=curl_config,
            text=True,
            capture_output=True,
            check=False,
        )
    except FileNotFoundError:
        return False, "curl is not available"

    if result.returncode != 0:
        detail = result.stderr.strip().splitlines()[-1] if result.stderr.strip() else f"exit {result.returncode}"
        return False, f"{name} could not be reached: {detail}"

    try:
        status = int(result.stdout.strip()[-3:])
    except ValueError:
        return False, f"{name} returned an unreadable HTTP status"

    if 200 <= status < 300:
        return True, f"{name} initialized with HTTP {status}"
    return False, f"{name} returned HTTP {status}"


def main() -> int:
    parser = argparse.ArgumentParser(description="Smoke test Brevo MCP initialize endpoints.")
    parser.add_argument("--server", action="append", help="Server name to test. May be repeated.")
    parser.add_argument("--timeout", type=float, default=15.0, help="Per-server timeout in seconds.")
    args = parser.parse_args()

    token = os.environ.get("BREVO_MCP_TOKEN")
    if not token:
        print("BREVO_MCP_TOKEN is not set.", file=sys.stderr)
        return 1

    servers = load_servers()
    selected = set(args.server or servers.keys())
    unknown = selected.difference(servers.keys())
    if unknown:
        print(f"Unknown MCP server(s): {', '.join(sorted(unknown))}", file=sys.stderr)
        return 1

    failures: list[str] = []
    for name in sorted(selected):
        server = servers[name]
        url = server.get("url")
        if not url:
            failures.append(f"{name} has no URL")
            continue
        ok, message = initialize_server(name, url, token, args.timeout)
        print(("ok: " if ok else "failed: ") + message)
        if not ok:
            failures.append(message)

    if failures:
        print("Brevo MCP smoke test failed.")
        return 1

    print("Brevo MCP smoke test passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
