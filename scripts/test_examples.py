#!/usr/bin/env python3
"""Run Node test suites for all Brevo backend examples."""

from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
EXAMPLES = (
    "cloudflare-pages-function",
    "cloudflare-worker",
    "nextjs-route-handler",
    "express-endpoint",
    "static-html-plus-serverless",
)


def main() -> int:
    node = os.environ.get("NODE_BIN", "node")
    failures: list[str] = []

    for name in EXAMPLES:
        cwd = ROOT / "examples" / name
        print(f"==> {name}")
        result = subprocess.run([node, "--test"], cwd=cwd, check=False)
        if result.returncode != 0:
            failures.append(name)

    if failures:
        print("Example test failures:")
        for failure in failures:
            print(f"- {failure}")
        return 1

    print("All example tests passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
