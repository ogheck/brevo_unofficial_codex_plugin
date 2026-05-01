# Brevo Helper Onboarding Checklist

Use this checklist when helping a user install, authenticate, or verify Brevo Helper.

## Codex MCP Access

- Open Brevo in the user's browser.
- Go to the Brevo API/MCP token area, usually under account settings for SMTP/API keys.
- Have the user generate a Brevo MCP token.
- Store the token as `BREVO_MCP_TOKEN` in the environment where Codex runs.
- Restart Codex after setting the token.
- Run `python3 scripts/brevo_onboarding_check.py`.

Do not ask the user to paste the token into chat.

## Application Backend API Access

- Use `BREVO_API_KEY` only in the target app's server-side runtime.
- Store it in the hosting provider's secret manager or an ignored local `.env` file.
- Never use it in static HTML, browser JavaScript, public logs, or `NEXT_PUBLIC_*` variables.
- Confirm the target backend can create or update contacts only after the user approves the intended list and attributes.

## Sender, Domain, And IP Review

Ask the user to verify these in Brevo:

- Sender identity is approved and recognizable.
- Domain authentication records are complete.
- Dedicated/sending IP setup is correct if the account uses dedicated IPs.
- Authorized IP restrictions are compatible with the deployment platform if the account uses IP allowlisting.
- Bounce, unsubscribe, tracking, and compliance settings match the campaign plan.

Codex may inspect sender and domain state through read-oriented MCP tools, but the user performs final dashboard changes.

## Verification Prompts

Use these prompts in a fresh Codex thread after install:

```text
Use Brevo Helper to verify my setup. Do not send, schedule, activate, or enroll anything.
```

```text
Use Brevo Helper to inspect my Brevo lists, templates, senders, domains, and campaign analytics.
```

Expected behavior:

- Brevo Helper skills are available.
- Read-oriented Brevo MCP tools initialize.
- Codex can summarize lists, templates, senders, domains, and analytics without attempting live send actions.
- Codex ends with manual Brevo dashboard handoff steps for anything live.
