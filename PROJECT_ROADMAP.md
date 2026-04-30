# Brevo Helper Codex Plugin Roadmap

Last updated: 2026-04-30

## Project Goal

Build an unofficial Codex plugin that helps create Brevo-backed marketing systems without letting Codex send, schedule, submit, activate, or enroll contacts in live Brevo messaging flows.

The plugin should help with:

- Planning drip campaigns and lifecycle sequences.
- Drafting marketing messages and Brevo-ready campaign copy.
- Reviewing Brevo assets, sender/domain setup, lists, templates, analytics, and webhooks.
- Building backend code that lets project users submit forms or events into Brevo safely.
- Producing clear Brevo dashboard handoff instructions for the user to complete manually.

## Core Principle

Codex prepares, reviews, and builds. The user performs final live Brevo actions inside Brevo.

Codex must not:

- Send email, SMS, or WhatsApp messages.
- Schedule, launch, submit, or resend campaigns.
- Activate live drip automations.
- Enroll contacts into live automations.
- Make broad destructive Brevo changes without explicit confirmation.

## Current Status

Done:

- Created repo-backed Codex marketplace structure.
- Added `brevo-helper` plugin manifest.
- Added focused Brevo MCP config using `BREVO_MCP_TOKEN`.
- Removed the campaign-management MCP endpoint from the default package.
- Added read-oriented plugin metadata.
- Added skills for Brevo operations, site integration, campaign QA, and drip building.
- Added README, license, icon, gitignore, and marketplace metadata.
- Pushed initial commits to GitHub.

Not done:

- Install and load-test the plugin from GitHub in Codex.
- Test Brevo MCP auth with a real `BREVO_MCP_TOKEN`.
- Build backend integration templates.
- Add example projects and fixtures.
- Add validation scripts.
- Add release checklist and versioning process.

## Phase 0: Charter And Safety Model

Status: mostly complete

Goal: Define what this plugin is allowed to do and what it must never do.

Tasks:

- Document the unofficial nature of the plugin.
- Define the no-direct-send boundary.
- Make Brevo dashboard handoff the default final step.
- Reduce accidental write surface in bundled MCP config.
- Add explicit confirmation requirements for risky non-send writes.
- Keep secrets out of repo, chat, frontend code, and public environment variables.

Acceptance criteria:

- README clearly states the plugin is unofficial.
- README clearly states Codex must not send or schedule from Brevo.
- Skill instructions enforce the same rule.
- Plugin metadata does not market the plugin as an official Brevo product.

## Phase 1: Plugin Packaging Foundation

Status: mostly complete

Goal: Make the repo installable as a Codex plugin marketplace source.

Tasks:

- Maintain `.agents/plugins/marketplace.json`.
- Maintain `plugins/brevo-helper/.codex-plugin/plugin.json`.
- Maintain `plugins/brevo-helper/.mcp.json`.
- Keep all plugin paths relative to plugin root.
- Keep version in `plugin.json` current.
- Add install instructions for GitHub and local development.

Acceptance criteria:

- `codex plugin marketplace add ogheck/brevo_unofficial_codex_plugin` can discover the marketplace.
- Brevo Helper appears in Codex plugin directory.
- Installing the plugin exposes bundled skills.
- Invalid JSON checks pass for plugin manifest, MCP config, and marketplace file.

## Phase 2: Brevo MCP Read Integration

Status: planned

Goal: Confirm the plugin can inspect Brevo state without enabling direct send operations.

Bundled read-oriented MCP surfaces:

- Contacts.
- Lists.
- Templates.
- Transactional templates.
- Campaign analytics.
- Webhooks.
- Senders.
- Domains.

Tasks:

- Generate a Brevo MCP token in Brevo.
- Set `BREVO_MCP_TOKEN` for Codex CLI and Codex app.
- Verify each bundled MCP endpoint initializes.
- Verify useful read operations work for contacts, lists, templates, analytics, senders, and domains.
- Document any endpoint that needs narrower tool allowlists.
- Decide whether webhook management should remain bundled or move to optional setup because it can mutate production behavior.

Acceptance criteria:

- Codex can read Brevo lists and contact attributes.
- Codex can read template metadata.
- Codex can read sender/domain state.
- Codex can read campaign analytics.
- No default tool path allows accidental direct campaign send or schedule.

## Phase 3: Skill Workflow V1

Status: in progress

Goal: Make Codex reliably choose the right workflow for common Brevo work.

Current skills:

- `brevo`: umbrella workflow and safety boundary.
- `brevo-site-integration`: website/backend lead capture.
- `brevo-campaign-qa`: campaign and template review for manual send.
- `brevo-drip-builder`: drip campaign planning and message drafting.

Tasks:

- Tighten skill descriptions so Codex routes correctly.
- Add examples for common prompts.
- Add a standard output format for each skill.
- Add a "manual Brevo handoff" section to every workflow output.
- Add guidance for when to use Brevo MCP versus local project files.

Acceptance criteria:

- "Build a Brevo drip campaign" triggers drip-builder behavior.
- "Connect this form to Brevo" triggers site integration behavior.
- "Review this campaign before I send" triggers campaign QA behavior without sending.
- Every workflow ends with manual dashboard steps when Brevo action is required.

## Phase 4: Backend Integration Templates

Status: planned

Goal: Provide reusable backend patterns for projects that need Brevo form/event submission.

Templates to create:

- Static HTML plus serverless endpoint.
- Cloudflare Pages Functions.
- Cloudflare Workers.
- Vercel/Next.js route handler.
- Express/Node endpoint.

Core backend behavior:

- Validate input.
- Normalize email and phone fields.
- Apply spam controls such as honeypot, Turnstile, or basic rate limiting.
- Create or update a Brevo contact with server-side `BREVO_API_KEY`.
- Add contact to configured list IDs.
- Populate existing Brevo attributes.
- Handle duplicate contacts gracefully.
- Return safe public error messages.
- Log enough for debugging without leaking secrets or personal data.

Files to add:

- `examples/cloudflare-pages-function/`
- `examples/cloudflare-worker/`
- `examples/nextjs-route-handler/`
- `examples/express-endpoint/`
- `docs/backend-patterns.md`

Acceptance criteria:

- Each template documents required env vars.
- Each template avoids browser-exposed Brevo keys.
- Each template includes validation and duplicate handling.
- Each template includes local test instructions.

## Phase 5: Drip Campaign Builder

Status: planned

Goal: Turn business goals into Brevo-ready lifecycle campaign plans.

Features:

- Intake questionnaire for project, audience, offer, goal, voice, and timing.
- Sequence planner with message timing, subject, preheader, CTA, and success metric.
- Draft copy for each message.
- Personalization field list.
- Required contact attributes.
- Required lists, segments, forms, templates, and events.
- Backend event requirements.
- Brevo dashboard setup checklist.
- QA checklist before manual activation.

Drip campaign types:

- Welcome sequence.
- Lead nurture.
- Quote follow-up.
- Abandoned inquiry.
- Post-purchase follow-up.
- Review request.
- Winback.
- Re-engagement.

Acceptance criteria:

- User can ask for a drip campaign and get a complete implementation brief.
- Output can be copied into Brevo templates and automation steps.
- Output includes backend requirements when form/event capture is needed.
- Output never claims Codex activated or submitted the campaign.

## Phase 6: Campaign And Template QA

Status: planned

Goal: Help the user catch marketing, compliance, and technical issues before using Brevo to send.

Checks:

- Subject and preheader alignment.
- CTA clarity.
- Link completeness.
- Personalization fallbacks.
- Sender/domain readiness.
- Unsubscribe and compliance footer.
- List and segment fit.
- UTM and attribution consistency.
- Mobile readability.
- Plain-text fallback.
- Test-send checklist for Brevo dashboard.

Acceptance criteria:

- Campaign QA returns prioritized findings.
- Campaign QA returns a manual "ready to test in Brevo" checklist.
- Campaign QA does not send, schedule, or submit anything.

## Phase 7: Project-Specific Website Integration

Status: planned

Goal: Use the plugin on a real project, starting with the first target site.

Initial target:

- Confirm first target project path before implementation.
- Likely candidate: Phresh Start Website.

Tasks:

- Inspect existing forms and serverless routes.
- Identify desired Brevo lists and attributes.
- Build backend endpoint.
- Wire frontend form submission.
- Add spam/rate-limit control.
- Add local and staging verification steps.
- Add project-specific notes to `docs/project-integrations.md`.

Acceptance criteria:

- A real form can submit to the backend.
- Backend can create/update Brevo contact in the intended list.
- No Brevo secret appears in frontend code.
- User can finish any required Brevo dashboard setup manually.

## Phase 8: Verification And Test Harness

Status: planned

Goal: Make plugin behavior and examples testable.

Tasks:

- Add JSON validation script for plugin and marketplace files.
- Add markdown lint or simple link check.
- Add example endpoint tests where templates include code.
- Add install smoke-test checklist.
- Add MCP auth smoke-test checklist.
- Add "no direct send" review checklist.

Potential files:

- `scripts/validate_plugin.py`
- `docs/testing.md`
- `docs/release-checklist.md`

Acceptance criteria:

- `python3 scripts/validate_plugin.py` validates required plugin files.
- README install instructions are tested.
- No bundled MCP server includes campaign send/schedule management by default.
- Roadmap and README stay aligned.

## Phase 9: Documentation And Distribution

Status: planned

Goal: Make the plugin understandable and installable by another Codex user.

Tasks:

- Expand README quickstart.
- Add screenshots or terminal examples after local install works.
- Add `docs/brevo-token-setup.md`.
- Add `docs/no-direct-send-policy.md`.
- Add `docs/drip-campaign-workflow.md`.
- Add `docs/site-integration-workflow.md`.
- Add changelog.
- Tag releases.

Acceptance criteria:

- New user can install from GitHub with one command.
- New user understands how to set `BREVO_MCP_TOKEN`.
- New user understands that sends and activation happen in Brevo, not Codex.
- Releases have clear version notes.

## Phase 10: Optional Advanced Features

Status: future

Possible features:

- CLI helper that generates backend endpoint stubs from selected runtime.
- Attribute mapping assistant that compares local form fields to Brevo contact attributes.
- Drip copy style profiles for different projects.
- Campaign brief generator from website content.
- Analytics summary workflow that reads Brevo campaign analytics and recommends copy/segment improvements.
- Webhook event debugging guide for project-specific backends.
- Optional extra marketplace entry for a write-enabled internal variant, kept separate from this safe public/default plugin.

Decision required:

- Whether to keep one safe plugin only or maintain separate safe and internal variants.

## Feature Inventory

Must have:

- Installable Codex marketplace structure.
- Unofficial branding.
- Brevo MCP token setup docs.
- No-direct-send policy.
- Drip campaign planning.
- Marketing message drafting.
- Campaign QA.
- Backend lead-capture guidance.
- Website integration workflow.
- Manual Brevo dashboard handoff.

Should have:

- Backend templates for common runtimes.
- Validation script.
- Install smoke-test docs.
- Project-specific integration notes.
- Example drip campaign output.

Could have:

- Reusable form schema examples.
- Attribute mapping examples.
- Analytics review templates.
- Screenshot-based docs after the plugin is installed.

Won't have by default:

- Direct Brevo send/schedule/launch tools.
- Live automation activation from Codex.
- Contact enrollment into live automations from Codex.
- Client-side Brevo API keys.
- Official Brevo branding or logo unless explicitly authorized.

## Open Decisions

- Which real project should be the first integration target?
- Which backend runtime should be the first template: Cloudflare Pages Functions, Cloudflare Workers, Vercel/Next.js, or Express?
- Should webhook management remain bundled by default or move to an advanced optional setup?
- Should we create a direct `docs/` guide for Phresh Start once the first project is confirmed?
- Do we need a private internal branch for higher-permission Brevo workflows, or should this repository stay strictly no-send?

## Near-Term Build Order

1. Add validation script for plugin JSON and required files.
2. Install plugin locally from the GitHub marketplace.
3. Set `BREVO_MCP_TOKEN` and verify read-only Brevo MCP tools.
4. Build the first backend integration template.
5. Use the plugin on the first real project form.
6. Add drip campaign example output.
7. Add release checklist and tag `v0.1.1`.
