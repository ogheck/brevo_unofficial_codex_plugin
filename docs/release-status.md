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
- Onboarding verifier now runs MCP `tools/list` to fail fast on Brevo Authorized IP blockers.
- Fresh Codex app thread smoke test loaded Brevo Helper and reached Brevo MCP without attempting send, schedule, activation, or enrollment.
- CI-safe release preflight is available with `python3 scripts/release_preflight.py --skip-marketplace`.
- GitHub Actions validation workflow ran successfully after being added.
- Local marketplace source was added from a checkout with `codex plugin marketplace add "/path/to/brevo_unofficial_codex_plugin"`.
- GitHub marketplace source was added with `codex plugin marketplace add ogheck/brevo_unofficial_codex_plugin`.
- GitHub marketplace cache was refreshed with `codex plugin marketplace upgrade brevo-unofficial`; rerun before tagging so it matches the exact tagged commit.
- CLI smoke-test examples were added in `docs/cli-smoke-test-examples.md`.
- GitHub Actions validation has passed on the pushed `main` branch; confirm the latest run matches the exact tagged commit before tagging.
- Default MCP config excludes campaign management, SMS campaigns, WhatsApp campaigns, and webhook management.

## Blocked

- Brevo rejected the fresh-thread read-only tools/list request because the Codex runtime IP is not authorized in Brevo.
- Run `python3 scripts/brevo_onboarding_check.py --warn-only` and add the IP it reports to Brevo Authorized IPs.

## Before Tagging

1. Set `BREVO_MCP_TOKEN` in the Codex runtime environment.
2. Restart Codex.
3. Run `python3 scripts/brevo_onboarding_check.py --warn-only` and add its reported IP to Brevo Authorized IPs.
4. Open a fresh Codex app thread after installing Brevo Helper.
5. Verify the new `brevo-onboarding` skill loads in the fresh thread.
6. Run `python3 scripts/brevo_onboarding_check.py`.
7. Verify read-oriented Brevo MCP tools initialize.
8. Confirm Codex can inspect lists, templates, senders, domains, and analytics.
9. Confirm there is no direct send, schedule, launch, activation, or enrollment path.
10. Confirm the latest GitHub Actions validation run passed.
11. Move release notes from `Unreleased` into the tagged version section in `CHANGELOG.md`.
12. Tag `v0.1.1`.
