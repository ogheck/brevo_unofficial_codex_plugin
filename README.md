# Brevo Helper for Codex

Unofficial Codex plugin for planning Brevo campaigns and building website/backend integrations without sending from Codex.

This plugin is not made by, endorsed by, or supported by Brevo.

## What It Includes

- Focused Brevo MCP server configuration for contacts, lists, templates, analytics, senders, and domains.
- Codex skills for Brevo planning, website lead-capture integration, drip campaign building, and campaign QA.
- A hard no-send boundary: Codex drafts, configures, reviews, and builds backend code; the user sends, schedules, submits, or activates inside Brevo.

## Install

Add the GitHub-backed marketplace:

```bash
codex plugin marketplace add ogheck/brevo_unofficial_codex_plugin
```

Then open the Codex plugin directory, choose the "Brevo Unofficial" marketplace, and install "Brevo Helper".

For local development from this checkout:

```bash
codex plugin marketplace add "/Users/danielheck/Documents/New project"
```

Restart Codex after installing or changing the plugin.

## Quickstart

1. Add the marketplace:

   ```bash
   codex plugin marketplace add ogheck/brevo_unofficial_codex_plugin
   ```

2. Install "Brevo Helper" from the Codex plugin directory.

3. Set Brevo MCP auth for Codex:

   ```bash
   export BREVO_MCP_TOKEN="your-token"
   codex
   ```

   For the Codex desktop app on macOS:

   ```bash
   launchctl setenv BREVO_MCP_TOKEN "your-token"
   ```

4. Restart Codex after setting the token.

5. Start with one of these prompts:

   ```text
   Use Brevo Helper to connect this form to Brevo safely.
   ```

   ```text
   Build a Brevo drip campaign plan for this project.
   ```

   ```text
   Review this Brevo campaign before I send it.
   ```

Codex should prepare code, copy, QA, and dashboard handoff steps. The user performs final send, schedule, activation, and enrollment actions inside Brevo.

## Development Checks

Run before committing:

```bash
python3 scripts/validate_plugin.py
python3 scripts/check_markdown_links.py
python3 scripts/test_integration_generator.py
python3 scripts/test_examples.py
python3 scripts/release_preflight.py
```

If your system `node` is unavailable, provide `NODE_BIN`:

```bash
NODE_BIN="/path/to/node" python3 scripts/test_examples.py
```

Use strict live mode only after `BREVO_MCP_TOKEN` is set and the Codex app smoke test is ready:

```bash
python3 scripts/release_preflight.py --strict-live
```

For CI runners without a local Codex marketplace cache:

```bash
python3 scripts/release_preflight.py --skip-marketplace
```

## Generate An Integration Stub

List available backend runtimes:

```bash
python3 scripts/create_integration_stub.py --list
```

Create a starter endpoint from a template:

```bash
python3 scripts/create_integration_stub.py \
  --runtime nextjs-route-handler \
  --target ./brevo-lead-capture
```

The generator copies the selected example and adds `BREVO_INTEGRATION_NOTES.md` with required env vars and manual Brevo handoff reminders.

## Brevo Authentication

Generate a Brevo MCP token from your Brevo account:

1. Open Brevo.
2. Go to Account > SMTP & API > API Keys.
3. Generate an MCP server API key/token.
4. Store it as `BREVO_MCP_TOKEN` in the environment where Codex runs.

For Codex CLI:

```bash
export BREVO_MCP_TOKEN="your-token"
codex
```

For the Codex desktop app on macOS:

```bash
launchctl setenv BREVO_MCP_TOKEN "your-token"
```

Then fully restart the Codex app.

Do not commit Brevo tokens or API keys to this repository.

## Runtime App Secrets

For websites or apps that call Brevo directly, use a separate server-side runtime secret such as `BREVO_API_KEY`.

Keep Brevo API keys out of frontend JavaScript, static HTML, public environment variables, and `NEXT_PUBLIC_` variables.

Backend templates are available in:

- `examples/cloudflare-pages-function/`
- `examples/cloudflare-worker/`
- `examples/nextjs-route-handler/`
- `examples/express-endpoint/`
- `examples/static-html-plus-serverless/`

## No Direct Sending From Codex

This plugin is intentionally not a Brevo send operator.

Codex should not:

- Send email, SMS, or WhatsApp messages.
- Schedule or launch campaigns.
- Submit campaigns for delivery.
- Activate live drip automations.
- Enroll contacts in live automations.

Codex should:

- Build backend lead-capture endpoints.
- Draft marketing messages and drip sequences.
- Prepare Brevo dashboard setup instructions.
- QA campaign assets and tracking.
- Tell the user exactly what to click or confirm inside Brevo.

## Starter Prompts

- "Use Brevo Helper to connect this newsletter form to Brevo."
- "Audit this lead capture flow and confirm it writes to the right Brevo list."
- "Build a Brevo drip campaign plan for this project."
- "Draft the Brevo messages and dashboard setup checklist."

## Safety Defaults

The bundled skills prohibit direct sending from Codex. They require explicit confirmation before bulk importing or deleting contacts, or changing sender/domain/webhook configuration.

## Project Docs

- `docs/no-direct-send-policy.md`
- `docs/brevo-token-setup.md`
- `docs/backend-patterns.md`
- `docs/attribute-mapping.md`
- `docs/drip-campaign-workflow.md`
- `docs/drip-campaign-playbooks.md`
- `docs/campaign-qa-workflow.md`
- `docs/campaign-qa-scorecard.md`
- `docs/analytics-review-workflow.md`
- `docs/site-integration-workflow.md`
- `docs/project-integration-intake.md`
- `docs/mcp-vs-local-files.md`
- `docs/optional-webhook-management.md`
- `docs/project-integrations.md`
- `docs/testing.md`
- `docs/release-checklist.md`
- `docs/release-status.md`

## References

- Brevo MCP docs: https://developers.brevo.com/docs/mcp-protocol
- Brevo API docs: https://developers.brevo.com/docs/how-it-works
- Codex plugin docs: https://developers.openai.com/codex/plugins/build
