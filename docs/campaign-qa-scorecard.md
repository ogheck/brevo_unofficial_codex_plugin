# Campaign QA Scorecard

Use this scorecard when reviewing Brevo campaigns, templates, or transactional email copy before the user sends, schedules, submits, or launches from Brevo.

Codex reviews and prepares. The user performs final live actions inside Brevo.

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

## Review Areas

- Audience, list, segment, exclusions, and consent basis.
- Sender identity and domain authentication.
- Subject, preheader, CTA, and landing page alignment.
- Links, placeholders, UTM tags, and tracking settings.
- Personalization tokens and fallback values.
- Compliance footer, unsubscribe link, and physical address.
- Mobile readability and plain-text fallback.
- Test recipient list and internal review plan.

## Finding Format

Each finding should include:

- Priority.
- Affected asset.
- Evidence.
- Recommended fix.
- Where to fix: Brevo dashboard, local template/code, or both.

## Manual Brevo Test Handoff

1. Open the campaign or template in Brevo.
2. Apply any dashboard-only fixes.
3. Send a Brevo test email to internal recipients.
4. Confirm links, personalization fallbacks, unsubscribe footer, sender, domain, plain-text fallback, and mobile rendering.
5. Manually send or schedule from Brevo only after the internal test passes.
