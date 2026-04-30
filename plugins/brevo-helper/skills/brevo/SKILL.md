---
name: brevo
description: Use Brevo from Codex through the unofficial Brevo Helper plugin. Trigger for Brevo, Sendinblue, contacts, lists, templates, drip campaigns, marketing copy, transactional email planning, sender domains, analytics, webhooks, and CRM/email-marketing integration tasks.
---

# Brevo Helper

Use this skill when the user wants Codex to work with Brevo or connect a project to Brevo.

This plugin is unofficial. Do not imply that it is made by, endorsed by, or supported by Brevo.

## Access Model

- Prefer the bundled Brevo MCP servers before writing custom API calls.
- Expect Brevo auth to come from `BREVO_MCP_TOKEN`; never ask the user to paste a token into chat.
- If tools are unavailable or auth fails, tell the user to generate a Brevo MCP token in Brevo and expose it to Codex as `BREVO_MCP_TOKEN`.
- If MCP coverage is not enough, use Brevo's public API only with server-side secrets such as `BREVO_API_KEY`.
- Webhook management is intentionally not bundled by default. Plan webhook needs and provide Brevo dashboard handoff steps unless the user explicitly installs an advanced webhook-management setup.

## Hard Boundary: No Direct Sending

Do not send, schedule, launch, resend, or submit any Brevo campaign or message from Codex.

Do not use MCP or API tools for:

- Sending any email, SMS, or WhatsApp message.
- Scheduling, launching, or resending a campaign.
- Submitting a campaign for delivery.
- Triggering a live automation/drip enrollment.

The intended handoff is: Codex drafts the strategy, content, backend code, QA checklist, and Brevo dashboard instructions; the user performs final submit/send/schedule actions inside Brevo.

## Safety Rules

Start read-only. Inspect account state, lists, attributes, templates, sender status, and analytics before making changes.

Require explicit user confirmation before:

- Bulk importing or deleting contacts.
- Deleting lists, templates, senders, domains, or webhooks.
- Changing sender/domain authentication settings.
- Updating active automations or production webhook destinations.

For risky non-send writes, summarize the exact action, target IDs or names, expected blast radius, and rollback path before proceeding.

## Default Workflow

1. Identify whether the task is account ops, website integration, drip/campaign planning, campaign QA, or debugging.
2. Gather current state through Brevo MCP and local project files.
3. Keep credentials server-side; never add Brevo keys to browser-visible code or `NEXT_PUBLIC_` variables.
4. Make the smallest practical change.
5. Verify with local tests, route checks, and Brevo readback where possible.
6. Report what changed, what was verified, and the exact Brevo dashboard actions the user must perform manually.

## Routing Examples

Use `brevo-site-integration` for prompts like:

- "Connect this contact form to Brevo."
- "Add newsletter signups to my Brevo list."
- "Build the backend for Brevo lead capture."

Use `brevo-drip-builder` for prompts like:

- "Build a welcome sequence in Brevo."
- "Draft a 5-email nurture campaign."
- "Plan a winback drip campaign."

Use `brevo-campaign-qa` for prompts like:

- "Review this Brevo campaign before I send it."
- "Check this template for missing variables."
- "QA my sender/domain setup."

## MCP Versus Local Files

Use Brevo MCP for Brevo account objects: lists, attributes, templates, analytics, senders, and domains.

Use local project files for application behavior: forms, submit handlers, API routes, serverless functions, environment variables, and tests.

For website integrations, use both: local files determine where code changes belong, and Brevo MCP determines which Brevo objects the code should target.

## Common Outputs

For audits, return:

- Current Brevo objects involved.
- Local project files involved.
- Risks or missing setup.
- Specific next edits or actions.

For implementations, return:

- Changed files.
- Required environment variables.
- Brevo list/template IDs used.
- Any webhook IDs or destinations that must be reviewed manually in Brevo.
- Verification steps completed.
- Manual Brevo dashboard handoff steps.

Always include a short "Manual Brevo Handoff" section when the next step involves a live Brevo action.
