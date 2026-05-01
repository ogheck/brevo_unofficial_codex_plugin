# Project Integrations

Use this file to track real projects connected to Brevo with this plugin.

Use [project integration intake](project-integration-intake.md) before editing a real target project.

## Integration Template

Project:

- Path:
- Runtime:
- Forms:
- Backend endpoint:
- Brevo lists:
- Brevo attributes:
- Sender/domain dependencies:
- Spam controls:
- Tests:
- Deployment target:
- Manual Brevo dashboard handoff:
- Status:

## Candidate: Phresh Start Website

Status: not started.

Known assumptions:

- Likely needs website lead capture or newsletter signup wiring.
- Exact project path still needs confirmation.
- Brevo list IDs and contact attributes still need confirmation from Brevo.

First implementation pass:

1. Inspect the project forms and current submit handlers.
2. Identify backend runtime and deployment target.
3. Confirm Brevo list and attributes through MCP or manual dashboard review.
4. Choose the closest backend template.
5. Wire the form to a server-side endpoint.
6. Add spam control.
7. Verify invalid email, valid submission, duplicate submission, and secret exposure checks.
8. Document final manual Brevo dashboard steps.

Template starter:

```bash
python3 scripts/create_integration_stub.py --runtime nextjs-route-handler --target ./brevo-lead-capture
```

Prepared intake:

- `docs/project-integration-intake.md`
- `plugins/brevo-helper/skills/brevo-site-integration/references/integration-intake.md`
