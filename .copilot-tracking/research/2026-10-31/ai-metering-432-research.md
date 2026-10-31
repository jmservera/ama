<!-- markdownlint-disable-file -->
# Task Research: ai-metering-432

| Field | Value |
| --- | --- |
| Date | 2026-10-31 |
| Researcher | RPI Agent / rpi-research |
| Status | Complete |
| Artifact path | .copilot-tracking/research/2026-10-31/ai-metering-432-research.md |

## Research Brief

* Research the remaining acceptance criteria of #432 after verifying merged work.
* Purpose: source-only extension of the existing AI cost ledger; evidence for maintainers and the capstone pitch.
* Scope: src/core, src/agents, src/api, directly related documentation and local synthetic tests.
* Non-goals: deployment, Azure access, credential files, private datasets, paid inference, mvp code, owner or Finance approval.
* Criteria: attributable calls, bounded dispatch, honest Unknown economics, quality-aware accepted-outcome reporting and explicit operational gaps.
* Requested outputs: research, plan, implementation, independent review and evidence-bearing Refs #432 PR.
* Output mode: convergence.

## Research Parameters

| Field | Value |
| --- | --- |
| Questions | What already exists? Where do calls bypass it? What can be delivered without spend/billing authority? |
| Codebase scope | Existing src ledger, model adapters, dispatch and reports |
| External scope | Issue/merged PR evidence; official public pricing only if needed |
| Initial internal areas | core ai/assistants, agents dispatch/chat, API ledger and tests |
| Initial external areas | #432, merged #433 |
| Posture | focused; bounded caller scope |
| Explicit limits | pip only; no secrets, Azure changes, deployment, main edits or other worktrees |
| Completion basis | Material criteria covered with explicit missing financial/approval evidence |
| Research edits | Evidence only |
| Resolved evidence root | .copilot-tracking/research/2026-10-31 |

## Extension Registry and Provenance

| Kind | Candidate | Provenance | Disposition |
| --- | --- | --- | --- |
| Instructions | Repository guidance | Supplied applyTo ** | Selected; source layout, branch and full publication gate |
| Skill | rpi-research | RPI lifecycle | Selected; three-wave evidence |
| Specialist | RPI Researcher | Registered agent | Skipped; tightly coupled code trace is handled inline |
| Skill | Web guidelines | Repository web policy | Conditional on web edits; no visual redesign intended |

## User Participation and Research Decisions

Intake is explicit full-loop authority in non-interactive mode. No ordinary confirmation is needed.
OD-51, live spend authority, named appointments and Finance decisions cannot be invented.

## Scope and Success Criteria

All nine issue criteria must be either delivered with local evidence or recorded as an unmet operational criterion.
No closing keyword is permitted in the PR.

## Task Research Requests

Read #432 first; check merged work before implementing; extend rather than replace the ledger.
Run requested API unittest and Ruff commands, exercise changed behaviour locally, retain original critique and Review.

## Direction Controls

Source-only changes on the already clean feat/ai-metering-432 branch, based on
origin/main 5666bd33e1827670e5c07e3e3063bbbe989b59d3. No existing PR for this branch.

## Research Questions

| ID | Question | Type | Status |
| --- | --- | --- | --- |
| Q1 | What does merged work cover? | straightforward | Answered in part |
| Q2 | Which calls and controls remain unmetered? | depth | Open |
| Q3 | How can financial/quality reporting preserve Unknown and approvals? | depth | Open |

## Prior Knowledge Gate

#433 merged on 2026-10-23, requirements and pitch documentation only.
The issue comment explicitly leaves all criteria unticked. Current code must be checked
because later chat/resident work may change the earlier coverage description.
Required case-study documents, reference index, memory and sector primer read.

## Research Cycle Log

### Cycle 1

#### Wave 1: Wider

Initial search found dispatch/chat usage paths and no cost-named file.
Prioritized the actual ledger implementation rather than assuming the issue's older inventory is current.

#### Wave 2: Deeper

The existing ledger is assistant_events/assistant_attempts/assistant_allowance
(C4), with serializable transactions and immutable events. It reserves tokens,
but does not price them. Unknown usage retains its reservation yet permits
later calls. Ai._chat discards usage (C5); chat now retains turn tokens (C6).
The resident path has a later merged conservative currency reservation (C7),
so the issue's original inventory is stale on that point.

#### Wave 3: Contrarian

Challenged both "no existing money limit" and "tokens imply financial cost".
#480 and #593 already deliver resident procedure-based reservation, but not
complete cached-token/configuration/output provenance or billing reconciliation.
Unknown cached tokens cannot be assumed zero for pricing. Images have no
provable token upper bound from character count. Late or failed calls can still
be billed, so retain liability and stop further dispatch rather than refunding.
Existing fake-provider contracts remain synthetic evidence, not live authority.

#### Parent Synthesis and Disposition

Accept extension of assistant_events for immutable consumption/price/spend/billing
records and the existing serialized transaction boundary. Reject a parallel cost
database, inferred cash savings, hardcoded deployment price or presumed authority.
Preserve existing resident SQL controls; source-only metering does not change its
deployed procedures. Explicitly report resident legacy-accounting coverage as a gap
until the composed financial ledger is supplied.

#### Cycle Re-entry Evaluation

No new cycle needed: bounded source trace establishes implementation contracts.
Actual price applicability, billing and spend/quality decisions require owner
evidence, not more source discovery. Planning is ready for source-only engineering.

## Evidence Log

| ID | Finding | Location | Confidence |
| --- | --- | --- | --- |
| W1 | All nine criteria open; OD-51 and spend authority unresolved | https://github.com/jmservera/ama/issues/432; retrieved 2026-10-31 | High |
| W2 | #433 delivered documentation, not metering | https://github.com/jmservera/ama/pull/433; merged 2026-10-23, retrieved 2026-10-31 | High |
| C1 | Current economics gaps and partial usage inventory | docs/reference/resources/ai-tokenomics.md:87 | High for dated documentation; verify source |
| C2 | Pitch requires explicit Unknown and evidence labels | docs/capstone/pitch/tokenomics-pitch-brief.md:80 | High |
| C3 | Full local gate required for runtime publication | src/README.md:78 | High |
| C4 | Existing SQL append-only events, token allowance and serialized claims/completions | src/core/src/zava_forward/core/assistants.py:340,409,782,858 | High |
| C5 | Legacy text/image calls discard usage | src/core/src/zava_forward/core/ai.py:60,113,142 | High |
| C6 | Chat retains usage and metadata-only audit, no price/complete effort | src/core/src/zava_forward/core/chat_panel.py:341,451 | High |
| C7 | Resident accounting already precommits one cent per request, no refund | src/api/src/zava_forward/api/resident_demo/aoai.py:27,341 | High |
| C8 | Legacy output and review records have stable record IDs | src/core/src/zava_forward/core/ai_tasks.py:229,337 | High |

## Findings Mapped to Questions and Evidence

Q1: requirements-only #433 is verified (W2); later runtime delivery remains to inspect.

## Key Discoveries

Unknown financial evidence must not be replaced with invented prices, authorised budgets or acceptance.

## Alternatives and Decision State

Extend immutable assistant events with content-free financial admission and
reporting; wire Ai and proposal output/review links. Enforce finite request
calls/depth and stop unknown liability/price without weakening manual routes.
Use an offline recording interface for owner-supplied evidence, not a new
deployment or implied financial approval. Report every uncovered historical
or independent resident path explicitly.

## Open Questions, Risks and Residual Uncertainty

Actual Azure billing, dated deployment prices, OD-51 and owner-authorised held-out batch remain unavailable.

## Current Decisions

Preserve workflow-only, resident/human approvals and safety clocks; do not call a paid provider.

## Potential Next Research

Actual model call boundaries and append-only ledger semantics.

## Planning Readiness

Ready for source-only implementation; Research disposition: executed.
Operational criteria remain blocked by OD-51, applicable price/billing and
held-out spend authority. No whole-issue acceptance is inferred.

## Sources and Self-check

Issue and merged PR retrieved with gh. No credential files or private datasets read.
Three inline waves completed in order; no worker or live provider ran.
