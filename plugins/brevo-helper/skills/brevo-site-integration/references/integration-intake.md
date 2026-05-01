# Brevo Site Integration Intake

Use this intake before editing a real project. Codex can build server-side form and event plumbing, but the user confirms live Brevo dashboard objects and activates any related automations manually.

## Project Facts

- Project name:
- Local path:
- Deployment target:
- Runtime or framework:
- Existing form files:
- Existing submit handler or route:
- Existing CRM/email/analytics integrations:
- Current environment variable pattern:

## Brevo Objects To Confirm

- Target list name and ID:
- Required contact attributes:
- Existing segments:
- Sender/domain dependencies:
- Templates involved:
- Automations that will consume the contact/list/attribute state:

If `BREVO_MCP_TOKEN` is unavailable, mark Brevo object IDs as manual dashboard confirmations instead of guessing.

## Security Review

Check for:

- Browser-visible Brevo keys.
- `NEXT_PUBLIC_` or equivalent public variables containing secrets.
- Static HTML that calls Brevo directly.
- Logs that include full form payloads or Brevo responses.
- Missing spam controls on public forms.
- Missing duplicate-contact handling.

## Runtime Selection

| Signal | Starter |
| --- | --- |
| Next.js App Router with `app/api` | `nextjs-route-handler` |
| Express or standalone Node server | `express-endpoint` |
| Cloudflare Pages with `functions/` | `cloudflare-pages-function` |
| Cloudflare Worker project | `cloudflare-worker` |
| Static site plus serverless API | `static-html-plus-serverless` |

## Verification Plan

Verify:

- Invalid email is rejected before Brevo is called.
- Honeypot, Turnstile, or rate-limit behavior works.
- Valid submission calls the server endpoint.
- Duplicate contact responses do not break the user flow.
- Contact attributes map to confirmed Brevo attributes.
- Brevo API key is not present in frontend files or build output.
- Required dashboard handoff steps are documented.
