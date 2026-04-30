# Cloudflare Pages Function Brevo Lead Capture

This example shows a server-side lead-capture endpoint for Cloudflare Pages Functions.

It accepts browser form submissions, validates input, and creates or updates a Brevo contact with a server-side API key.

## Files

- `functions/api/brevo-lead.js`: Pages Function endpoint.
- `test/brevo-lead.test.mjs`: Node test coverage for validation, honeypot, create, and duplicate-update behavior.

## Required Environment Variables

- `BREVO_API_KEY`: Server-side Brevo API key.
- `BREVO_LIST_IDS`: Comma-separated Brevo list IDs, for example `12,34`.

Optional:

- `ALLOWED_ORIGINS`: Comma-separated allowed origins for CORS.

## Request

`POST /api/brevo-lead`

```json
{
  "email": "customer@example.com",
  "firstName": "Jane",
  "lastName": "Customer",
  "phone": "555-555-5555",
  "source": "website-form",
  "message": "I want more information",
  "company": ""
}
```

`company` is a honeypot field. Real users should leave it blank.

## Response

Success:

```json
{
  "ok": true
}
```

Validation failure:

```json
{
  "ok": false,
  "message": "Enter a valid email address."
}
```

## Notes

- Do not expose `BREVO_API_KEY` to browser JavaScript.
- Keep final campaign sending, scheduling, and automation activation inside Brevo.
- Add stronger rate limiting or Turnstile before using on a high-traffic public form.

## Tests

Run from this example directory:

```bash
npm test
```
