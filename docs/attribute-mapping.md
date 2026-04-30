# Attribute Mapping

Use this guide when mapping website or app fields to Brevo contact attributes.

## Rules

- Confirm attributes exist in Brevo before relying on them.
- Use uppercase Brevo attribute names in API payloads.
- Keep source field names stable in local code.
- Normalize email before sending it to Brevo.
- Store phone numbers in Brevo's `SMS` attribute only when formatting and consent expectations are clear.
- Do not invent production attributes without a manual Brevo dashboard handoff.

## Common Mapping

| Local Field | Brevo Attribute | Notes |
| --- | --- | --- |
| `email` | Contact email | Required for email contacts. |
| `firstName` | `FIRSTNAME` | Add fallback in campaign copy. |
| `lastName` | `LASTNAME` | Optional. |
| `phone` | `SMS` | Use proper country code when possible. |
| `source` | `SOURCE` | Use a stable source value such as `website-form`. |
| `message` | `MESSAGE` | Consider truncation and privacy needs. |
| `interest` | `INTEREST` | Confirm custom attribute exists. |
| `lastInquiryDate` | `LAST_INQUIRY_DATE` | Confirm Brevo date format and attribute type. |

## Output Format

When Codex maps a project form, return:

- Local field.
- Brevo attribute.
- Data type.
- Required or optional.
- Normalization rule.
- Consent or privacy note.
- Whether the Brevo attribute exists or must be created manually.

## Manual Brevo Handoff

If attributes are missing, tell the user:

- Attribute name.
- Attribute type.
- Where it is used.
- Whether old contacts need backfill.
- Which templates or segments depend on it.
