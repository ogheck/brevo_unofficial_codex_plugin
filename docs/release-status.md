# Release Status

Current target: `v0.1.1`

Status: not ready to tag.

## Verified

- Plugin validation passes with `python3 scripts/validate_plugin.py`.
- Markdown link checks pass with `python3 scripts/check_markdown_links.py`.
- Integration generator tests pass with `python3 scripts/test_integration_generator.py`.
- All backend example tests pass with `python3 scripts/test_examples.py`.
- Release preflight passes in non-strict mode with `python3 scripts/release_preflight.py`.
- Strict release preflight passes with `python3 scripts/release_preflight.py --strict-live`.
- Strict release preflight including the app install-state diagnostic passes with `python3 scripts/release_preflight.py --strict-live --check-codex-app`.
- Brevo MCP initialize smoke test passed for contacts, lists, templates, transactional templates, campaign analytics, senders, and domains.
- Codex app plugin state diagnostic passes with `python3 scripts/check_codex_plugin_state.py`.
- Codex config shows `brevo-helper@brevo-unofficial` enabled.
- Installed plugin cache exists at the expected Brevo Helper version.
- Marketplace auth policy now uses install-time authentication setup.
- Guided onboarding verifier is available with `python3 scripts/brevo_onboarding_check.py`.
- CI-safe release preflight is available with `python3 scripts/release_preflight.py --skip-marketplace`.
- GitHub Actions validation workflow ran successfully after being added.
- Local marketplace source was added with `codex plugin marketplace add "/Users/danielheck/Documents/New project"`.
- GitHub marketplace source was added with `codex plugin marketplace add ogheck/brevo_unofficial_codex_plugin`.
- GitHub marketplace cache was refreshed with `codex plugin marketplace upgrade brevo-unofficial`; rerun before tagging so it matches the exact tagged commit.
- CLI smoke-test examples were added in `docs/cli-smoke-test-examples.md`.
- GitHub Actions validation has passed on the pushed `main` branch; confirm the latest run matches the exact tagged commit before tagging.
- Default MCP config excludes campaign management, SMS campaigns, WhatsApp campaigns, and webhook management.

## Blocked

- Fresh Codex app thread smoke test still needs to confirm bundled Brevo Helper skills and read-oriented MCP tools are visible to the model.

## Before Tagging

1. Set `BREVO_MCP_TOKEN` in the Codex runtime environment.
2. Restart Codex.
3. Open a fresh Codex app thread after installing Brevo Helper.
4. Verify the new `brevo-onboarding` skill loads in the fresh thread.
5. Run `python3 scripts/brevo_onboarding_check.py`.
6. Verify read-oriented Brevo MCP tools initialize.
7. Confirm Codex can inspect lists, templates, senders, domains, and analytics.
8. Confirm there is no direct send, schedule, launch, activation, or enrollment path.
9. Confirm the latest GitHub Actions validation run passed.
10. Move release notes from `Unreleased` into the tagged version section in `CHANGELOG.md`.
11. Tag `v0.1.1`.
