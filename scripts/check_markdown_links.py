#!/usr/bin/env python3
"""Check local Markdown links in repository docs."""

from __future__ import annotations

import re
import sys
from pathlib import Path
from urllib.parse import unquote


ROOT = Path(__file__).resolve().parents[1]
LINK_PATTERN = re.compile(r"(?<!!)\[[^\]]+\]\(([^)]+)\)")
EXTERNAL_PREFIXES = ("http://", "https://", "mailto:", "#")


def normalize_target(raw_target: str) -> str | None:
    target = raw_target.strip()
    if not target or target.startswith(EXTERNAL_PREFIXES):
        return None
    if target.startswith("<") and target.endswith(">"):
        target = target[1:-1]
    if " " in target and not target.startswith("./") and not target.startswith("../"):
        return None
    target = target.split("#", 1)[0]
    target = unquote(target)
    return target or None


def main() -> int:
    errors: list[str] = []
    markdown_files = sorted(path for path in ROOT.rglob("*.md") if ".git" not in path.parts)

    for markdown_file in markdown_files:
        text = markdown_file.read_text(encoding="utf-8")
        for line_number, line in enumerate(text.splitlines(), start=1):
            for match in LINK_PATTERN.finditer(line):
                target = normalize_target(match.group(1))
                if target is None:
                    continue
                resolved = (markdown_file.parent / target).resolve()
                try:
                    resolved.relative_to(ROOT)
                except ValueError:
                    errors.append(f"{markdown_file.relative_to(ROOT)}:{line_number}: link escapes repo: {target}")
                    continue
                if not resolved.exists():
                    errors.append(f"{markdown_file.relative_to(ROOT)}:{line_number}: missing link target: {target}")

    if errors:
        print("Markdown link check failed:")
        for error in errors:
            print(f"- {error}")
        return 1

    print("Markdown link check passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
