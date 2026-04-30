# Brevo Helper for Codex

Unofficial Codex plugin for working with Brevo through Brevo MCP and website integration workflows.

This plugin is not made by, endorsed by, or supported by Brevo.

## What It Includes

- Focused Brevo MCP server configuration for contacts, lists, templates, campaigns, analytics, webhooks, senders, and domains.
- Codex skills for safe Brevo operations, website lead-capture integration, and campaign QA.
- Read-first safety rules for campaign sends, bulk imports, deletes, and production configuration changes.

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

## Starter Prompts

- "Use Brevo Helper to connect this newsletter form to Brevo."
- "Audit this lead capture flow and confirm it writes to the right Brevo list."
- "Review this Brevo campaign draft before I send it."

## Safety Defaults

The bundled skills require explicit confirmation before sending messages, launching campaigns, bulk importing or deleting contacts, or changing sender/domain/webhook configuration.

## References

- Brevo MCP docs: https://developers.brevo.com/docs/mcp-protocol
- Brevo API docs: https://developers.brevo.com/docs/how-it-works
- Codex plugin docs: https://developers.openai.com/codex/plugins/build
