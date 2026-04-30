# Backend Patterns For Brevo Integrations

Use backend endpoints for all project-to-Brevo writes. Do not call Brevo from browser-visible JavaScript with an API key.

## Required Runtime Secrets

Common environment variables:

- `BREVO_API_KEY`: Server-side Brevo API key for the application runtime.
- `BREVO_LIST_IDS`: Comma-separated Brevo list IDs for contact enrollment.
- `ALLOWED_ORIGINS`: Optional comma-separated list of allowed browser origins.

Do not use `BREVO_MCP_TOKEN` in application runtime code. That token is for Codex MCP access only.

## Request Flow

1. Browser submits form data to your backend endpoint.
2. Backend validates and normalizes fields.
3. Backend applies spam/rate-limit checks.
4. Backend creates or updates the Brevo contact.
5. Backend returns a generic success/failure response.
6. User manages any live campaign or automation activation manually in Brevo.

## Contact Handling

Recommended behavior:

- Treat duplicate contacts as expected.
- Create contact when missing.
- Update contact when existing.
- Keep list IDs in environment variables.
- Map only known contact attributes.
- Avoid logging full request bodies with personal data.

Brevo API references:

- Create contact: https://developers.brevo.com/reference/create-contact
- Update contact: https://developers.brevo.com/reference/updatecontact

## Public Response Handling

Return safe messages:

- `200`: accepted or subscribed.
- `400`: invalid form input.
- `405`: method not allowed.
- `429`: rate limited.
- `500`: generic service error.

Do not return raw Brevo errors to the browser.

## Example Runtimes

Current templates:

- `examples/cloudflare-pages-function/`
- `examples/cloudflare-worker/`
- `examples/nextjs-route-handler/`
- `examples/express-endpoint/`
- `examples/static-html-plus-serverless/`

Each template follows the same core contract: browser-visible code posts form JSON to a backend endpoint, and only backend code calls Brevo with `BREVO_API_KEY`.
