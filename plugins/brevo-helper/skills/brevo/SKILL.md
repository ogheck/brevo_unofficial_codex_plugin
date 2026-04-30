---
name: brevo
description: Use Brevo from Codex through the unofficial Brevo Helper plugin. Trigger for Brevo, Sendinblue, contacts, lists, templates, campaigns, transactional email, sender domains, analytics, webhooks, and CRM/email-marketing tasks.
---

# Brevo Helper

Use this skill when the user wants Codex to work with Brevo or connect a project to Brevo.

This plugin is unofficial. Do not imply that it is made by, endorsed by, or supported by Brevo.

## Access Model

- Prefer the bundled Brevo MCP servers before writing custom API calls.
- Expect Brevo auth to come from `BREVO_MCP_TOKEN`; never ask the user to paste a token into chat.
- If tools are unavailable or auth fails, tell the user to generate a Brevo MCP token in Brevo and expose it to Codex as `BREVO_MCP_TOKEN`.
- If MCP coverage is not enough, use Brevo's public API only with server-side secrets such as `BREVO_API_KEY`.

## Safety Rules

Start read-only. Inspect account state, lists, attributes, templates, campaign drafts, sender status, and webhook configuration before making changes.

Require explicit user confirmation before:

- Sending any email, SMS, or WhatsApp message.
- Scheduling, launching, or resending a campaign.
- Bulk importing or deleting contacts.
- Deleting lists, templates, senders, domains, or webhooks.
- Changing sender/domain authentication settings.
- Updating active automations or production webhook destinations.

For risky writes, summarize the exact action, target IDs or names, expected blast radius, and rollback path before proceeding.

## Default Workflow

1. Identify whether the task is account ops, website integration, campaign QA, or debugging.
2. Gather current state through Brevo MCP and local project files.
3. Keep credentials server-side; never add Brevo keys to browser-visible code or `NEXT_PUBLIC_` variables.
4. Make the smallest practical change.
5. Verify with local tests, route checks, and Brevo readback where possible.
6. Report what changed, what was verified, and any action that still needs Brevo dashboard confirmation.

## Common Outputs

For audits, return:

- Current Brevo objects involved.
- Local project files involved.
- Risks or missing setup.
- Specific next edits or actions.

For implementations, return:

- Changed files.
- Required environment variables.
- Brevo list/template/webhook IDs used.
- Verification steps completed.
