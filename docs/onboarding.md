# Brevo Helper Onboarding

Brevo Helper can guide setup and verify local configuration, but it does not collect, store, or publish Brevo credentials.

## What Install-Time Auth Means

The marketplace marks Brevo Helper authentication as install-time setup. This tells users to complete Brevo credential setup when installing the plugin.

It does not create a public account link and does not give other users access to your Brevo account.

Access still depends on credentials stored in the user's own environment:

- `BREVO_MCP_TOKEN` for Codex MCP access.
- `BREVO_API_KEY` for server-side application code only.

## Guided Setup

1. Install Brevo Helper from the "Brevo Unofficial" marketplace.
2. Open Brevo and generate a Brevo MCP token from the API/MCP token area.
3. Store the token as `BREVO_MCP_TOKEN` in the environment where Codex runs.
4. If the target website or app needs to create contacts, create a separate Brevo API key and store it as `BREVO_API_KEY` only in the server-side runtime.
5. Review sender identity, domain authentication, and any dedicated/sending IP or authorized-IP settings in Brevo.
6. Restart Codex after changing local environment variables.
7. Run the onboarding verifier:

   ```bash
   python3 scripts/brevo_onboarding_check.py
   ```

## macOS Codex App Environment

For the Codex desktop app on macOS:

```bash
launchctl setenv BREVO_MCP_TOKEN "your-token"
```

Then fully quit and restart Codex.

If your application backend also runs from a local process, set `BREVO_API_KEY` in that backend's environment. Do not put it in Codex plugin files unless it is a placeholder.

## CLI Environment

For Codex CLI:

```bash
export BREVO_MCP_TOKEN="your-token"
codex
```

For app backend development, keep `BREVO_API_KEY` in an ignored `.env` file or hosting secret manager.

## Verifier

Run:

```bash
python3 scripts/brevo_onboarding_check.py
```

The verifier checks:

- Marketplace auth policy is install-time.
- `BREVO_MCP_TOKEN` is present in the current process or macOS launch environment.
- `BREVO_API_KEY` is present when required.
- Bundled read-oriented MCP endpoints initialize when a token is available.
- No default send, schedule, SMS, WhatsApp, or webhook-management MCP endpoint is bundled.

The verifier does not print secrets.

To require the application API key check:

```bash
python3 scripts/brevo_onboarding_check.py --require-api-key
```

To skip the live MCP network smoke during documentation or CI checks:

```bash
python3 scripts/brevo_onboarding_check.py --skip-mcp-smoke
```

## Fresh Thread Smoke Prompt

After installing and restarting Codex, open a fresh thread and ask:

```text
Use Brevo Helper to verify my setup. Inspect lists, templates, senders, domains, and campaign analytics. Do not send, schedule, activate, or enroll anything.
```

Expected behavior:

- Codex uses Brevo Helper.
- Read-oriented Brevo MCP tools initialize.
- Codex can inspect setup without trying to send or activate live messaging.
- Any live Brevo action is left as a manual dashboard handoff step.
