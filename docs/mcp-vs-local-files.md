# MCP Versus Local Files

Use this guide when deciding whether Brevo Helper should inspect Brevo through MCP, inspect the local codebase, or do both.

## Use Brevo MCP For

- Lists and list IDs.
- Contact attributes.
- Template metadata.
- Sender identity state.
- Domain authentication state.
- Campaign analytics.
- Existing contact/list/template context needed for planning or QA.

MCP access should be read-oriented in this plugin. Do not use Brevo MCP to send, schedule, launch, submit, activate, or enroll contacts into live messaging flows.

## Use Local Project Files For

- Form markup.
- Submit handlers.
- API routes.
- Serverless functions.
- Environment variable names.
- Existing CRM/email integrations.
- Frontend bundle exposure risk.
- Tests and deployment config.

Local code determines how the project should call Brevo. Brevo MCP determines what account objects the code should target.

## Use Both For Site Integrations

For a website or app form:

1. Inspect local files to find the form and backend runtime.
2. Use Brevo MCP to confirm lists, attributes, senders, domains, and templates.
3. Implement or adapt a server-side endpoint.
4. Keep `BREVO_API_KEY` server-side.
5. Verify local behavior with tests.
6. Give the user manual Brevo dashboard handoff steps.

## If MCP Is Unavailable

If MCP tools are unavailable or `BREVO_MCP_TOKEN` is missing:

- Continue with local code work where possible.
- Use placeholder list names rather than invented IDs.
- Tell the user exactly which Brevo objects must be confirmed manually.
- Do not ask the user to paste credentials into chat.

## If Local Files Are Unavailable

If the user only wants planning or copy:

- Produce the campaign, QA, or integration brief.
- Clearly mark implementation assumptions.
- Include the backend runtime options.
- Include the manual Brevo dashboard handoff.
