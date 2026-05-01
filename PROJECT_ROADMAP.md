# Brevo Helper Codex Plugin Roadmap

Last updated: 2026-05-01

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
- Added skills for Brevo operations, onboarding, site integration, campaign QA, and drip building.
- Added README, license, icon, gitignore, and marketplace metadata.
- Added static plugin validation script.
- Added testing and release checklist docs.
- Added backend integration patterns doc.
- Added first backend template: Cloudflare Pages Function lead-capture endpoint.
- Added tests for the Cloudflare Pages Function template.
- Added remaining backend templates for Cloudflare Workers, Next.js route handlers, Express, and static HTML plus serverless.
- Added endpoint tests for all backend templates.
- Added a repo-level example test runner.
- Added local Markdown link checker.
- Tightened bundled skill routing examples and output structures.
- Added no-direct-send, token setup, drip workflow, and site integration docs.
- Added example drip campaign brief output.
- Added changelog.
- Moved webhook management out of the default MCP config.
- Added MCP-versus-local-files guidance.
- Added campaign QA workflow and example QA report.
- Added project integration tracker and form schema fixture.
- Added attribute mapping guide and example.
- Added analytics review workflow and example.
- Added release status doc with current blockers.
- Expanded README quickstart and development checks.
- Added release preflight script.
- Added GitHub Actions validation workflow.
- Confirmed the initial GitHub Actions validation run passed.
- Added backend integration stub generator and tests.
- Added bundled drip campaign playbooks and a quote follow-up campaign example.
- Added campaign QA readiness scorecard guidance.
- Added site integration intake guidance for first real-project wiring.
- Added CLI smoke-test examples for marketplace refresh and release preflight.
- Added copy style profiles for Brevo drip campaign drafting.
- Added Brevo MCP initialize smoke-test script for live read-endpoint checks.
- Added Codex app marketplace/plugin install-state diagnostic.
- Added guided install-time onboarding docs and verifier script.
- Switched marketplace authentication policy to install-time setup.
- Added the local repo as a Codex marketplace source for smoke testing.
- Added the GitHub repo as a Codex marketplace source for smoke testing.
- Refreshed the GitHub marketplace cache with the latest pushed revision.
- Confirmed strict live release preflight passes with the current Brevo MCP token environment.
- Confirmed Codex app install-state diagnostic passes after installing Brevo Helper.
- Pushed initial commits to GitHub.

Not done:

- Confirm bundled Brevo Helper skills and MCP tools are visible inside a fresh Codex app thread.
- Tag `v0.1.1` after install and MCP smoke tests pass.

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

Status: in progress

Goal: Confirm the plugin can inspect Brevo state without enabling direct send operations.

Bundled read-oriented MCP surfaces:

- Contacts.
- Lists.
- Templates.
- Transactional templates.
- Campaign analytics.
- Senders.
- Domains.

Tasks:

- Generate a Brevo MCP token in Brevo.
- Set `BREVO_MCP_TOKEN` for Codex CLI and Codex app.
- Verify each bundled MCP endpoint initializes.
- Verify useful read operations work for contacts, lists, templates, analytics, senders, and domains.
- Document any endpoint that needs narrower tool allowlists.
- Done: Move webhook management to optional documentation because it can mutate production behavior.

Added:

- `docs/mcp-vs-local-files.md`
- `docs/optional-webhook-management.md`

Acceptance criteria:

- Codex can read Brevo lists and contact attributes.
- Codex can read template metadata.
- Codex can read sender/domain state.
- Codex can read campaign analytics.
- No default tool path allows accidental direct campaign send or schedule.

## Phase 3: Skill Workflow V1

Status: complete

Goal: Make Codex reliably choose the right workflow for common Brevo work.

Current skills:

- `brevo`: umbrella workflow and safety boundary.
- `brevo-onboarding`: install-time setup, credential guidance, and smoke testing.
- `brevo-site-integration`: website/backend lead capture.
- `brevo-campaign-qa`: campaign and template review for manual send.
- `brevo-drip-builder`: drip campaign planning and message drafting.

Done:

- Tighten skill descriptions so Codex routes correctly.
- Add onboarding routing for setup, token, API key, sender/domain, and IP checks.
- Add examples for common prompts.
- Add a standard output format for each skill.
- Add a "manual Brevo handoff" section to every workflow output.
- Add guidance for when to use Brevo MCP versus local project files.

Acceptance criteria:

- "Build a Brevo drip campaign" triggers drip-builder behavior.
- "Set up Brevo Helper authentication" triggers onboarding behavior.
- "Connect this form to Brevo" triggers site integration behavior.
- "Review this campaign before I send" triggers campaign QA behavior without sending.
- Every workflow ends with manual dashboard steps when Brevo action is required.

## Phase 4: Backend Integration Templates

Status: complete

Goal: Provide reusable backend patterns for projects that need Brevo form/event submission.

Added:

- Cloudflare Pages Functions.
- Static HTML plus serverless endpoint.
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

Added files:

- `examples/cloudflare-pages-function/`
- `examples/static-html-plus-serverless/`
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

Status: complete

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

Added:

- `docs/drip-campaign-workflow.md`
- `docs/drip-campaign-playbooks.md`
- `examples/drip-campaign-brief/welcome-sequence.md`
- `examples/drip-campaign-brief/quote-follow-up.md`
- `plugins/brevo-helper/skills/brevo-drip-builder/references/drip-playbooks.md`

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

Status: complete

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

Added:

- `docs/campaign-qa-workflow.md`
- `docs/campaign-qa-scorecard.md`
- `examples/campaign-qa-report/template-readiness.md`
- `plugins/brevo-helper/skills/brevo-campaign-qa/references/readiness-scorecard.md`

## Phase 7: Project-Specific Website Integration

Status: in progress, blocked on first target project path

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

Added:

- `docs/project-integrations.md`
- `docs/project-integration-intake.md`
- `examples/form-schema/lead-capture.schema.json`
- `plugins/brevo-helper/skills/brevo-site-integration/references/integration-intake.md`

Acceptance criteria:

- A real form can submit to the backend.
- Backend can create/update Brevo contact in the intended list.
- No Brevo secret appears in frontend code.
- User can finish any required Brevo dashboard setup manually.

## Phase 8: Verification And Test Harness

Status: in progress

Goal: Make plugin behavior and examples testable.

Done:

- Add JSON validation script for plugin and marketplace files.
- Add install smoke-test checklist.
- Add MCP auth smoke-test checklist.
- Add "no direct send" review checklist.
- Add release checklist.
- Add endpoint tests for the Cloudflare Pages Function template.
- Add endpoint tests for Cloudflare Worker, Next.js route handler, Express, and static HTML plus serverless templates.
- Add a repo-level example test runner.
- Add markdown link checker.
- Add the local marketplace source with `codex plugin marketplace add`.
- Add the GitHub marketplace source with `codex plugin marketplace add`.
- Refresh the GitHub marketplace cache with `codex plugin marketplace upgrade`.
- Add release preflight script.
- Add GitHub Actions validation workflow.
- Add backend integration stub generator tests.
- Add Brevo MCP initialize smoke-test script for live read endpoints.

Remaining tasks:

- Install the plugin from the Codex app UI and verify bundled skills load.

Added files:

- `scripts/validate_plugin.py`
- `docs/testing.md`
- `docs/release-checklist.md`
- `examples/cloudflare-pages-function/test/brevo-lead.test.mjs`
- `examples/cloudflare-worker/test/index.test.mjs`
- `examples/nextjs-route-handler/test/route.test.mjs`
- `examples/express-endpoint/test/brevoLead.test.mjs`
- `examples/static-html-plus-serverless/test/brevo-lead.test.mjs`
- `scripts/test_examples.py`
- `scripts/create_integration_stub.py`
- `scripts/test_integration_generator.py`
- `scripts/check_markdown_links.py`
- `scripts/release_preflight.py`
- `scripts/smoke_brevo_mcp.py`
- `.github/workflows/validate.yml`

Acceptance criteria:

- `python3 scripts/validate_plugin.py` validates required plugin files.
- README install instructions are tested.
- No bundled MCP server includes campaign send/schedule management by default.
- Roadmap and README stay aligned.

## Phase 9: Documentation And Distribution

Status: in progress

Goal: Make the plugin understandable and installable by another Codex user.

Done:

- Add release checklist.
- Add release status doc.
- Expand README quickstart.
- Add `docs/onboarding.md`.
- Add `docs/brevo-token-setup.md`.
- Add `docs/no-direct-send-policy.md`.
- Add `docs/drip-campaign-workflow.md`.
- Add `docs/campaign-qa-workflow.md`.
- Add `docs/site-integration-workflow.md`.
- Add changelog.
- Add project integration tracker.
- Add form schema fixture.
- Add attribute mapping guide.
- Add analytics review workflow.
- Add CLI smoke-test examples for marketplace refresh and release preflight.

Remaining tasks:

- Add screenshots after local app install works.
- Tag releases.

Acceptance criteria:

- New user can install from GitHub with one command.
- New user understands how to set `BREVO_MCP_TOKEN`.
- New user understands that sends and activation happen in Brevo, not Codex.
- Releases have clear version notes.

## Phase 10: Optional Advanced Features

Status: future

Possible features:

- CLI helper that generates backend endpoint stubs from selected runtime. Added `scripts/create_integration_stub.py`.
- Attribute mapping assistant that compares local form fields to Brevo contact attributes.
- Drip copy style profiles for different projects. Added `docs/copy-style-profiles.md`.
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

- Backend templates for common runtimes. Added Cloudflare Pages Functions, Cloudflare Workers, Next.js route handlers, Express, and static HTML plus serverless.
- Validation script. Added `scripts/validate_plugin.py`.
- Install smoke-test docs. Added `docs/testing.md`.
- Project-specific integration notes.
- Form schema fixture. Added `examples/form-schema/lead-capture.schema.json`.
- Example drip campaign output. Added `examples/drip-campaign-brief/welcome-sequence.md`.
- Reusable drip campaign playbooks. Added `docs/drip-campaign-playbooks.md`.

Could have:

- Reusable form schema examples. Added `examples/form-schema/lead-capture.schema.json`.
- Attribute mapping examples. Added `examples/attribute-mapping/website-lead.md`.
- Analytics review templates. Added `examples/analytics-review/campaign-summary.md`.
- Copy style profile examples. Added `examples/copy-style-profiles/warm-professional.md`.
- Screenshot-based docs after the plugin is installed.

Won't have by default:

- Direct Brevo send/schedule/launch tools.
- Live automation activation from Codex.
- Contact enrollment into live automations from Codex.
- Client-side Brevo API keys.
- Official Brevo branding or logo unless explicitly authorized.

## Open Decisions

- Which real project should be the first integration target?
- Should we create a direct `docs/` guide for Phresh Start once the first project is confirmed?
- Do we need a private internal branch for higher-permission Brevo workflows, or should this repository stay strictly no-send?

## Near-Term Build Order

1. Done: Add validation script for plugin JSON and required files.
2. In progress: Add marketplace source and install/load-test plugin from Codex.
3. Set `BREVO_MCP_TOKEN` and verify read-only Brevo MCP tools.
4. Done: Build backend integration templates.
5. Use the plugin on the first real project form.
6. Done: Add drip campaign example output and reusable campaign playbooks.
7. In progress: Add release checklist and tag `v0.1.1`.
