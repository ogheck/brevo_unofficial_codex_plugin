# Example Attribute Mapping: Website Lead

| Local Field | Brevo Attribute | Required | Normalization | Manual Brevo Handoff |
| --- | --- | --- | --- | --- |
| `email` | Contact email | Yes | Trim and lowercase. | Confirm email consent language on form. |
| `firstName` | `FIRSTNAME` | No | Trim. | Confirm attribute exists. |
| `lastName` | `LASTNAME` | No | Trim. | Confirm attribute exists. |
| `phone` | `SMS` | No | Trim; prefer country code. | Confirm SMS consent before SMS use. |
| `source` | `SOURCE` | Yes | Use stable value `website-form`. | Create custom text attribute if missing. |
| `message` | `MESSAGE` | No | Trim and truncate to 1000 chars. | Decide retention/privacy policy. |

## Backend Notes

- Keep `BREVO_API_KEY` server-side.
- Add the contact to configured list IDs.
- Treat duplicate contacts as expected.
- Do not enroll contacts into live automations from Codex.

## Manual Brevo Handoff

1. Confirm or create `SOURCE` as a text attribute.
2. Confirm `FIRSTNAME` and `LASTNAME` exist.
3. Confirm whether `MESSAGE` should be stored as a contact attribute.
4. Confirm target list IDs in Brevo.
5. Manually configure related automations in Brevo after tests pass.
