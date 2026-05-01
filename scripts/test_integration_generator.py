#!/usr/bin/env python3
"""Tests for create_integration_stub.py."""

from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

import create_integration_stub as generator


class IntegrationGeneratorTests(unittest.TestCase):
    def test_lists_expected_runtimes(self) -> None:
        choices = generator.runtime_choices()
        self.assertIn("cloudflare-pages-function", choices)
        self.assertIn("nextjs-route-handler", choices)
        self.assertIn("static-html-plus-serverless", choices)

    def test_creates_template_and_notes(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            target = Path(temp_dir) / "brevo"
            planned = generator.copy_template("cloudflare-worker", target)

            self.assertIn(str(target / "BREVO_INTEGRATION_NOTES.md"), planned)
            self.assertTrue((target / "README.md").exists())
            self.assertTrue((target / "src" / "index.js").exists())
            self.assertIn("BREVO_API_KEY", (target / "BREVO_INTEGRATION_NOTES.md").read_text(encoding="utf-8"))

    def test_dry_run_does_not_write(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            target = Path(temp_dir) / "brevo"
            planned = generator.copy_template("nextjs-route-handler", target, dry_run=True)

            self.assertTrue(planned)
            self.assertFalse(target.exists())

    def test_refuses_non_empty_target_without_force(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            target = Path(temp_dir) / "brevo"
            target.mkdir()
            (target / "existing.txt").write_text("keep", encoding="utf-8")

            with self.assertRaises(FileExistsError):
                generator.copy_template("express-endpoint", target)


if __name__ == "__main__":
    unittest.main()
