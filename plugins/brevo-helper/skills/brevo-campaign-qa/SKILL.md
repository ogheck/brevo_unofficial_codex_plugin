---
name: brevo-campaign-qa
description: Review, prepare, debug, or QA Brevo campaign plans, templates, transactional email copy, sender setup, domain setup, webhooks, and analytics for manual Brevo dashboard sending.
---

# Brevo Campaign QA

Use this skill for Brevo email campaign and template work. Codex prepares and reviews assets; the user sends or schedules inside Brevo.

## Read First

Before editing or preparing send-ready assets, inspect:

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

## No Direct Sending

Do not send, schedule, launch, resend, or submit campaigns from Codex, even if the user asks casually. Keep the final send/schedule action in the Brevo dashboard.

For send-ready handoff, state:

- Campaign name or ID.
- Audience/list/segment.
- Sender.
- Subject.
- Estimated recipient count if available.
- Exact manual action the user should perform inside Brevo.

Stop after the handoff checklist.
