# Example Brevo Campaign QA Report

This is an example output shape for campaign review. It is not a sent or scheduled campaign.

## Readiness Verdict

Status: blocked.

Reason: One P0 blocker and two P1 issues need confirmation before the user sends from Brevo.

## Blocking Issues

- P0 Blocker: CTA URL is still a placeholder.
- P1 Fix Before Send: `FIRSTNAME` personalization needs a fallback value.
- P1 Fix Before Send: Sender/domain authentication status is not confirmed.

## Recommended Improvements

- P1 Fix Before Send: Align the subject and preheader so they promise the same outcome.
- P2 Improve: Shorten the first paragraph for mobile scanning.
- P2 Improve: Add one primary CTA and remove duplicate competing links.
- P1 Fix Before Send: Add UTM parameters to the CTA URL.

## Brevo Setup Checks

- List or segment: confirm the audience is the intended list.
- Sender: confirm sender identity is verified.
- Domain: confirm domain authentication passes.
- Footer: confirm unsubscribe and physical address footer are present.
- Plain text: confirm Brevo has a readable fallback.

## Test Plan

1. Send a Brevo test email to internal recipients.
2. Open the test email on desktop and mobile.
3. Click every link.
4. Confirm personalization fallback rendering.
5. Confirm unsubscribe footer and sender details.
6. Confirm tracking settings.

## Manual Brevo Handoff

1. Open the campaign in Brevo.
2. Replace placeholder CTA links.
3. Add personalization fallbacks.
4. Confirm sender/domain readiness.
5. Send test emails from Brevo.
6. Manually send or schedule from Brevo only after the checks pass.
