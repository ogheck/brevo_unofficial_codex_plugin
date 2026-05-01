# Brevo Drip Playbooks

These playbooks are planning defaults for Codex output. Codex must not activate automations, enroll contacts, send messages, schedule messages, or submit campaigns from Brevo.

## Universal Assets

Every drip brief should identify:

- Entry trigger and consent basis.
- Required list, segment, or form.
- Required contact attributes and fallbacks.
- Template names and message count.
- Exclusions, suppression rules, and stop conditions.
- Backend event or form requirements.
- Dashboard handoff steps for manual Brevo setup, testing, and activation.

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

## Copy Rules

- Give every personalization token a fallback.
- Keep the first message tightly aligned to the trigger.
- Make only claims the user can substantiate.
- Prefer one primary CTA per message.
- Include compliance reminders for unsubscribe footer, sender identity, and physical address.
- For re-engagement and winback, include a clear preference or opt-out path.

## Backend Event Defaults

Use these names in briefs unless the user's project already has event names:

- `lead_submitted`
- `lead_interest_updated`
- `quote_requested`
- `quote_sent`
- `inquiry_abandoned`
- `purchase_completed`
- `review_eligible`
- `customer_inactive`
- `subscriber_reengagement_candidate`

The plugin can plan these events and build server-side code that records attributes or list membership. The user still configures and activates Brevo automations manually.
