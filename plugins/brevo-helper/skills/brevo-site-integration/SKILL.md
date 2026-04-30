---
name: brevo-site-integration
description: Connect websites, landing pages, forms, lead capture, newsletters, careers flows, or contact forms to Brevo safely from Codex.
---

# Brevo Site Integration

Use this skill when connecting a site or app to Brevo, especially forms that create contacts, add contacts to lists, trigger transactional email, or fire webhooks/events.

## First Pass

Inspect the project before changing code:

- Find forms, submit handlers, API routes, serverless functions, and existing email/CRM providers.
- Identify frontend-visible environment variables and confirm Brevo secrets are not exposed to the browser.
- Determine the hosting/runtime pattern: Cloudflare Pages Functions, Workers, Vercel, Next.js API routes, Express, static HTML, or another backend.
- Use Brevo MCP to inspect the relevant lists, attributes, templates, senders, and domains.

## Implementation Rules

- Put Brevo API calls behind a server-side endpoint.
- Use `BREVO_API_KEY` only on the server if direct API calls are needed.
- Use `BREVO_MCP_TOKEN` only for Codex MCP access, not application runtime code.
- Validate and normalize form input before sending it to Brevo.
- Map fields intentionally to Brevo contact attributes; do not invent attributes without checking existing account state.
- Use list IDs from Brevo readback, not hardcoded guesses.
- Handle duplicate contacts as a normal outcome.
- Return user-safe errors from public endpoints; do not leak Brevo API errors or secrets.
- Add spam controls where appropriate, such as honeypot fields, rate limits, or Turnstile.

## Runtime Patterns

Prefer the repo examples when they fit the target project:

- `examples/cloudflare-pages-function/`
- `examples/cloudflare-worker/`
- `examples/nextjs-route-handler/`
- `examples/express-endpoint/`
- `examples/static-html-plus-serverless/`

Use `examples/form-schema/lead-capture.schema.json` as a starting point for public lead-capture payloads.

Use `docs/attribute-mapping.md` when mapping local fields to Brevo contact attributes.

## MCP Versus Local Files

Use local files to locate form and backend code. Use Brevo MCP to confirm list IDs, attributes, templates, sender state, and domain state. If MCP is unavailable, use placeholder list names and tell the user which Brevo dashboard values must be confirmed manually.

## Prompt Examples

Handle prompts like:

- "Connect this form to Brevo safely."
- "Add a backend endpoint that creates Brevo contacts."
- "Wire newsletter signups to a Brevo list."
- "Audit this app for browser-exposed Brevo secrets."

## Verification Checklist

When possible, verify:

- The form submits successfully in local or staging.
- The server endpoint rejects malformed input.
- No Brevo key appears in client bundles, static HTML, logs, or committed files.
- The expected contact appears in the expected Brevo list.
- Expected attributes are populated.
- Duplicate submissions do not break the flow.
- User-facing success and error states are clear.

## Output Structure

When done, include:

- The form or route connected.
- Brevo list/template IDs used.
- Environment variables required.
- Verification performed.
- Any Brevo dashboard setup still needed, such as sender/domain authentication.

End with a "Manual Brevo Handoff" section for list, attribute, sender, domain, template, or automation steps the user must complete inside Brevo.
