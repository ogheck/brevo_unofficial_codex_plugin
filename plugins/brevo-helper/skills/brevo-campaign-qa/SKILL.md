---
name: brevo-campaign-qa
description: Review, prepare, debug, or QA Brevo campaigns, templates, transactional emails, sender setup, domain setup, webhooks, and analytics before sending.
---

# Brevo Campaign QA

Use this skill for Brevo email campaign and template work.

## Read First

Before editing or sending anything, inspect:

- Campaign draft status, subject, sender, recipients, schedule, and included lists or segments.
- Template variables and required attributes.
- Sender and domain authentication status.
- Unsubscribe and compliance links.
- Recent analytics for comparable campaigns when relevant.
- Webhook configuration if tracking or downstream automation is involved.

## QA Checklist

Check for:

- Broken or placeholder links.
- Missing personalization fallback values.
- Missing unsubscribe footer or physical address where required.
- Unverified sender/domain setup.
- Wrong list, segment, or suppression handling.
- Misleading subject/preheader mismatch.
- Test-recipient safety before any broad send.
- UTM and attribution consistency.
- Mobile-readable layout and plain-text fallback where available.

## Write Safety

Do not send, schedule, or launch campaigns without explicit user confirmation.

For send-like actions, state:

- Campaign name or ID.
- Audience/list/segment.
- Sender.
- Subject.
- Estimated recipient count if available.
- Exact action requested.

Wait for the user to approve before executing the send or schedule operation.
