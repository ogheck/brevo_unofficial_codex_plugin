# Example Brevo Drip Campaign Brief

This is an example output shape for a Brevo welcome sequence. It is not an activated campaign.

## Campaign Brief

Goal: Convert new website leads into booked consultations.

Audience: People who submit a lead form and consent to receive follow-up email.

Primary CTA: Book a consultation.

## Audience And Trigger

- Entry trigger: Contact is added to the confirmed website leads list.
- Required list: Website Leads.
- Exclusions: Existing customers and unsubscribed contacts.
- Required attributes: `FIRSTNAME`, `SOURCE`, `INTEREST`, `LAST_INQUIRY_DATE`.

## Sequence Plan

| Step | Timing | Subject | Preheader | Goal | CTA |
| --- | --- | --- | --- | --- | --- |
| 1 | Immediately | Thanks for reaching out | Here is what happens next | Confirm receipt and set expectations | Book a consultation |
| 2 | 2 days later | A quick way to compare options | What to ask before you decide | Educate and build trust | View the checklist |
| 3 | 5 days later | Still looking for the right fit? | We can help you narrow it down | Recover undecided leads | Reply with a question |

## Message Drafts

### Message 1

Subject: Thanks for reaching out

Preheader: Here is what happens next

Body:

Hi {{ contact.FIRSTNAME | default: "there" }},

Thanks for getting in touch. We received your request and will use the details you shared to point you in the right direction.

If you are ready to talk through options, you can book a consultation now.

CTA: Book a consultation

### Message 2

Subject: A quick way to compare options

Preheader: What to ask before you decide

Body:

Hi {{ contact.FIRSTNAME | default: "there" }},

Choosing the right next step is easier when you compare timing, cost, scope, and fit side by side.

Use the checklist before you commit, and bring any questions to your consultation.

CTA: View the checklist

### Message 3

Subject: Still looking for the right fit?

Preheader: We can help you narrow it down

Body:

Hi {{ contact.FIRSTNAME | default: "there" }},

If you are still comparing options, reply with the biggest question on your mind. We can help you sort through the tradeoffs.

CTA: Reply with a question

## Brevo Assets Needed

- List: Website Leads.
- Templates: Welcome 1, Welcome 2, Welcome 3.
- Attributes: `FIRSTNAME`, `SOURCE`, `INTEREST`, `LAST_INQUIRY_DATE`.
- Segment: Website leads not converted after 7 days.

## Backend Requirements

- Server-side lead endpoint creates or updates contacts.
- Endpoint adds contacts to the Website Leads list.
- Endpoint stores `SOURCE` and `LAST_INQUIRY_DATE`.
- Public form uses a honeypot or Turnstile.
- `BREVO_API_KEY` stays server-side.

## QA Checklist

- Confirm each personalization field has a fallback.
- Confirm sender and domain are authenticated.
- Confirm unsubscribe and physical address footer exist.
- Confirm every CTA URL works.
- Send Brevo test emails to internal recipients.
- Confirm automation delays and exclusions before activation.

## Manual Brevo Handoff

1. Create or confirm the Website Leads list in Brevo.
2. Create required contact attributes.
3. Build the three templates from the copy above.
4. Configure the automation trigger and delays in Brevo.
5. Send test emails from Brevo.
6. Manually activate the automation in Brevo after review.
