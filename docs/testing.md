# Testing Brevo Helper

Use this guide before committing plugin changes or publishing a release.

## Static Validation

Run:

```bash
python3 scripts/validate_plugin.py
python3 scripts/check_markdown_links.py
```

The plugin validator checks:

- Plugin manifest JSON.
- Marketplace JSON.
- MCP server configuration.
- Required skill files and frontmatter.
- No direct campaign-management, SMS, or WhatsApp send-capable MCP endpoint is bundled by default.
- No obvious Brevo token has been committed.

The markdown link checker verifies local Markdown links point at files inside this repository.

For install-time setup verification, run:

```bash
python3 scripts/brevo_onboarding_check.py --skip-mcp-smoke
```

Run it without `--skip-mcp-smoke` after `BREVO_MCP_TOKEN` is set.

## Integration Generator Tests

Run:

```bash
python3 scripts/test_integration_generator.py
```

This verifies the backend stub generator lists runtimes, copies templates, refuses accidental overwrites, and supports dry runs.

## Example Endpoint Tests

Run every example suite:

```bash
python3 scripts/test_examples.py
```

If your system `node` is not usable, set `NODE_BIN`:

```bash
NODE_BIN="/path/to/node" python3 scripts/test_examples.py
```

Or run individual example suites:

```bash
cd examples/cloudflare-pages-function
npm test

cd ../cloudflare-worker
npm test

cd ../nextjs-route-handler
npm test

cd ../express-endpoint
npm test

cd ../static-html-plus-serverless
npm test
```

These cover invalid email handling, honeypot behavior, CORS where applicable, contact creation payloads, and duplicate-contact updates.

## Release Preflight

Run:

```bash
python3 scripts/release_preflight.py
```

This runs plugin validation, Markdown link validation, all backend example tests, checks whether the git worktree is clean, and checks whether the local GitHub marketplace cache matches the current repo revision.

To include the local Codex app marketplace/plugin install-state diagnostic:

```bash
python3 scripts/release_preflight.py --check-codex-app
```

On CI runners that do not have a local Codex marketplace cache, use:

```bash
python3 scripts/release_preflight.py --skip-marketplace
```

After `BREVO_MCP_TOKEN` is set and live smoke testing is ready, run:

```bash
python3 scripts/release_preflight.py --strict-live
```

Strict live mode also runs the bundled Brevo MCP initialize smoke test:

```bash
python3 scripts/smoke_brevo_mcp.py
```

This checks each bundled read-oriented MCP endpoint and does not print the token.

For the guided install-time setup check, run:

```bash
python3 scripts/brevo_onboarding_check.py
```

## GitHub Actions

The repository includes `.github/workflows/validate.yml`.

It runs:

- Plugin package validation.
- Markdown link validation.
- Integration generator tests.
- Backend example tests.
- Release preflight with the marketplace cache check skipped.

## Local Marketplace Smoke Test

From this repository:

```bash
codex plugin marketplace add "/Users/danielheck/Documents/New project"
```

Restart Codex, open the plugin directory, choose the "Brevo Unofficial" marketplace, and install "Brevo Helper".

Expected result:

- The plugin appears as "Brevo Helper".
- The plugin prompts for install-time authentication setup.
- The plugin shows read-oriented capabilities.
- The bundled skills are available in new Codex threads.

After installing, run:

```bash
python3 scripts/check_codex_plugin_state.py
```

Expected result:

- The `brevo-unofficial` marketplace is registered.
- The marketplace cache revision matches this checkout.
- The `brevo-helper@brevo-unofficial` plugin is enabled in Codex config.
- An installed Brevo Helper plugin copy exists under the Codex plugin cache.

See [CLI smoke test examples](cli-smoke-test-examples.md) for verified marketplace refresh and preflight output.

## GitHub Marketplace Smoke Test

After pushing to GitHub:

```bash
codex plugin marketplace add ogheck/brevo_unofficial_codex_plugin
```

Expected result:

- Codex discovers the marketplace.
- Brevo Helper can be installed from the GitHub-backed source.

## Brevo MCP Auth Smoke Test

Set `BREVO_MCP_TOKEN` in the environment where Codex runs.

For Codex CLI:

```bash
export BREVO_MCP_TOKEN="your-token"
codex
```

For Codex app on macOS:

```bash
launchctl setenv BREVO_MCP_TOKEN "your-token"
```

Restart the Codex app after setting the variable.

Expected result:

- Brevo contact/list/template/sender/domain read tools initialize.
- Codex can inspect Brevo setup when asked.
- Codex does not expose a default send/schedule/launch path.

For a command-line initialize check:

```bash
python3 scripts/smoke_brevo_mcp.py
```

For a broader onboarding check:

```bash
python3 scripts/brevo_onboarding_check.py
```

Add `--require-api-key` when the target app integration needs server-side `BREVO_API_KEY`.

## No-Direct-Send Review

Before release, confirm:

- `.mcp.json` does not include `brevo_email_campaign_management`.
- `.mcp.json` does not include SMS or WhatsApp campaign servers.
- `.mcp.json` does not include `brevo_webhooks_management` by default.
- Skill files say Codex must not send, schedule, submit, activate, or enroll contacts in live automations.
- README tells users final send/schedule/activation happens in Brevo.
