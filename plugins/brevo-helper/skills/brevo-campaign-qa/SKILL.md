---
name: brevo-campaign-qa
description: Review, prepare, debug, or QA Brevo campaign plans, templates, transactional email copy, sender setup, domain setup, webhooks, and analytics for manual Brevo dashboard sending.
---

# Brevo Campaign QA

Use this skill for Brevo email campaign and template work. Codex prepares and reviews assets; the user sends or schedules inside Brevo.

Use `references/readiness-scorecard.md` when available to grade findings and decide whether the campaign is blocked, needs changes, or is ready for a Brevo dashboard test send.

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

## Severity Model

Use this priority model:

| Priority | Meaning | Examples |
| --- | --- | --- |
| P0 Blocker | Must be fixed before Brevo test send or launch | Missing unsubscribe footer, broken primary CTA, unverified sender/domain, wrong audience |
| P1 Fix Before Send | Should be fixed before broad send, but may be tested internally | Missing fallback, weak suppression, subject/preheader mismatch, missing UTM |
| P2 Improve | Useful polish that should not block internal testing | Copy clarity, mobile scannability, secondary CTA cleanup |

Readiness verdicts:

- `Blocked`: any P0 issue exists.
- `Needs changes`: no P0 issues, but one or more P1 issues exist.
- `Ready for Brevo test`: no P0 or P1 issues found; user should still test manually in Brevo.

## Output Structure

Use this standard section order:

1. Readiness Verdict.
2. Blocking Issues.
3. Recommended Improvements.
4. Brevo Setup Checks.
5. Test Plan.
6. Manual Brevo Handoff.

If no blocking issues are found, say that clearly and still include the test-send checklist for the Brevo dashboard.

For each finding, include priority, affected asset, evidence, recommended fix, and whether Brevo or local project files need to change.

## Prompt Examples

Handle prompts like:

- "Review this Brevo email before I send it."
- "QA this campaign subject, preheader, and CTA."
- "Check whether this template is ready for Brevo."
- "Look at my sender/domain setup before launch."

Use Brevo MCP for sender, domain, template, list, and analytics context when available. Use local files for HTML templates, generated copy, route output, and tracked links when the campaign content lives in the project.

Use `docs/analytics-review-workflow.md` when the user asks for performance analysis or recommendations from Brevo campaign analytics.

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
