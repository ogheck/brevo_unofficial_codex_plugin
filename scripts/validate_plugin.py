#!/usr/bin/env python3
"""Validate the Brevo Helper Codex plugin package."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PLUGIN_ROOT = ROOT / "plugins" / "brevo-helper"
MANIFEST = PLUGIN_ROOT / ".codex-plugin" / "plugin.json"
MCP_CONFIG = PLUGIN_ROOT / ".mcp.json"
MARKETPLACE = ROOT / ".agents" / "plugins" / "marketplace.json"

DENIED_MCP_URL_PARTS = (
    "/v1/brevo/mcp",
    "brevo_email_campaign_management",
    "brevo_sms_campaigns",
    "brevo_whatsapp_campaigns",
    "brevo_whatsapp_management",
    "brevo_webhooks_management",
)

RAW_SECRET_PATTERNS = (
    re.compile(r"xkeysib-[A-Za-z0-9_-]{16,}"),
)

ENV_ASSIGNMENT_PATTERN = re.compile(r"\b(BREVO_API_KEY|BREVO_MCP_TOKEN)\s*=\s*(['\"])(.*?)\2")
SAFE_PLACEHOLDER_VALUES = {
    "",
    "test-key",
    "your-token",
    "your-api-key",
    "replace-me",
}


def load_json(path: Path, errors: list[str]) -> dict:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        errors.append(f"Missing required JSON file: {path.relative_to(ROOT)}")
    except json.JSONDecodeError as exc:
        errors.append(f"Invalid JSON in {path.relative_to(ROOT)}: {exc}")
    return {}


def require(condition: bool, message: str, errors: list[str]) -> None:
    if not condition:
        errors.append(message)


def rel(path: Path) -> str:
    return str(path.relative_to(ROOT))


def validate_manifest(errors: list[str]) -> dict:
    manifest = load_json(MANIFEST, errors)
    if not manifest:
        return manifest

    require(manifest.get("name") == "brevo-helper", "Plugin name must be brevo-helper.", errors)
    require(re.fullmatch(r"\d+\.\d+\.\d+", manifest.get("version", "")) is not None, "Plugin version must be semver.", errors)
    require("unofficial" in manifest.get("description", "").lower(), "Manifest description must state unofficial positioning.", errors)
    require(manifest.get("skills") == "./skills/", "Manifest skills path must be ./skills/.", errors)
    require(manifest.get("mcpServers") == "./.mcp.json", "Manifest mcpServers path must be ./.mcp.json.", errors)

    interface = manifest.get("interface", {})
    require(interface.get("displayName") == "Brevo Helper", "Interface displayName must be Brevo Helper.", errors)
    capabilities = set(interface.get("capabilities", []))
    require("Read" in capabilities, "Plugin capabilities must include Read.", errors)
    require("Write" not in capabilities, "Default plugin capabilities must not include Write.", errors)
    long_description = interface.get("longDescription", "").lower()
    require("does not send" in long_description, "Long description must mention no direct sending.", errors)

    for key in ("skills", "mcpServers"):
        value = manifest.get(key)
        if isinstance(value, str) and value.startswith("./"):
            target = PLUGIN_ROOT / value[2:]
            require(target.exists(), f"Manifest path does not exist: {key} -> {value}", errors)

    icon = interface.get("composerIcon")
    if isinstance(icon, str) and icon.startswith("./"):
        require((PLUGIN_ROOT / icon[2:]).exists(), f"Composer icon path does not exist: {icon}", errors)

    return manifest


def validate_marketplace(errors: list[str]) -> None:
    marketplace = load_json(MARKETPLACE, errors)
    if not marketplace:
        return

    entries = marketplace.get("plugins", [])
    require(isinstance(entries, list) and entries, "Marketplace must contain plugin entries.", errors)
    matching = [entry for entry in entries if entry.get("name") == "brevo-helper"]
    require(len(matching) == 1, "Marketplace must contain exactly one brevo-helper entry.", errors)
    if not matching:
        return

    entry = matching[0]
    source = entry.get("source", {})
    require(source.get("source") == "local", "Marketplace source must be local.", errors)
    require(source.get("path") == "./plugins/brevo-helper", "Marketplace path must be ./plugins/brevo-helper.", errors)
    require((ROOT / source.get("path", "")[2:]).exists(), "Marketplace plugin path does not exist.", errors)
    policy = entry.get("policy", {})
    require(policy.get("installation") == "AVAILABLE", "Marketplace installation policy must be AVAILABLE.", errors)
    require(policy.get("authentication") == "ON_USE", "Marketplace auth policy must be ON_USE.", errors)
    require(entry.get("category") == "Productivity", "Marketplace category must be Productivity.", errors)


def validate_mcp(errors: list[str]) -> None:
    config = load_json(MCP_CONFIG, errors)
    servers = config.get("mcpServers", {})
    require(isinstance(servers, dict) and servers, "MCP config must define mcpServers.", errors)

    for name, server in servers.items():
        url = server.get("url", "")
        require(server.get("type") == "http", f"MCP server {name} must use type=http.", errors)
        require(url.startswith("https://mcp.brevo.com/v1/"), f"MCP server {name} must use a Brevo MCP URL.", errors)
        require(server.get("bearer_token_env_var") == "BREVO_MCP_TOKEN", f"MCP server {name} must use BREVO_MCP_TOKEN.", errors)
        for denied in DENIED_MCP_URL_PARTS:
            require(denied not in url, f"MCP server {name} uses denied send-capable endpoint: {url}", errors)


def validate_skills(errors: list[str]) -> None:
    skills_root = PLUGIN_ROOT / "skills"
    require(skills_root.exists(), "Plugin skills directory is missing.", errors)
    skill_files = sorted(skills_root.glob("*/SKILL.md"))
    require(len(skill_files) >= 4, "Expected at least four bundled skills.", errors)

    for skill_file in skill_files:
        text = skill_file.read_text(encoding="utf-8")
        require(text.startswith("---\n"), f"{rel(skill_file)} must start with YAML frontmatter.", errors)
        require("\ndescription:" in text[:500], f"{rel(skill_file)} frontmatter needs a description.", errors)

    umbrella = skills_root / "brevo" / "SKILL.md"
    if umbrella.exists():
        text = umbrella.read_text(encoding="utf-8").lower()
        require("do not send" in text, "Umbrella Brevo skill must include no-send rule.", errors)
        require("dashboard" in text and "handoff" in text, "Umbrella Brevo skill must mention dashboard handoff.", errors)


def validate_text_scan(errors: list[str]) -> None:
    placeholder_marker = "[TO" "DO"

    for path in ROOT.rglob("*"):
        if ".git" in path.parts or not path.is_file():
            continue
        if path.suffix.lower() in {".png", ".jpg", ".jpeg", ".gif", ".webp"}:
            continue
        text = path.read_text(encoding="utf-8", errors="ignore")
        if placeholder_marker in text:
            errors.append(f"Leftover scaffold placeholder in {rel(path)}")
        for pattern in RAW_SECRET_PATTERNS:
            if pattern.search(text):
                errors.append(f"Potential committed Brevo secret in {rel(path)}")
        for match in ENV_ASSIGNMENT_PATTERN.finditer(text):
            value = match.group(3).strip()
            if value.startswith("<") and value.endswith(">"):
                continue
            if value.lower() not in SAFE_PLACEHOLDER_VALUES and not value.lower().startswith("your-"):
                errors.append(f"Potential committed Brevo secret in {rel(path)}")


def main() -> int:
    errors: list[str] = []
    validate_manifest(errors)
    validate_marketplace(errors)
    validate_mcp(errors)
    validate_skills(errors)
    validate_text_scan(errors)

    if errors:
        print("Brevo Helper plugin validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1

    print("Brevo Helper plugin validation passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
