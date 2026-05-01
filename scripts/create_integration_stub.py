#!/usr/bin/env python3
"""Create a Brevo backend integration stub from a bundled template."""

from __future__ import annotations

import argparse
import shutil
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
EXAMPLES = ROOT / "examples"
RUNTIMES = {
    "cloudflare-pages-function": EXAMPLES / "cloudflare-pages-function",
    "cloudflare-worker": EXAMPLES / "cloudflare-worker",
    "nextjs-route-handler": EXAMPLES / "nextjs-route-handler",
    "express-endpoint": EXAMPLES / "express-endpoint",
    "static-html-plus-serverless": EXAMPLES / "static-html-plus-serverless",
}

NOTES = """# Brevo Integration Notes

This stub was generated from a Brevo Helper backend template.

## Required Server-Side Environment Variables

- `BREVO_API_KEY`: Brevo API key for the application backend only.
- `BREVO_LIST_IDS`: Comma-separated Brevo list IDs.
- `ALLOWED_ORIGINS`: Optional comma-separated browser origins for CORS.

## Safety Rules

- Do not place `BREVO_API_KEY` in browser JavaScript, static HTML, or public environment variables.
- Do not use `BREVO_MCP_TOKEN` in application runtime code. It is for Codex MCP access only.
- Do not send, schedule, launch, activate, or enroll contacts into live Brevo messaging flows from Codex.

## Manual Brevo Handoff

1. Confirm target list IDs in Brevo.
2. Confirm contact attributes exist before using them in production.
3. Confirm sender/domain setup if the captured contacts will receive email later.
4. Manually configure and activate related campaigns or automations inside Brevo after tests pass.
"""


def runtime_choices() -> str:
    return ", ".join(sorted(RUNTIMES))


def copy_template(runtime: str, target: Path, force: bool = False, dry_run: bool = False) -> list[str]:
    source = RUNTIMES[runtime]
    if not source.exists():
        raise FileNotFoundError(f"Template missing: {source}")

    if target.exists() and any(target.iterdir()) and not force:
        raise FileExistsError(f"Target directory is not empty: {target}")

    planned: list[str] = []
    for path in sorted(source.rglob("*")):
        if path.is_dir():
            continue
        relative = path.relative_to(source)
        destination = target / relative
        planned.append(str(destination))
        if dry_run:
            continue
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(path, destination)

    notes_path = target / "BREVO_INTEGRATION_NOTES.md"
    planned.append(str(notes_path))
    if not dry_run:
        target.mkdir(parents=True, exist_ok=True)
        notes_path.write_text(NOTES, encoding="utf-8")

    return planned


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Create a Brevo backend integration stub.")
    parser.add_argument("--runtime", choices=sorted(RUNTIMES), help="Template runtime to copy.")
    parser.add_argument("--target", type=Path, help="Target directory for generated files.")
    parser.add_argument("--force", action="store_true", help="Allow copying into a non-empty target directory.")
    parser.add_argument("--dry-run", action="store_true", help="Print planned files without writing.")
    parser.add_argument("--list", action="store_true", help="List available runtimes.")
    args = parser.parse_args(argv)

    if args.list:
        print(runtime_choices())
        return 0

    if not args.runtime or not args.target:
        parser.error("--runtime and --target are required unless --list is used")

    target = args.target.expanduser().resolve()
    try:
        planned = copy_template(args.runtime, target, force=args.force, dry_run=args.dry_run)
    except (FileExistsError, FileNotFoundError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1

    action = "Would create" if args.dry_run else "Created"
    print(f"{action} Brevo {args.runtime} integration stub at {target}")
    for path in planned:
        print(f"- {path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
