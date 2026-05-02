# Contributing

Thanks for improving Brevo Helper. This repository is public and handles marketing/email workflow code, so keep changes conservative and auditable.

## Safety Boundary

The default plugin must not send, schedule, launch, activate, or enroll anything from Codex.

Do not add default MCP servers, skills, scripts, or examples that let Codex:

- Send email, SMS, or WhatsApp messages.
- Schedule or launch Brevo campaigns.
- Submit campaigns for delivery.
- Activate live automations.
- Enroll contacts in live automations.

If a future private variant needs higher-permission Brevo operations, keep it separate from the public/default plugin and document the risk clearly.

## Secrets

Never commit Brevo API keys, MCP tokens, exported environment files, private customer data, or production contact lists.

Use placeholders such as:

```bash
BREVO_MCP_TOKEN="your-token"
BREVO_API_KEY="your-server-side-api-key"
```

Keep `BREVO_MCP_TOKEN` for Codex MCP access only. Use `BREVO_API_KEY` only in server-side application runtimes.

## Local Paths

Public docs should use generic paths such as:

```bash
codex plugin marketplace add "/path/to/brevo_unofficial_codex_plugin"
```

Do not commit machine-specific paths, local usernames, or local Codex cache paths unless they are intentionally anonymized examples.

## Checks

Run these before opening a pull request:

```bash
python3 scripts/validate_plugin.py
python3 scripts/check_markdown_links.py
python3 scripts/test_integration_generator.py
python3 scripts/test_examples.py
python3 scripts/release_preflight.py --skip-marketplace
```

Use live Brevo checks only when you have a local token configured and understand that Brevo Authorized IP settings may block the request:

```bash
python3 scripts/brevo_onboarding_check.py
```

