#!/usr/bin/env python3
"""Smoke test bundled Brevo MCP endpoints without printing credentials."""

from __future__ import annotations

import argparse
import ipaddress
import json
import os
import re
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

TOOLS_LIST_PAYLOAD = {
    "jsonrpc": "2.0",
    "id": 2,
    "method": "tools/list",
    "params": {},
}

IP_CANDIDATE_PATTERN = re.compile(r"\b(?:\d{1,3}\.){3}\d{1,3}\b|[0-9A-Fa-f:]{2,}")


def load_servers() -> dict[str, dict[str, str]]:
    config = json.loads(MCP_CONFIG.read_text(encoding="utf-8"))
    servers = config.get("mcpServers", {})
    if not isinstance(servers, dict) or not servers:
        raise ValueError("MCP config does not define mcpServers.")
    return servers


def redact(text: str, token: str) -> str:
    if token:
        text = text.replace(token, "[redacted]")
    return text


def extract_ip_addresses(text: str) -> list[str]:
    found: list[str] = []
    for candidate in IP_CANDIDATE_PATTERN.findall(text):
        try:
            address = str(ipaddress.ip_address(candidate.strip("[]")))
        except ValueError:
            continue
        if address not in found:
            found.append(address)
    return found


def summarize_body(body: str, token: str) -> str:
    clean = redact(body.strip(), token)
    if not clean:
        return "empty response"

    addresses = extract_ip_addresses(clean)
    if addresses:
        return f"authorized IP blocker; add {', '.join(addresses)} in Brevo Authorized IPs"

    for line in clean.splitlines():
        if line.startswith("data:"):
            payload = line.removeprefix("data:").strip()
            try:
                decoded = json.loads(payload)
            except json.JSONDecodeError:
                continue
            error = decoded.get("error")
            if isinstance(error, dict):
                message = error.get("message") or error.get("code")
                if message:
                    return str(message)[:300]
            result = decoded.get("result")
            if isinstance(result, dict) and isinstance(result.get("tools"), list):
                return f"{len(result['tools'])} tool(s) listed"

    try:
        decoded = json.loads(clean)
    except json.JSONDecodeError:
        return clean[:300]

    error = decoded.get("error")
    if isinstance(error, dict):
        message = error.get("message") or error.get("code")
        if message:
            return str(message)[:300]
    result = decoded.get("result")
    if isinstance(result, dict) and isinstance(result.get("tools"), list):
        return f"{len(result['tools'])} tool(s) listed"
    return clean[:300]


def post_mcp_request(name: str, url: str, token: str, payload: dict, timeout: float) -> tuple[bool, int | None, str]:
    request_body = json.dumps(payload)
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
            ["curl", "-sS", "-w", "\n%{http_code}", "--config", "-"],
            input=curl_config,
            text=True,
            capture_output=True,
            check=False,
        )
    except FileNotFoundError:
        return False, None, "curl is not available"

    if result.returncode != 0:
        detail = result.stderr.strip().splitlines()[-1] if result.stderr.strip() else f"exit {result.returncode}"
        return False, None, f"{name} could not be reached: {redact(detail, token)}"

    stdout = result.stdout.rstrip("\n")
    body, _, status_text = stdout.rpartition("\n")
    try:
        status = int(status_text)
    except ValueError:
        return False, None, f"{name} returned an unreadable HTTP status"

    return 200 <= status < 300, status, body


def initialize_server(name: str, url: str, token: str, timeout: float) -> tuple[bool, str]:
    ok, status, body = post_mcp_request(name, url, token, INITIALIZE_PAYLOAD, timeout)
    if ok:
        return True, f"{name} initialized with HTTP {status}"
    if status is None:
        return False, body
    return False, f"{name} initialize returned HTTP {status}: {summarize_body(body, token)}"


def list_server_tools(name: str, url: str, token: str, timeout: float) -> tuple[bool, str]:
    ok, status, body = post_mcp_request(name, url, token, TOOLS_LIST_PAYLOAD, timeout)
    summary = summarize_body(body, token)
    if ok and "tool(s) listed" in summary:
        return True, f"{name} tools/list returned {summary}"
    if ok:
        return False, f"{name} tools/list returned HTTP {status}: {summary}"
    if status is None:
        return False, body
    return False, f"{name} tools/list returned HTTP {status}: {summary}"


def main() -> int:
    parser = argparse.ArgumentParser(description="Smoke test bundled Brevo MCP endpoints.")
    parser.add_argument("--server", action="append", help="Server name to test. May be repeated.")
    parser.add_argument("--timeout", type=float, default=15.0, help="Per-server timeout in seconds.")
    parser.add_argument("--tools-list", action="store_true", help="Also call MCP tools/list to catch authorization/IP allowlist blockers.")
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
            continue
        if args.tools_list:
            ok, message = list_server_tools(name, url, token, args.timeout)
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
