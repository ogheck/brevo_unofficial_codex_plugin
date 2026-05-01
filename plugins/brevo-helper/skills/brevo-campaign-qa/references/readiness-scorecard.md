# Brevo Campaign Readiness Scorecard

Codex reviews and prepares. The user sends, schedules, submits, or launches manually inside Brevo.

## Verdict Rules

| Verdict | Rule | Handoff |
| --- | --- | --- |
| Blocked | Any P0 issue exists | Do not test or launch until fixed |
| Needs changes | No P0 issues, but one or more P1 issues exist | Internal Brevo test send may be useful after targeted fixes |
| Ready for Brevo test | No P0 or P1 issues found | User sends an internal test from Brevo before any real send |

## Priority Levels

| Priority | Meaning | Examples |
| --- | --- | --- |
| P0 Blocker | High-risk issue that can break compliance, delivery, audience targeting, or conversion | Missing unsubscribe footer, missing physical address where required, broken primary CTA, wrong list or segment, unverified sender/domain, no consent basis |
| P1 Fix Before Send | Issue that should be fixed before a real send | Missing personalization fallback, subject/preheader mismatch, missing suppression, inconsistent UTM tags, unclear CTA, missing plain-text fallback |
| P2 Improve | Quality improvement that should not block internal testing | Shorten opening copy, improve mobile scannability, tighten CTA language, remove secondary distractions |

## Required Review Areas

- Audience, list, segment, exclusions, and consent basis.
- Sender identity and domain authentication.
- Subject, preheader, CTA, and landing page alignment.
- Links, placeholders, UTM tags, and tracking settings.
- Personalization tokens and fallback values.
- Compliance footer, unsubscribe link, and physical address.
- Mobile readability and plain-text fallback.
- Test recipient list and internal review plan.

## Finding Format

Use this structure for each finding:

- Priority.
- Affected asset.
- Evidence.
- Recommended fix.
- Where to fix: Brevo dashboard, local template/code, or both.

## Manual Test Handoff

When the campaign is ready for testing, instruct the user to:

1. Open the campaign or template in Brevo.
2. Apply any remaining dashboard-only fixes.
3. Send a Brevo test email to internal recipients.
4. Confirm links, personalization fallbacks, unsubscribe footer, sender, domain, plain-text fallback, and mobile rendering.
5. Manually send or schedule from Brevo only after the internal test passes.
