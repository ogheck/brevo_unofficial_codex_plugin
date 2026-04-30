# Express Brevo Lead Capture Endpoint

This example shows a server-side Brevo lead-capture endpoint for an Express app.

The endpoint accepts browser form submissions, validates input, and creates or updates a Brevo contact with a server-side API key.

## Files

- `src/brevoLead.js`: Reusable Express handler factory.
- `src/server.js`: Minimal Express server wiring.
- `test/brevoLead.test.mjs`: Node test coverage for validation, honeypot, create, and duplicate-update behavior.

## Required Environment Variables

- `BREVO_API_KEY`: Server-side Brevo API key.
- `BREVO_LIST_IDS`: Comma-separated Brevo list IDs, for example `12,34`.

Optional:

- `ALLOWED_ORIGINS`: Comma-separated allowed origins for simple CORS handling.
- `PORT`: Server port. Defaults to `3000`.

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
- Make sure `express.json()` runs before the Brevo handler.
- Keep final campaign sending, scheduling, and automation activation inside Brevo.
- Add production-grade rate limiting before using on a public form.
