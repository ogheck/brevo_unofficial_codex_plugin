# Static HTML Plus Serverless Brevo Lead Capture

This example shows a plain HTML form that submits to a small serverless endpoint.

Use this pattern when the public site is mostly static and you only need a backend function to protect the Brevo API key.

## Files

- `public/index.html`: Plain form with a hidden honeypot field.
- `public/main.js`: Browser JavaScript that submits JSON to `/api/brevo-lead`.
- `api/brevo-lead.mjs`: Framework-neutral Fetch-style serverless handler.
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
  "phone": "+15555555555",
  "source": "static-html-form",
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

## Adapter Notes

The endpoint exports `handleBrevoLeadRequest(request, env)`. Wrap that function with the adapter your host expects:

- Cloudflare Pages Functions can call it from `onRequestPost`.
- Vercel functions can pass a Web `Request` to it in App Router style.
- Netlify Edge Functions can return its `Response` directly.

## Notes

- Do not place `BREVO_API_KEY` in `public/main.js` or any other browser file.
- Keep final campaign sending, scheduling, and automation activation inside Brevo.
- Add production-grade spam control before using on a high-traffic public form.
