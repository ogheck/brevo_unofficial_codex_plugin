# Example Copy Style Profile: Warm Professional

Use this profile for service businesses, consultants, local operators, and most first-pass Brevo drip campaign drafts when the user has not supplied a stricter brand voice.

## Profile

Name: Warm Professional.

Voice: Clear, helpful, direct, lightly personal.

Best for: Welcome sequences, quote follow-up, lead nurture, and consultation booking.

Avoid:

- Overly casual jokes.
- Urgency that is not real.
- Dense jargon.
- Unsupported superlatives.
- Multiple competing CTAs.

## Subject Style

- Short and specific.
- Tied to the trigger or next step.
- No clickbait.

Examples:

- Thanks for reaching out
- Your quote is ready
- A quick way to compare options
- Questions about your request?

## Preheader Style

- Add context that the subject does not repeat.
- Keep it useful even if the subject is all the user reads.

Examples:

- Here is what happens next
- Review the details and next steps
- What to ask before you decide
- We can help you narrow it down

## CTA Style

Use one clear action:

- Book a consultation.
- Review your quote.
- View the checklist.
- Reply with a question.

## Personalization Fallback

Use fallbacks that still sound natural:

```text
Hi {{ contact.FIRSTNAME | default: "there" }},
```

Avoid sentences that become awkward without the personalized value.
