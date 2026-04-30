# Optional Webhook Management

Webhook management is not bundled in Brevo Helper's default MCP configuration.

Reason: webhook endpoints can affect production event delivery. Creating, deleting, or changing webhook destinations can break downstream systems or expose event data to the wrong service.

## Default Behavior

By default, Codex should:

- Plan webhook needs.
- Review webhook-related local code.
- Identify expected event destinations.
- Document manual Brevo dashboard setup.
- Avoid changing production webhook configuration.

## When Webhooks Are Needed

Use webhook planning for:

- Delivery/open/click event ingestion.
- CRM synchronization.
- Internal analytics.
- Lead lifecycle state updates.
- Debugging downstream automation.

## Manual Brevo Handoff

For webhook setup, Codex should provide:

- Destination URL.
- Events to subscribe to.
- Authentication or signing requirements.
- Test payload expectations.
- Rollback steps.
- The exact Brevo dashboard area where the user makes the change.

## Advanced Internal Variant

If a future private variant needs webhook-management MCP access, keep it separate from the safe public/default plugin.

That variant should require:

- Explicit installation.
- Explicit user confirmation before writes.
- Narrow tool allowlists where possible.
- A written rollback plan before changing production webhook destinations.
