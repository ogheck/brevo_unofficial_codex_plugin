# Form Schema Examples

These schemas describe public form payloads before a server-side endpoint maps them to Brevo contacts.

## Files

- `lead-capture.schema.json`: Common lead-capture payload used by the backend templates.

## Mapping Notes

Suggested Brevo contact attributes:

- `firstName` -> `FIRSTNAME`
- `lastName` -> `LASTNAME`
- `phone` -> `SMS`
- `source` -> `SOURCE`
- `message` -> `MESSAGE`

Confirm attributes exist in Brevo before using them in production.

Do not put `BREVO_API_KEY` or `BREVO_MCP_TOKEN` in browser-visible form code.
