# CLI Smoke Test Examples

These examples show the verified command-line checks for the Brevo Helper marketplace source and plugin package.

The Codex CLI can add or refresh marketplace sources. The final plugin install/load check still happens in the Codex app plugin UI.

## Marketplace Commands

Add the GitHub-backed marketplace:

```bash
codex plugin marketplace add ogheck/brevo_unofficial_codex_plugin
```

Add this local checkout as a development marketplace:

```bash
codex plugin marketplace add "/path/to/brevo_unofficial_codex_plugin"
```

Refresh the GitHub-backed marketplace cache:

```bash
codex plugin marketplace upgrade brevo-unofficial
```

Expected output:

```text
Upgraded marketplace `brevo-unofficial` to the latest configured revision.
Installed marketplace root: <codex-home>/.tmp/marketplaces/brevo-unofficial
```

## Static Release Preflight

Run:

```bash
python3 scripts/release_preflight.py
```

Example verified result:

```text
Brevo Helper plugin validation passed.
Markdown link check passed.
Ran 4 tests in 0.004s
All example tests passed.
ok: working tree is clean
ok: marketplace cache revision matches local revision <current-commit>
ok: plugin manifest version is 0.1.1
Static preflight passed. Release remains blocked on live smoke tests.
```

The live blocker is expected until `BREVO_MCP_TOKEN` is set and the Codex app plugin install/load smoke test has been completed.

## GitHub Actions

The pushed `main` branch runs `.github/workflows/validate.yml`.

Example verified run:

- Workflow: Validate.
- Conclusion: success.
- URL: https://github.com/ogheck/brevo_unofficial_codex_plugin/actions

## Manual App UI Check

After adding the marketplace, use the Codex app plugin UI to:

1. Choose the "Brevo Unofficial" marketplace.
2. Install "Brevo Helper".
3. Restart Codex.
4. Open a new thread and confirm the bundled Brevo skills are available.
5. Set `BREVO_MCP_TOKEN` and confirm the read-oriented MCP tools initialize.

Do not tag `v0.1.1` until the app UI and Brevo MCP auth checks pass.
