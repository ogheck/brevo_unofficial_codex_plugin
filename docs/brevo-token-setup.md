# Brevo Token Setup

Brevo Helper uses two separate kinds of credentials.

## Codex MCP Token

Use `BREVO_MCP_TOKEN` only for Codex MCP access.

This token lets Codex inspect supported Brevo objects through bundled MCP servers, such as contacts, lists, templates, analytics, senders, and domains.

Do not place `BREVO_MCP_TOKEN` in application code.

For Codex CLI:

```bash
export BREVO_MCP_TOKEN="your-token"
codex
```

For Codex app on macOS:

```bash
launchctl setenv BREVO_MCP_TOKEN "your-token"
```

Restart the Codex app after setting the variable.

## Application API Key

Use `BREVO_API_KEY` only in server-side application runtimes.

Examples:

- Cloudflare Worker secret.
- Cloudflare Pages environment variable.
- Vercel server-side environment variable.
- Render or other backend service secret.
- Local `.env` file that is ignored by git.

Never expose the Brevo API key in:

- Static HTML.
- Browser JavaScript.
- `NEXT_PUBLIC_*` variables.
- Public logs.
- Git commits.
- Chat messages.

## Separation Rule

`BREVO_MCP_TOKEN` is for Codex to inspect Brevo.

`BREVO_API_KEY` is for your application backend to create or update contacts.

Neither credential should be used for sending, scheduling, launching, or activating Brevo campaigns from Codex.
