#!/usr/bin/env python3
"""Check local Codex marketplace/cache/install state for Brevo Helper."""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
import tomllib
from dataclasses import dataclass
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
PLUGIN_MANIFEST = ROOT / "plugins" / "brevo-helper" / ".codex-plugin" / "plugin.json"
MARKETPLACE_MANIFEST = ROOT / ".agents" / "plugins" / "marketplace.json"


@dataclass
class Check:
    status: str
    label: str
    detail: str


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def codex_home_default() -> Path:
    configured = os.environ.get("CODEX_HOME")
    if configured:
        return Path(configured).expanduser()
    return Path.home() / ".codex"


def git_output(command: list[str], cwd: Path) -> str | None:
    result = subprocess.run(command, cwd=cwd, check=False, capture_output=True, text=True)
    if result.returncode != 0:
        return None
    return result.stdout.strip()


def short_revision(revision: str | None) -> str:
    if not revision:
        return "unknown"
    return revision[:8]


def load_codex_config(config_path: Path) -> dict[str, Any] | None:
    try:
        return tomllib.loads(config_path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        return None


def plugin_config_matches(config: dict[str, Any], plugin_name: str, marketplace_name: str) -> list[tuple[str, bool]]:
    plugin_table = config.get("plugins", {})
    if not isinstance(plugin_table, dict):
        return []

    matches: list[tuple[str, bool]] = []
    expected_key = f"{plugin_name}@{marketplace_name}"
    for key, value in plugin_table.items():
        if key != plugin_name and key != expected_key and not key.startswith(f"{plugin_name}@"):
            continue
        enabled = True
        if isinstance(value, dict) and value.get("enabled") is False:
            enabled = False
        matches.append((key, enabled))
    return matches


def find_installed_plugin_manifests(cache_root: Path, plugin_name: str) -> list[Path]:
    if not cache_root.exists():
        return []

    matches: list[Path] = []
    for manifest_path in cache_root.rglob("plugin.json"):
        if manifest_path.parent.name != ".codex-plugin":
            continue
        try:
            manifest = read_json(manifest_path)
        except (OSError, json.JSONDecodeError):
            continue
        if manifest.get("name") == plugin_name:
            matches.append(manifest_path)
    return sorted(matches)


def build_checks(codex_home: Path) -> list[Check]:
    checks: list[Check] = []

    try:
        plugin_manifest = read_json(PLUGIN_MANIFEST)
        plugin_name = str(plugin_manifest.get("name", ""))
        plugin_version = str(plugin_manifest.get("version", "unknown"))
        checks.append(Check("ok", "repo plugin manifest", f"{plugin_name} {plugin_version}"))
    except (OSError, json.JSONDecodeError) as exc:
        return [Check("blocked", "repo plugin manifest", str(exc))]

    try:
        marketplace_manifest = read_json(MARKETPLACE_MANIFEST)
        marketplace_name = str(marketplace_manifest.get("name", ""))
        checks.append(Check("ok", "repo marketplace manifest", marketplace_name))
    except (OSError, json.JSONDecodeError) as exc:
        return checks + [Check("blocked", "repo marketplace manifest", str(exc))]

    config_path = codex_home / "config.toml"
    config = load_codex_config(config_path)
    if config is None:
        return checks + [Check("blocked", "Codex config", f"missing {config_path}")]
    checks.append(Check("ok", "Codex config", "config.toml found"))

    marketplaces = config.get("marketplaces", {})
    marketplace_config = marketplaces.get(marketplace_name) if isinstance(marketplaces, dict) else None
    if not isinstance(marketplace_config, dict):
        checks.append(Check("blocked", "marketplace registration", f"{marketplace_name} is not registered"))
    else:
        source_type = marketplace_config.get("source_type", "unknown")
        checks.append(Check("ok", "marketplace registration", f"{marketplace_name} registered as {source_type}"))

        local_head = git_output(["git", "rev-parse", "HEAD"], ROOT)
        registered_revision = marketplace_config.get("last_revision")
        if registered_revision and local_head:
            if registered_revision == local_head:
                checks.append(Check("ok", "registered revision", f"matches repo HEAD {short_revision(local_head)}"))
            else:
                checks.append(
                    Check(
                        "blocked",
                        "registered revision",
                        f"{short_revision(registered_revision)} does not match repo HEAD {short_revision(local_head)}",
                    )
                )
        elif registered_revision:
            checks.append(Check("info", "registered revision", f"registered {short_revision(str(registered_revision))}"))
        else:
            checks.append(Check("info", "registered revision", "not recorded for this marketplace source"))

    marketplace_cache = codex_home / ".tmp" / "marketplaces" / marketplace_name
    cached_manifest = marketplace_cache / "plugins" / plugin_name / ".codex-plugin" / "plugin.json"
    if marketplace_cache.exists():
        checks.append(Check("ok", "marketplace cache", str(marketplace_cache)))
    else:
        checks.append(Check("blocked", "marketplace cache", f"missing {marketplace_cache}"))

    if cached_manifest.exists():
        checks.append(Check("ok", "cached plugin manifest", f"{plugin_name} is available in marketplace cache"))
    else:
        checks.append(Check("blocked", "cached plugin manifest", f"missing {cached_manifest}"))

    install_metadata = marketplace_cache / ".codex-marketplace-install.json"
    if install_metadata.exists():
        try:
            install = read_json(install_metadata)
            revision = install.get("revision")
            local_head = git_output(["git", "rev-parse", "HEAD"], ROOT)
            if revision and local_head and revision == local_head:
                checks.append(Check("ok", "cached checkout revision", f"matches repo HEAD {short_revision(local_head)}"))
            elif revision and local_head:
                checks.append(
                    Check(
                        "blocked",
                        "cached checkout revision",
                        f"{short_revision(str(revision))} does not match repo HEAD {short_revision(local_head)}",
                    )
                )
            elif revision:
                checks.append(Check("info", "cached checkout revision", f"cached {short_revision(str(revision))}"))
        except (OSError, json.JSONDecodeError) as exc:
            checks.append(Check("warn", "cached checkout revision", f"could not read install metadata: {exc}"))

    config_matches = plugin_config_matches(config, plugin_name, marketplace_name)
    enabled_matches = [key for key, enabled in config_matches if enabled]
    disabled_matches = [key for key, enabled in config_matches if not enabled]
    if enabled_matches:
        checks.append(Check("ok", "plugin enabled config", ", ".join(enabled_matches)))
    elif disabled_matches:
        checks.append(Check("blocked", "plugin enabled config", f"present but disabled: {', '.join(disabled_matches)}"))
    else:
        expected_key = f'{plugin_name}@{marketplace_name}'
        checks.append(Check("blocked", "plugin enabled config", f'no [plugins."{expected_key}"] entry found'))

    installed_manifests = find_installed_plugin_manifests(codex_home / "plugins" / "cache", plugin_name)
    if installed_manifests:
        locations = [str(path.parent.parent) for path in installed_manifests]
        checks.append(Check("ok", "installed plugin cache", "; ".join(locations)))
    else:
        checks.append(Check("blocked", "installed plugin cache", f"no {plugin_name} install found under plugins/cache"))

    checks.append(
        Check(
            "info",
            "session load",
            "after installing, restart Codex and open a new thread to confirm Brevo Helper skills appear",
        )
    )
    return checks


def print_checks(checks: list[Check], codex_home: Path) -> None:
    print("Codex app plugin state check")
    print(f"repo: {ROOT}")
    print(f"codex home: {codex_home}")
    print()
    for check in checks:
        print(f"{check.status:7} {check.label:26} {check.detail}")


def main() -> int:
    parser = argparse.ArgumentParser(description="Check local Codex install state for Brevo Helper.")
    parser.add_argument("--codex-home", type=Path, default=codex_home_default(), help="Codex home directory to inspect.")
    parser.add_argument("--warn-only", action="store_true", help="Always exit 0 after printing the diagnostic report.")
    args = parser.parse_args()

    codex_home = args.codex_home.expanduser()
    checks = build_checks(codex_home)
    print_checks(checks, codex_home)

    blocked = [check for check in checks if check.status == "blocked"]
    if blocked and not args.warn_only:
        print()
        print("Codex plugin state check failed.")
        return 1

    print()
    print("Codex plugin state check passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
