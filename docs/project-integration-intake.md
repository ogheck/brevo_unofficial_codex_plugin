# Project Integration Intake

Use this intake before connecting a real website, app, landing page, or form to Brevo.

Codex can inspect local project files and build server-side integration code. The user confirms live Brevo list IDs, attributes, sender/domain setup, and automation activation inside Brevo.

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

If `BREVO_MCP_TOKEN` is unavailable, do not guess Brevo IDs. Mark them as dashboard confirmations.

## Runtime Selection

| Target project signal | Preferred starter |
| --- | --- |
| Next.js App Router with `app/api` | `nextjs-route-handler` |
| Express or standalone Node server | `express-endpoint` |
| Cloudflare Pages with `functions/` | `cloudflare-pages-function` |
| Cloudflare Worker project | `cloudflare-worker` |
| Static site that can call a serverless API | `static-html-plus-serverless` |

## Security Review

Check for:

- Browser-visible Brevo keys.
- `NEXT_PUBLIC_` or equivalent public variables containing secrets.
- Static HTML that calls Brevo directly.
- Logs that include full form payloads or Brevo responses.
- Missing spam controls on public forms.
- Missing duplicate-contact handling.

## Verification Plan

Verify:

- Invalid email is rejected before Brevo is called.
- Honeypot, Turnstile, or rate-limit behavior works.
- Valid submission calls the server endpoint.
- Duplicate contact responses do not break the user flow.
- Contact attributes map to confirmed Brevo attributes.
- Brevo API key is not present in frontend files or build output.
- Required dashboard handoff steps are documented.
