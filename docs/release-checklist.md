# Release Checklist

Use this checklist before tagging or publishing a Brevo Helper release.

## Static Checks

- Run `python3 scripts/validate_plugin.py`.
- Run `python3 scripts/check_markdown_links.py`.
- Run `python3 scripts/test_integration_generator.py`.
- Run `python3 scripts/test_examples.py`.
- Run `python3 scripts/release_preflight.py`.
- After `BREVO_MCP_TOKEN` is set, run `python3 scripts/smoke_brevo_mcp.py`.
- Confirm the preflight reports a clean git worktree.
- Confirm GitHub Actions validation passes on the pushed commit.
- Confirm the GitHub Actions run is for the commit being tagged.
- Confirm plugin manifest, marketplace JSON, and MCP config parse as valid JSON.
- Confirm no Brevo API key or MCP token is committed.
- Confirm `.mcp.json` does not include campaign send, schedule, SMS, or WhatsApp campaign servers.
- Confirm `.mcp.json` does not include webhook management by default.

## Documentation Checks

- Confirm README install instructions match the current marketplace source.
- Confirm `docs/testing.md` covers local and GitHub marketplace smoke tests.
- Confirm `docs/cli-smoke-test-examples.md` reflects the latest pushed commit before tagging.
- Confirm backend examples document required environment variables.
- Confirm docs state this plugin is unofficial and final send/activation work happens in Brevo.

## Manual Smoke Tests

- Install the plugin from the local marketplace path.
- Install the plugin from `ogheck/brevo_unofficial_codex_plugin` after pushing.
- Restart Codex and confirm the bundled skills load.
- Set `BREVO_MCP_TOKEN` in the Codex runtime environment and verify read-oriented MCP tools initialize.
- Run `python3 scripts/release_preflight.py --strict-live`.
- Ask Codex to review a Brevo campaign and confirm it gives handoff steps instead of attempting to send.
- Ask Codex to build a drip campaign and confirm it produces a plan, copy, backend needs, and manual Brevo setup steps.

## Example Checks

- Review each example for browser-exposed secrets.
- Confirm examples validate inputs before calling Brevo.
- Confirm examples handle duplicate contact behavior.
- Confirm examples return safe public error messages.
- Confirm examples keep sends, schedules, and automation activation outside Codex.

## Versioning

- Update `plugins/brevo-helper/.codex-plugin/plugin.json`.
- Update `PROJECT_ROADMAP.md`.
- Update `docs/release-status.md`.
- Add or update `CHANGELOG.md`.
- Commit changes with a focused release message.
- Tag the release only after static checks and manual smoke tests pass.
