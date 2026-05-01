---
name: brevo-onboarding
description: Use when setting up, installing, authenticating, or verifying Brevo Helper for Codex, including Brevo MCP token setup, server-side Brevo API key setup, sender/domain authentication, IP-related Brevo setup checks, and local onboarding smoke tests.
---

# Brevo Helper Onboarding

Use this skill when the user wants to install, authenticate, link, verify, or troubleshoot Brevo Helper setup.

This plugin is unofficial. Do not imply that Codex can complete a Brevo account-linking flow as Brevo, and do not ask the user to paste secrets into chat.

## Setup Boundary

Codex can guide setup, inspect local environment state, and run local smoke tests.

Codex must not:

- Store Brevo tokens in the repository.
- Ask the user to paste `BREVO_MCP_TOKEN` or `BREVO_API_KEY` into chat.
- Put Brevo secrets in frontend code, public env vars, logs, or committed files.
- Send, schedule, launch, activate, or enroll anything in Brevo.

If browser control is used to create API keys or persistent access, stop before the final creation step and ask the user to complete it.

## Onboarding Workflow

1. Read `references/onboarding-checklist.md` when the user needs setup steps or verification criteria.
2. Confirm whether the user is setting up Codex MCP access, application backend API access, or both.
3. Direct the user to Brevo dashboard setup pages for token/key creation and sender/domain/IP review.
4. Tell the user how to store secrets locally:
   - `BREVO_MCP_TOKEN` for Codex MCP access.
   - `BREVO_API_KEY` only for server-side application runtimes.
5. Run `python3 scripts/brevo_onboarding_check.py` from the plugin repo when local verification is useful.
6. If `BREVO_MCP_TOKEN` is set, run `python3 scripts/smoke_brevo_mcp.py` or let the onboarding check run it.
7. Report what is ready, what is missing, and what the user must finish manually in Brevo.

## Output Format

Return:

- `Ready`: checks that passed.
- `Missing`: local env vars, app install state, sender/domain/IP checks, or docs still needed.
- `Manual Brevo Steps`: dashboard actions the user must perform.
- `Security Notes`: how secrets are being kept out of code and chat.
