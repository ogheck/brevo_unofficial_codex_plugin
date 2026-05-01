# Campaign QA Workflow

Use this workflow before the user sends, schedules, submits, or launches a Brevo campaign manually.

Codex reviews and prepares. The user performs the final live action inside Brevo.

Use the [campaign QA scorecard](campaign-qa-scorecard.md) to assign priorities and readiness verdicts.

## Inputs

Gather or infer:

- Campaign name or draft.
- Audience, list, or segment.
- Sender.
- Subject.
- Preheader.
- Template copy.
- CTA URLs.
- Personalization fields.
- Compliance footer.
- UTM or attribution needs.
- Comparable analytics when available.

## Output Sections

Use this structure:

1. Readiness Verdict.
2. Blocking Issues.
3. Recommended Improvements.
4. Brevo Setup Checks.
5. Test Plan.
6. Manual Brevo Handoff.

## Checks

Review:

- Broken or placeholder links.
- Subject and preheader alignment.
- CTA clarity.
- Personalization fallbacks.
- Sender/domain readiness.
- Unsubscribe and physical address footer.
- List and segment fit.
- Suppression or exclusion needs.
- Mobile readability.
- Plain-text fallback.
- UTM and attribution consistency.

## Finding Priorities

- P0 Blocker: must be fixed before Brevo test send or launch.
- P1 Fix Before Send: should be fixed before a real send.
- P2 Improve: useful quality improvement that should not block internal testing.

## Manual Brevo Handoff

End with the exact dashboard steps:

- Open the campaign or template.
- Apply copy or setup changes.
- Send a Brevo test email to internal recipients.
- Confirm links, footer, sender, list, and tracking.
- The user manually sends, schedules, or submits from Brevo only after review.
