#!/usr/bin/env python3
"""Verify Brevo Helper onboarding state without printing credentials."""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PLUGIN_MANIFEST = ROOT / "plugins" / "brevo-helper" / ".codex-plugin" / "plugin.json"
MARKETPLACE = ROOT / ".agents" / "plugins" / "marketplace.json"
MCP_CONFIG = ROOT / "plugins" / "brevo-helper" / ".mcp.json"

DENIED_MCP_NAMES = {
    "brevo_email_campaign_management",
    "brevo_sms_campaigns",
    "brevo_whatsapp_campaigns",
    "brevo_whatsapp_management",
    "brevo_webhooks_management",
}


@dataclass
class Check:
    status: str
    label: str
    detail: str


def read_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def has_process_env(name: str) -> bool:
    return bool(os.environ.get(name))


def has_launchctl_env(name: str) -> bool:
    if sys.platform != "darwin":
        return False
    try:
        result = subprocess.run(
            ["launchctl", "getenv", name],
            check=False,
            capture_output=True,
            text=True,
        )
    except FileNotFoundError:
        return False
    return result.returncode == 0 and bool(result.stdout.strip())


def secret_location(name: str) -> str | None:
    locations: list[str] = []
    if has_process_env(name):
        locations.append("current process")
    if has_launchctl_env(name):
        locations.append("macOS launch environment")
    if not locations:
        return None
    return ", ".join(locations)


def marketplace_auth_policy() -> tuple[bool, str]:
    marketplace = read_json(MARKETPLACE)
    entries = marketplace.get("plugins", [])
    matching = [entry for entry in entries if entry.get("name") == "brevo-helper"]
    if not matching:
        return False, "brevo-helper marketplace entry is missing"
    policy = matching[0].get("policy", {})
    auth_policy = policy.get("authentication")
    if auth_policy != "ON_INSTALL":
        return False, f"authentication policy is {auth_policy}; expected ON_INSTALL"
    return True, "authentication policy is ON_INSTALL"


def mcp_config_status() -> tuple[bool, str]:
    config = read_json(MCP_CONFIG)
    servers = config.get("mcpServers", {})
    if not isinstance(servers, dict) or not servers:
        return False, "MCP config has no servers"

    bundled_names = set(servers)
    denied = bundled_names.intersection(DENIED_MCP_NAMES)
    if denied:
        return False, f"send-capable or advanced write server bundled by default: {', '.join(sorted(denied))}"

    missing_token_env = [
        name for name, server in servers.items() if server.get("bearer_token_env_var") != "BREVO_MCP_TOKEN"
    ]
    if missing_token_env:
        return False, f"servers missing BREVO_MCP_TOKEN env binding: {', '.join(sorted(missing_token_env))}"

    return True, f"{len(servers)} read-oriented MCP server(s) configured"


def run_command(command: list[str]) -> tuple[bool, str]:
    result = subprocess.run(command, cwd=ROOT, check=False, capture_output=True, text=True)
    output = "\n".join(part for part in (result.stdout.strip(), result.stderr.strip()) if part)
    return result.returncode == 0, output


def build_checks(args: argparse.Namespace) -> list[Check]:
    checks: list[Check] = []

    try:
        manifest = read_json(PLUGIN_MANIFEST)
        checks.append(Check("ok", "plugin manifest", f"{manifest.get('name')} {manifest.get('version')}"))
    except (OSError, json.JSONDecodeError) as exc:
        return [Check("blocked", "plugin manifest", str(exc))]

    try:
        ok, detail = marketplace_auth_policy()
        checks.append(Check("ok" if ok else "blocked", "install-time auth policy", detail))
    except (OSError, json.JSONDecodeError) as exc:
        checks.append(Check("blocked", "install-time auth policy", str(exc)))

    try:
        ok, detail = mcp_config_status()
        checks.append(Check("ok" if ok else "blocked", "MCP safety config", detail))
    except (OSError, json.JSONDecodeError) as exc:
        checks.append(Check("blocked", "MCP safety config", str(exc)))

    mcp_location = secret_location("BREVO_MCP_TOKEN")
    if mcp_location:
        checks.append(Check("ok", "BREVO_MCP_TOKEN", f"set in {mcp_location}"))
    else:
        checks.append(Check("blocked", "BREVO_MCP_TOKEN", "not set in current process or macOS launch environment"))

    api_location = secret_location("BREVO_API_KEY")
    if api_location:
        checks.append(Check("ok", "BREVO_API_KEY", f"set in {api_location}"))
    elif args.require_api_key:
        checks.append(Check("blocked", "BREVO_API_KEY", "required but not set"))
    else:
        checks.append(Check("warn", "BREVO_API_KEY", "not set; only required for server-side app integrations"))

    if args.skip_mcp_smoke:
        checks.append(Check("info", "MCP tools/list smoke", "skipped by --skip-mcp-smoke"))
    elif not has_process_env("BREVO_MCP_TOKEN"):
        checks.append(
            Check(
                "blocked",
                "MCP tools/list smoke",
                "BREVO_MCP_TOKEN must be set in this process to run scripts/smoke_brevo_mcp.py",
            )
        )
    else:
        ok, output = run_command(
            [
                sys.executable,
                "scripts/smoke_brevo_mcp.py",
                "--server",
                "brevo_contacts",
                "--tools-list",
                "--timeout",
                "8",
            ]
        )
        checks.append(Check("ok" if ok else "blocked", "MCP tools/list smoke", summarize_smoke_output(output)))

    checks.append(
        Check(
            "info",
            "manual Brevo review",
            "verify sender identity, domain authentication, and dedicated/authorized IP settings in Brevo if used",
        )
    )
    return checks


def summarize_smoke_output(output: str) -> str:
    if not output:
        return "no output"
    if "Brevo MCP smoke test passed." in output:
        ok_lines = [line for line in output.splitlines() if line.startswith("ok: ")]
        return f"passed ({len(ok_lines)} endpoint checks)"
    failed_lines = [line for line in output.splitlines() if line.startswith("failed: ")]
    if failed_lines:
        return "; ".join(failed_lines[:3])
    lines = [line for line in output.splitlines() if line.strip()]
    return lines[-1] if lines else "failed"


def print_checks(checks: list[Check]) -> None:
    print("Brevo Helper onboarding check")
    print(f"repo: {ROOT}")
    print()
    for check in checks:
        print(f"{check.status:7} {check.label:24} {check.detail}")


def main() -> int:
    parser = argparse.ArgumentParser(description="Verify Brevo Helper onboarding state.")
    parser.add_argument("--require-api-key", action="store_true", help="Fail if BREVO_API_KEY is not available.")
    parser.add_argument("--skip-mcp-smoke", action="store_true", help="Skip live Brevo MCP initialize smoke.")
    parser.add_argument("--warn-only", action="store_true", help="Always exit 0 after printing the report.")
    args = parser.parse_args()

    checks = build_checks(args)
    print_checks(checks)

    blocked = [check for check in checks if check.status == "blocked"]
    if blocked and not args.warn_only:
        print()
        print("Brevo Helper onboarding check failed.")
        return 1

    print()
    print("Brevo Helper onboarding check passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
