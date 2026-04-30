---
name: brevo-drip-builder
description: Plan Brevo drip campaigns, lifecycle sequences, nurture emails, campaign briefs, segmentation rules, and Brevo dashboard handoff steps without sending from Codex.
---

# Brevo Drip Builder

Use this skill when the user wants to build a drip campaign, lifecycle sequence, welcome series, winback flow, lead nurture, or marketing message set for Brevo.

Codex must not send, schedule, launch, submit, or enroll contacts in the drip campaign. The output should be ready for the user to implement or submit manually in Brevo.

## Inputs To Gather

Gather or infer:

- Business/project name.
- Audience and entry trigger.
- Offer or conversion goal.
- Brand voice and constraints.
- Number of messages and timing.
- Contact attributes needed for personalization.
- Brevo list, segment, or form context if available.
- Unsubscribe/compliance needs.
- Backend events or webhooks needed to support the flow.

## Output Structure

Produce:

- Campaign objective.
- Audience and entry conditions.
- Message sequence table with timing, subject, preheader, goal, CTA, and personalization fields.
- Full draft copy for each message when requested.
- Required Brevo assets: lists, segments, forms, templates, attributes, and webhooks.
- Backend implementation plan for capture, validation, events, and server-side Brevo API calls.
- Brevo dashboard handoff checklist.
- QA checklist before the user submits or schedules in Brevo.

## Backend Guidance

- Keep Brevo runtime API keys server-side only.
- Prefer a backend endpoint that validates form submissions and then creates/updates contacts or emits the required event.
- Do not place Brevo API keys in static HTML, frontend bundles, or public environment variables.
- Include spam/rate-limit controls for public forms.
- Treat duplicate contacts as expected behavior.

## Manual Handoff

End with the exact manual steps the user should take in Brevo, such as:

- Create or confirm the list/segment.
- Create the templates from the generated copy.
- Configure the automation trigger and delays.
- Send tests to internal recipients from Brevo.
- Review analytics/tracking settings.
- Manually activate the automation in Brevo.
