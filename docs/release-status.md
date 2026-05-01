# Release Status

Current target: `v0.1.1`

Status: not ready to tag.

## Verified

- Plugin validation passes with `python3 scripts/validate_plugin.py`.
- Markdown link checks pass with `python3 scripts/check_markdown_links.py`.
- All backend example tests pass with `python3 scripts/test_examples.py`.
- Local marketplace source was added with `codex plugin marketplace add "/Users/danielheck/Documents/New project"`.
- GitHub marketplace source was added with `codex plugin marketplace add ogheck/brevo_unofficial_codex_plugin`.
- GitHub marketplace cache was refreshed with `codex plugin marketplace upgrade brevo-unofficial`.
- Default MCP config excludes campaign management, SMS campaigns, WhatsApp campaigns, and webhook management.

## Blocked

- Codex app UI install/load test has not been completed.
- Brevo MCP auth smoke test has not been completed because `BREVO_MCP_TOKEN` is not set in the current environment.

## Before Tagging

1. Set `BREVO_MCP_TOKEN` in the Codex runtime environment.
2. Restart Codex.
3. Install Brevo Helper from the Codex app plugin UI.
4. Verify bundled skills load in a new thread.
5. Verify read-oriented Brevo MCP tools initialize.
6. Confirm Codex can inspect lists, templates, senders, domains, and analytics.
7. Confirm there is no direct send, schedule, launch, activation, or enrollment path.
8. Move release notes from `Unreleased` into the tagged version section in `CHANGELOG.md`.
9. Tag `v0.1.1`.
