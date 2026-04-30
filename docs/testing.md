# Testing Brevo Helper

Use this guide before committing plugin changes or publishing a release.

## Static Validation

Run:

```bash
python3 scripts/validate_plugin.py
```

This checks:

- Plugin manifest JSON.
- Marketplace JSON.
- MCP server configuration.
- Required skill files and frontmatter.
- No direct campaign-management, SMS, or WhatsApp send-capable MCP endpoint is bundled by default.
- No obvious Brevo token has been committed.

## Example Endpoint Tests

For the Cloudflare Pages Function template:

```bash
cd examples/cloudflare-pages-function
npm test
```

This covers invalid email handling, honeypot behavior, contact creation payloads, and duplicate-contact updates.

## Local Marketplace Smoke Test

From this repository:

```bash
codex plugin marketplace add "/Users/danielheck/Documents/New project"
```

Restart Codex, open the plugin directory, choose the "Brevo Unofficial" marketplace, and install "Brevo Helper".

Expected result:

- The plugin appears as "Brevo Helper".
- The plugin shows read-oriented capabilities.
- The bundled skills are available in new Codex threads.

## GitHub Marketplace Smoke Test

After pushing to GitHub:

```bash
codex plugin marketplace add ogheck/brevo_unofficial_codex_plugin
```

Expected result:

- Codex discovers the marketplace.
- Brevo Helper can be installed from the GitHub-backed source.

## Brevo MCP Auth Smoke Test

Set `BREVO_MCP_TOKEN` in the environment where Codex runs.

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

Expected result:

- Brevo contact/list/template/sender/domain read tools initialize.
- Codex can inspect Brevo setup when asked.
- Codex does not expose a default send/schedule/launch path.

## No-Direct-Send Review

Before release, confirm:

- `.mcp.json` does not include `brevo_email_campaign_management`.
- `.mcp.json` does not include SMS or WhatsApp campaign servers.
- Skill files say Codex must not send, schedule, submit, activate, or enroll contacts in live automations.
- README tells users final send/schedule/activation happens in Brevo.
