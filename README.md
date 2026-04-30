# Brevo Helper for Codex

Unofficial Codex plugin for planning Brevo campaigns and building website/backend integrations without sending from Codex.

This plugin is not made by, endorsed by, or supported by Brevo.

## What It Includes

- Focused Brevo MCP server configuration for contacts, lists, templates, analytics, webhooks, senders, and domains.
- Codex skills for Brevo planning, website lead-capture integration, drip campaign building, and campaign QA.
- A hard no-send boundary: Codex drafts, configures, reviews, and builds backend code; the user sends, schedules, submits, or activates inside Brevo.

## Install

After this repository is pushed to GitHub:

```bash
codex plugin marketplace add ogheck/brevo_unofficial_codex_plugin
```

Then open the Codex plugin directory, choose the "Brevo Unofficial" marketplace, and install "Brevo Helper".

For local development from this checkout:

```bash
codex plugin marketplace add "/Users/danielheck/Documents/New project"
```

Restart Codex after installing or changing the plugin.

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
- `docs/drip-campaign-workflow.md`
- `docs/site-integration-workflow.md`
- `docs/testing.md`
- `docs/release-checklist.md`

## References

- Brevo MCP docs: https://developers.brevo.com/docs/mcp-protocol
- Brevo API docs: https://developers.brevo.com/docs/how-it-works
- Codex plugin docs: https://developers.openai.com/codex/plugins/build
