#!/usr/bin/env python3
"""Run Brevo Helper release preflight checks."""

from __future__ import annotations

import argparse
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CODEX_NODE = Path.home() / ".cache" / "codex-runtimes" / "codex-primary-runtime" / "dependencies" / "node" / "bin" / "node"
MARKETPLACE_CACHE = Path.home() / ".codex" / ".tmp" / "marketplaces" / "brevo-unofficial"


def run_check(label: str, command: list[str], env: dict[str, str] | None = None) -> bool:
    print(f"==> {label}", flush=True)
    result = subprocess.run(command, cwd=ROOT, env=env, check=False)
    if result.returncode == 0:
        print(f"ok: {label}")
        return True
    print(f"failed: {label}")
    return False


def output(command: list[str], cwd: Path = ROOT) -> str | None:
    result = subprocess.run(command, cwd=cwd, check=False, capture_output=True, text=True)
    if result.returncode != 0:
        return None
    return result.stdout.strip()


def node_bin() -> str:
    if os.environ.get("NODE_BIN"):
        return os.environ["NODE_BIN"]
    if CODEX_NODE.exists():
        return str(CODEX_NODE)
    found = shutil.which("node")
    return found or "node"


def manifest_version() -> str:
    manifest = json.loads((ROOT / "plugins" / "brevo-helper" / ".codex-plugin" / "plugin.json").read_text(encoding="utf-8"))
    return str(manifest.get("version", "unknown"))


def marketplace_revision_status() -> tuple[bool, str]:
    local_head = output(["git", "rev-parse", "--short", "HEAD"])
    if not MARKETPLACE_CACHE.exists():
        return False, f"marketplace cache missing: {MARKETPLACE_CACHE}"

    cache_head = output(["git", "rev-parse", "--short", "HEAD"], cwd=MARKETPLACE_CACHE)
    if not cache_head:
        return False, f"marketplace cache is not a readable git checkout: {MARKETPLACE_CACHE}"
    if local_head != cache_head:
        return False, f"marketplace cache revision {cache_head} does not match local revision {local_head}"
    return True, f"marketplace cache revision matches local revision {local_head}"


def worktree_status() -> tuple[bool, str]:
    status = output(["git", "status", "--short"])
    if status:
        return False, f"working tree has uncommitted changes:\n{status}"
    return True, "working tree is clean"


def live_blockers() -> list[str]:
    blockers: list[str] = []
    if not os.environ.get("BREVO_MCP_TOKEN"):
        blockers.append("BREVO_MCP_TOKEN is not set in this environment.")
    return blockers


def main() -> int:
    parser = argparse.ArgumentParser(description="Run Brevo Helper release preflight checks.")
    parser.add_argument("--strict-live", action="store_true", help="Fail if live Brevo/Codex app checks are still blocked.")
    parser.add_argument("--skip-marketplace", action="store_true", help="Skip local Codex marketplace cache revision check.")
    parser.add_argument("--check-codex-app", action="store_true", help="Also check local Codex app marketplace/plugin install state.")
    args = parser.parse_args()

    env = os.environ.copy()
    env["NODE_BIN"] = node_bin()

    checks = [
        run_check("plugin package validation", [sys.executable, "scripts/validate_plugin.py"]),
        run_check("markdown link validation", [sys.executable, "scripts/check_markdown_links.py"]),
        run_check("integration generator tests", [sys.executable, "scripts/test_integration_generator.py"]),
        run_check("backend example tests", [sys.executable, "scripts/test_examples.py"], env=env),
    ]

    worktree_ok, worktree_message = worktree_status()
    print("==> git worktree")
    print(("ok: " if worktree_ok else "blocked: ") + worktree_message)
    checks.append(worktree_ok)

    print("==> marketplace cache")
    if args.skip_marketplace:
        print("skipped: local Codex marketplace cache check")
    else:
        marketplace_ok, marketplace_message = marketplace_revision_status()
        print(("ok: " if marketplace_ok else "blocked: ") + marketplace_message)
        checks.append(marketplace_ok)

    version = manifest_version()
    print(f"==> version")
    print(f"ok: plugin manifest version is {version}")

    print("==> Codex app plugin state")
    if args.check_codex_app:
        checks.append(run_check("Codex app plugin install state", [sys.executable, "scripts/check_codex_plugin_state.py"]))
    else:
        print("skipped: run python3 scripts/check_codex_plugin_state.py before tagging")

    blockers = live_blockers()
    if blockers:
        print("==> live blockers")
        for blocker in blockers:
            print(f"- {blocker}")
        if args.strict_live:
            checks.append(False)
    else:
        print("==> live blockers")
        print("ok: BREVO_MCP_TOKEN is set. Run Codex app and Brevo MCP smoke tests before tagging.")
        if args.strict_live:
            checks.append(run_check("Brevo MCP initialize smoke test", [sys.executable, "scripts/smoke_brevo_mcp.py"]))

    if not all(checks):
        print("Release preflight failed.")
        return 1

    if blockers:
        print("Static preflight passed. Release remains blocked on live smoke tests.")
    else:
        print("Static preflight passed. Continue with Codex app UI and Brevo MCP smoke tests.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
