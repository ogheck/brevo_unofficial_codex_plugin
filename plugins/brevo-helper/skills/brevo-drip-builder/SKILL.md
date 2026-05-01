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
- Campaign type: welcome, lead nurture, quote follow-up, abandoned inquiry, post-purchase, review request, winback, or re-engagement.
- Contact attributes needed for personalization.
- Brevo list, segment, or form context if available.
- Unsubscribe/compliance needs.
- Backend events or webhooks needed to support the flow.

If the user does not specify a campaign type, choose the closest fit from the entry trigger and goal. Use `references/drip-playbooks.md` when available for timing, assets, suppression rules, and backend event defaults.

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

Use this standard section order unless the user asks for a different format:

1. Campaign Brief.
2. Audience And Trigger.
3. Sequence Plan.
4. Message Drafts.
5. Brevo Assets Needed.
6. Backend Requirements.
7. QA Checklist.
8. Manual Brevo Handoff.

## Prompt Examples

Handle prompts like:

- "Create a 4-email welcome sequence for a home service lead form."
- "Build a Brevo nurture campaign for free estimate requests."
- "Draft winback emails for inactive customers."
- "Map the backend events and contact attributes needed for this drip."

## Campaign Type Defaults

Use these defaults as a starting point, then adapt to the user's business and consent model:

| Type | Default trigger | Typical sequence | Main exit or suppression |
| --- | --- | --- | --- |
| Welcome | Consented lead joins a list | 3 to 5 emails over 1 to 10 days | Converted, unsubscribed, or moved to customer list |
| Lead nurture | Lead shows interest in a category | 4 to 6 emails over 2 to 4 weeks | Booked, purchased, stale, or excluded segment |
| Quote follow-up | Quote requested or sent | 3 to 4 emails over 1 to 10 days | Quote accepted, declined, expired, or replied |
| Abandoned inquiry | Consented lead starts but does not complete an inquiry | 1 to 2 emails within 72 hours | Inquiry completed or no consent/lawful basis |
| Post-purchase | Purchase or service completion | 3 to 4 emails over 1 to 30 days | Refund, support escalation, or repeat purchase |
| Review request | Fulfillment complete and customer is eligible | 1 to 2 emails over 3 to 10 days | Review submitted or open support issue |
| Winback | Customer inactive after expected interval | 2 to 3 emails over 2 to 4 weeks | Purchase, opt-out, or suppressed segment |
| Re-engagement | Subscriber inactive for engagement window | 2 to 3 emails over 1 to 3 weeks | Clicked, unsubscribed, or sunset from list |

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
