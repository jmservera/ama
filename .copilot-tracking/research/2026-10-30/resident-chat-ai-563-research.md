<!-- markdownlint-disable-file -->
# Task Research: resident-chat-ai-563

## Research Brief

Date: 2026-10-30. Status: Complete. Research disposition: executed.
Task ID: issue-563. Output mode: convergence. Audience: implementer and owner.
Find why consented resident questions never reach AI, then prepare a bounded
source fix with honest fallback, grounding, thin labels and collapsed sources.

## Research Parameters

Focused posture, selected for the caller's named failure and source targets.
Evidence root: .copilot-tracking/research/2026-10-30/.
Internal candidates: src/api, src/agents, src/core, public infra configuration,
PR #562 and the caller-supplied sibling acceptance artifact.
External candidates: Web Interface Guidelines and Microsoft Teams AI labels.
No secrets, .env, private datasets, Azure operations, push or issue closure.
Source edits are prohibited during Research.

## Extension Registry and Provenance

Repository instructions apply throughout. rpi-research selected for research;
web-design-guidelines selected for the UI; Fluent 2, WCAG and content standards
take precedence over generic aesthetics. Design overhaul skills skipped:
this is an existing-app functional repair, not a redesign. Independent specialist
research skipped: one tightly coupled routing trace is best followed inline.

## User Participation and Research Decisions

Explicit full-loop request authorizes automatic progression for this task.
No routine questions needed; local-only commit and no deployment are explicit.
Clean topic branch feat/resident-chat-ai-563 matches the work, tracks main,
has no PR, and starts at 7c131156. PR #562 is evidence-only, not a code dependency.

## Direction Controls

* Source in src/; tests outside package directories; no mvp feature additions.
* Preserve consent, own-record projection, human authority and inability route.
* Local unit/ruff/mypy/browser evidence; live acceptance remains unproven.

## Research Questions

Q1: Which configuration or routing branch prevents resident model execution?
Q2: How can free text be answered without inventing record facts or authority?
Q3: What UI changes and tests prove labels, sources and explicit fallback?

## Prior Knowledge Gate

Read original/addendum, reference index and memory. Issue #563 and PR #562
confirm rules-only live observations, not the cause. The sibling acceptance
record preserves authenticated live evidence and explicitly lacks AI proof.

## Research Cycle Log

### Cycle 1

#### Wave 1: Wider

Read startup, API dispatch, core advisor contracts, existing provider/HTTP/browser
tests, shared widget and public deployment template. C2-C6 establish two independent
code limitations and a third configuration prerequisite. Reflection: enabling a
setting alone cannot fix repair questions.

#### Wave 2: Deeper

Traced consent and session binding before record lookup, own-case projection,
durable reservation before token/HTTP, output schema and post-inference
revocation check. Read Fluent, WCAG and plain-content standards. Retrieved the
current Web Interface Guidelines and official Teams label pattern (W1-W2).
Reflection: reuse the existing accounting/transport and UI; introduce a bounded
generated-answer contract, not another AI client or conversation store.

#### Wave 3: Contrarian

Challenged a config-only fix: unknown routes never invoke the advisor, and even
enabled fixed-topic calls select prewritten sentence IDs. Rejected enabling AI
by default: public Bicep omits the explicit activation settings, but actual Azure
configuration is uninspected and the reviewed tariff/access gates still apply.
Checked transport Authorization structurally against Bearer-token syntax (true);
it is not the source defect. Preserve deterministic safety/legal/consent/action
routes and out-of-scope refusal. Prompt grounding and source validation cannot
prove semantic correctness; real-model evaluation and human approval remain gates.
No further cycle needed: material source paths and contracts are established.

## Evidence Log

C1: Issue #563, PR #562 and caller-supplied sibling changes artifact establish
the reported symptom; retrieved with gh/read on 2026-10-30.

| ID | Finding | Source |
| --- | --- | --- |
| C2 | Free text is reduced to host topics; rat question is unknown | src/api/src/zava_forward/api/resident_demo/chat.py:145 |
| C3 | Only Topic instances call an advisor; strings always use rules | src/api/src/zava_forward/api/resident_demo/app.py:405 |
| C4 | Enabled advisor selects guidance IDs, never writes prose | src/api/src/zava_forward/api/resident_demo/aoai.py:133 |
| C5 | Explicit managed-identity factory defaults off | src/api/src/zava_forward/api/resident_demo/aoai.py:257 |
| C6 | Deployment template supplies SQL but no assistant activation | infra/resident-demo.bicep:140 |
| C7 | Consent precedes row lookup; late replies recheck authority | src/api/src/zava_forward/api/resident_demo/app.py:380 |
| C8 | Shared widget already renders escaped text and collapsed details | src/api/src/zava_forward/api/web/chat-widget.js:100 |
| C9 | Legacy contract intentionally excludes raw questions | src/core/src/zava_forward/core/resident_assistant.py:1 |
| W1 | Small AI Generated header label; incorrect-content disclosure | https://learn.microsoft.com/en-us/microsoftteams/platform/agents-in-teams/integrate-ai/ai-content-labels, retrieved 2026-10-30 |
| W2 | Native semantics, focus, polite updates, reduced motion and wrap rules | https://raw.githubusercontent.com/vercel-labs/web-interface-guidelines/main/command.md, retrieved 2026-10-30 |

## Findings, Alternatives and Decision State

Selected: bounded generated prose for consented in-scope free text, using only
its own projected answer/progress, host-owned source IDs and repair-reporting
guidance. Keep legacy fixed-topic API behavior. Keep protected routes rules-only.
Reject config-only and topic-ID-only fixes (C2-C4). Keep default-off activation,
expiry, rate/cost reservation and managed identity (C5); record owner settings,
not an unverified claim about live configuration. Generated text must be escaped,
labelled AI-generated and unapproved, with honest inability/human help retained.

## Risks and Residual Uncertainty

No secrets/.env/private datasets read; no Azure inspection or paid model call.
Local scripted transport proves routing/schema/UI, not actual-model quality.
Current tariff expires 2026-11-01; no authority extension is in scope. Missing
live authenticated evidence leaves issue acceptance incomplete. Local source
distributions were missing in /tmp/mv; installed pinned projects/dev tools in
the external task-owned runtime rather than mutate the shared environment.

## Self-check

Three waves completed inline. Claims have stable evidence pointers, alternatives
were challenged, explicit limits retained. Research disposition: executed.

## Planning Readiness

Ready for bounded implementation planning (C2-C9, W1-W2).
