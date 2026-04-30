# No-Direct-Send Policy

Brevo Helper is designed for preparation, review, implementation, and manual Brevo dashboard handoff.

Codex must not use this plugin to send, schedule, launch, resend, submit, activate, or enroll contacts into live Brevo messaging flows.

## Allowed Work

Codex may:

- Plan drip campaigns and lifecycle sequences.
- Draft marketing messages and Brevo-ready template copy.
- Review campaigns, templates, senders, domains, analytics, webhooks, lists, and attributes.
- Build backend code that creates or updates contacts from project forms or events.
- Produce manual Brevo dashboard instructions.

## Disallowed Work

Codex must not:

- Send email, SMS, or WhatsApp messages.
- Schedule or launch campaigns.
- Submit campaign drafts for delivery.
- Activate live automations.
- Enroll contacts into live automations.
- Use a broad write-capable Brevo MCP server by default.

## Risky Non-Send Writes

Some Brevo operations are not message sends but can still affect production systems. Before those actions, Codex should ask for explicit confirmation and summarize:

- The exact action.
- The Brevo object IDs or names involved.
- Expected blast radius.
- Rollback or recovery path.

Examples include deleting lists, changing webhook destinations, changing sender/domain settings, or bulk importing contacts.

## Manual Handoff Standard

When a live Brevo action is required, Codex should stop at a handoff section that tells the user what to do in Brevo.

The handoff should include:

- Brevo object names or IDs.
- Exact dashboard area to open.
- Values to copy.
- Test-send or preview checks.
- The final manual action the user performs inside Brevo.
