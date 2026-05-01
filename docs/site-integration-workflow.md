# Site Integration Workflow

Use this workflow when Codex is connecting a website, landing page, app form, newsletter signup, or lead capture flow to Brevo.

Use the [project integration intake](project-integration-intake.md) before editing a real project.

## Discovery

Inspect the project first:

- Form markup and submit handlers.
- API routes, serverless functions, or backend endpoints.
- Hosting/runtime environment.
- Existing email, CRM, or analytics integrations.
- Environment variables.
- Client bundle exposure risk.

Use Brevo MCP read tools when available to inspect lists, attributes, templates, senders, domains, and relevant setup.

## Runtime Selection

Prefer the closest template:

- `examples/cloudflare-pages-function/`
- `examples/cloudflare-worker/`
- `examples/nextjs-route-handler/`
- `examples/express-endpoint/`
- `examples/static-html-plus-serverless/`

You can generate a starter copy with:

```bash
python3 scripts/create_integration_stub.py --runtime nextjs-route-handler --target ./brevo-lead-capture
```

## Implementation Rules

- Keep Brevo API calls server-side.
- Use `BREVO_API_KEY` only in the backend runtime.
- Use `BREVO_MCP_TOKEN` only for Codex MCP access.
- Validate and normalize user input.
- Map only known Brevo attributes.
- Use configured list IDs.
- Treat duplicates as expected.
- Return safe public errors.
- Avoid logging secrets or full personal-data payloads.

## Verification

Check:

- Invalid email is rejected before calling Brevo.
- Honeypot or spam controls work.
- Valid form submissions call the backend.
- Backend creates or updates the expected contact.
- Duplicate submissions do not fail the user flow.
- Brevo keys are not visible in browser files.

## Manual Brevo Handoff

List any dashboard work left for the user:

- Confirm list IDs and names.
- Confirm contact attributes exist.
- Confirm sender/domain setup.
- Create or review templates.
- Manually enable related automations after tests pass.
