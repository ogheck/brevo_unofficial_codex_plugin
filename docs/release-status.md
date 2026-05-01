# Release Status

Current target: `v0.1.1`

Status: not ready to tag.

## Verified

- Plugin validation passes with `python3 scripts/validate_plugin.py`.
- Markdown link checks pass with `python3 scripts/check_markdown_links.py`.
- Integration generator tests pass with `python3 scripts/test_integration_generator.py`.
- All backend example tests pass with `python3 scripts/test_examples.py`.
- Release preflight passes in non-strict mode with `python3 scripts/release_preflight.py`.
- Strict release preflight now checks `BREVO_MCP_TOKEN` and runs `scripts/smoke_brevo_mcp.py`.
- Brevo MCP initialize smoke test passed for contacts, lists, templates, transactional templates, campaign analytics, senders, and domains.
- CI-safe release preflight is available with `python3 scripts/release_preflight.py --skip-marketplace`.
- GitHub Actions validation workflow ran successfully after being added.
- Local marketplace source was added with `codex plugin marketplace add "/Users/danielheck/Documents/New project"`.
- GitHub marketplace source was added with `codex plugin marketplace add ogheck/brevo_unofficial_codex_plugin`.
- GitHub marketplace cache was refreshed with `codex plugin marketplace upgrade brevo-unofficial`; rerun before tagging so it matches the exact tagged commit.
- CLI smoke-test examples were added in `docs/cli-smoke-test-examples.md`.
- GitHub Actions validation has passed on the pushed `main` branch; confirm the latest run matches the exact tagged commit before tagging.
- Default MCP config excludes campaign management, SMS campaigns, WhatsApp campaigns, and webhook management.

## Blocked

- Codex app UI install/load test has not been completed.
- Codex app UI read-tool smoke test still needs to confirm the bundled MCP tools load inside a normal Codex app thread.

## Before Tagging

1. Set `BREVO_MCP_TOKEN` in the Codex runtime environment.
2. Restart Codex.
3. Install Brevo Helper from the Codex app plugin UI.
4. Verify bundled skills load in a new thread.
5. Verify read-oriented Brevo MCP tools initialize.
6. Confirm Codex can inspect lists, templates, senders, domains, and analytics.
7. Confirm there is no direct send, schedule, launch, activation, or enrollment path.
8. Run `python3 scripts/release_preflight.py --strict-live`.
9. Confirm the latest GitHub Actions validation run passed.
10. Move release notes from `Unreleased` into the tagged version section in `CHANGELOG.md`.
11. Tag `v0.1.1`.
