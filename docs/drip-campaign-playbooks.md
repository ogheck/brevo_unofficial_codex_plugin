# Drip Campaign Playbooks

Use these playbooks when turning a business goal into a Brevo-ready lifecycle campaign. They are planning defaults, not live automations.

Codex prepares the brief, copy, backend requirements, QA checklist, and dashboard instructions. The user builds, tests, sends, schedules, or activates inside Brevo.

## Playbook Matrix

| Playbook | Entry trigger | Suggested timing | Required data | Stop conditions |
| --- | --- | --- | --- | --- |
| Welcome | New consented lead joins target list | Immediate, day 2, day 5, optional day 10 | `FIRSTNAME`, `SOURCE`, `INTEREST`, `LAST_INQUIRY_DATE` | Converted, unsubscribed, hard bounce, moved to customer list |
| Lead nurture | Lead has a known interest or lifecycle stage | Day 0, 3, 7, 14, optional day 21 | `FIRSTNAME`, `INTEREST`, `SOURCE`, `LEAD_STAGE`, `LAST_ENGAGED_DATE` | Booked, purchased, stale, unsubscribed, excluded segment |
| Quote follow-up | Quote requested or quote sent | 1 hour, day 2, day 5, optional day 10 | `FIRSTNAME`, `QUOTE_STATUS`, `QUOTE_SENT_DATE`, `SERVICE_INTEREST` | Quote accepted, declined, expired, replied, unsubscribed |
| Abandoned inquiry | Consented lead began an inquiry and did not finish | 2 hours, optional day 2 | `FIRSTNAME`, `INQUIRY_STAGE`, `SOURCE`, `LAST_INQUIRY_DATE` | Inquiry completed, no consent, replied, unsubscribed |
| Post-purchase | Purchase, booking, or service completion recorded | Day 0, day 3, day 14, optional day 30 | `FIRSTNAME`, `PURCHASE_DATE`, `PRODUCT_OR_SERVICE`, `CUSTOMER_STAGE` | Refund, open support issue, repeat purchase, unsubscribed |
| Review request | Customer becomes eligible for review ask | Day 3, optional day 10 | `FIRSTNAME`, `SERVICE_DATE`, `REVIEW_ELIGIBLE`, `SUPPORT_STATUS` | Review submitted, open support issue, unsubscribed |
| Winback | Customer inactive beyond normal repeat window | Day 0, day 7, optional day 21 | `FIRSTNAME`, `LAST_PURCHASE_DATE`, `CUSTOMER_STAGE`, `PREFERRED_OFFER` | Purchase, active support issue, unsubscribed, suppressed |
| Re-engagement | Subscriber has not opened or clicked during engagement window | Day 0, day 7, final day 14 | `FIRSTNAME`, `LAST_ENGAGED_DATE`, `SUBSCRIBER_STATUS`, `SOURCE` | Clicked, unsubscribed, sunset from list |

## Required Brief Sections

Every drip brief should include:

- Campaign objective.
- Audience and trigger.
- Message sequence with timing, subject, preheader, CTA, personalization, and metric.
- Message drafts or template outline.
- Required Brevo assets.
- Backend event or form requirements.
- QA checklist.
- Manual Brevo dashboard handoff.

## Backend Event Defaults

Use these event names unless the target project already has a naming convention:

- `lead_submitted`
- `lead_interest_updated`
- `quote_requested`
- `quote_sent`
- `inquiry_abandoned`
- `purchase_completed`
- `review_eligible`
- `customer_inactive`
- `subscriber_reengagement_candidate`

## Compliance And Safety Notes

- Confirm consent or lawful basis before planning an abandoned inquiry, winback, or re-engagement flow.
- Give every personalization token a fallback.
- Add suppression rules for unsubscribed contacts, hard bounces, active support issues, and converted leads.
- Keep Brevo API keys server-side.
- Do not use Codex to send, schedule, submit, activate, or enroll contacts into the campaign.
