# Example Brevo Quote Follow-Up Brief

This is an example output shape for a Brevo quote follow-up sequence. It is not an activated campaign.

## Campaign Brief

Goal: Help recent quote requesters understand the proposal and convert them into booked customers.

Audience: People who requested or received a quote and consented to follow-up email.

Primary CTA: Approve the quote or book a review call.

## Audience And Trigger

- Entry trigger: Contact attribute `QUOTE_STATUS` becomes `sent`.
- Required list: Quote Requests.
- Exclusions: Contacts with `QUOTE_STATUS` of `accepted`, `declined`, or `expired`; unsubscribed contacts; active support escalations.
- Required attributes: `FIRSTNAME`, `QUOTE_STATUS`, `QUOTE_SENT_DATE`, `SERVICE_INTEREST`, `QUOTE_REVIEW_URL`.

## Sequence Plan

| Step | Timing | Subject | Preheader | Goal | CTA | Success Metric |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | 1 hour after quote is sent | Your quote is ready | Review the details and next steps | Confirm quote delivery and reduce confusion | Review your quote | Quote review page visits |
| 2 | 2 days later | Questions about your quote? | A quick review can help | Invite replies and remove objections | Book a review call | Calls booked or replies |
| 3 | 5 days later | Want us to hold this option? | We can help you choose the right next step | Create a clear decision path | Approve the quote | Quote approvals |
| 4 | 10 days later, optional | Should we close this out? | Tell us what changed | Clean up stale opportunities respectfully | Update your request | Status updates |

## Message Drafts

### Message 1

Subject: Your quote is ready

Preheader: Review the details and next steps

Body:

Hi {{ contact.FIRSTNAME | default: "there" }},

Your quote for {{ contact.SERVICE_INTEREST | default: "your request" }} is ready to review.

The quote page includes the recommended scope, timing, and next steps. If anything looks off, reply to this email and we will help you adjust it.

CTA: Review your quote

### Message 2

Subject: Questions about your quote?

Preheader: A quick review can help

Body:

Hi {{ contact.FIRSTNAME | default: "there" }},

If you are comparing options or want to talk through the quote, we can review the details with you and explain where the recommendation came from.

CTA: Book a review call

### Message 3

Subject: Want us to hold this option?

Preheader: We can help you choose the right next step

Body:

Hi {{ contact.FIRSTNAME | default: "there" }},

Your quote is still open. If the scope still looks right, approving it is the fastest way to reserve the next step.

If your needs changed, reply with the update and we can revise the quote.

CTA: Approve the quote

### Message 4

Subject: Should we close this out?

Preheader: Tell us what changed

Body:

Hi {{ contact.FIRSTNAME | default: "there" }},

We do not want to keep following up if this is no longer useful. Should we close this request, update it, or help you move forward?

CTA: Update your request

## Brevo Assets Needed

- List: Quote Requests.
- Templates: Quote Follow-Up 1, Quote Follow-Up 2, Quote Follow-Up 3, optional Quote Follow-Up 4.
- Attributes: `FIRSTNAME`, `QUOTE_STATUS`, `QUOTE_SENT_DATE`, `SERVICE_INTEREST`, `QUOTE_REVIEW_URL`.
- Segment: Quote requests where `QUOTE_STATUS` is `sent` and `QUOTE_SENT_DATE` is within the active follow-up window.

## Backend Requirements

- Server-side quote workflow creates or updates the Brevo contact.
- Backend sets `QUOTE_STATUS` to `sent` when the quote is ready.
- Backend stores `QUOTE_SENT_DATE`, `SERVICE_INTEREST`, and `QUOTE_REVIEW_URL`.
- Quote approval or decline updates `QUOTE_STATUS` so the automation can stop.
- `BREVO_API_KEY` stays server-side.

## QA Checklist

- Confirm every quote URL is unique to the recipient and does not expose private data in public logs.
- Confirm each personalization field has a fallback.
- Confirm the quote accepted, declined, expired, and unsubscribed exclusions are active.
- Confirm sender and domain are authenticated.
- Confirm unsubscribe and physical address footer exist.
- Send Brevo test emails to internal recipients.
- Confirm automation delays and stop conditions before activation.

## Manual Brevo Handoff

1. Create or confirm the Quote Requests list in Brevo.
2. Create required contact attributes.
3. Build the templates from the copy above.
4. Configure the automation trigger, delays, and exclusions in Brevo.
5. Send test emails from Brevo.
6. Manually activate the automation in Brevo after review.
