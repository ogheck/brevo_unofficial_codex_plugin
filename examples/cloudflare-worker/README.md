# Cloudflare Worker Brevo Lead Capture

This example shows a server-side Brevo lead-capture endpoint for a standalone Cloudflare Worker.

The Worker accepts browser form submissions, validates input, and creates or updates a Brevo contact with a server-side API key.

## Files

- `src/index.js`: Worker entrypoint.
- `test/index.test.mjs`: Node test coverage for validation, CORS, create, and duplicate-update behavior.

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
  "phone": "+15555555555",
  "source": "website-form",
  "message": "I want more information",
  "company": ""
}
```

`company` is a honeypot field. Real users should leave it blank.

## Tests

Run from this example directory:

```bash
npm test
```

## Notes

- Do not expose `BREVO_API_KEY` to browser JavaScript.
- Use a server-side Worker secret for the Brevo API key.
- Keep final campaign sending, scheduling, and automation activation inside Brevo.
- Add Turnstile or rate limiting before using on a high-traffic public form.
