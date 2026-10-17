<!-- markdownlint-disable-file -->
# Review: setup-profile-evidence-360

## Scope and Evidence

* Task ID: issue-360-followup
* Task slug: setup-profile-evidence-360
* Review date: 2026-10-17
* Review scope: full task's source/test/documentation boundary; delivery still pending.
* Assessed boundary: resource-bound profile contract, refusal/neutral/default behavior, required regression/compatibility evidence, runbook and RPI reconciliation. No live setup acceptance.
* Plan: .copilot-tracking/plans/2026-10-17/setup-profile-evidence-360-plan.md
* Phase details: .copilot-tracking/details/2026-10-17/setup-profile-evidence-360-phase-details.md
* Plan critique: .copilot-tracking/reviews/plans/2026-10-17/setup-profile-evidence-360-plan-critique.md
* Changes: .copilot-tracking/changes/2026-10-17/setup-profile-evidence-360-changes.md
* Research: .copilot-tracking/research/2026-10-17/setup-profile-evidence-360-research.md

## Opening Review State

* Goal: assess implemented classification once against all owner safety requirements.
* Scope: completed P01/P02, critique disposition and P03 delivery readiness.
* Evidence readiness: dated artifacts reconciled, 200 combined tests passed, four unsafe mutations killed.
* Acceptance basis: current plan requirements and source-only owner boundaries.
* First comparison: source resolver and negative matrix, followed by docs/artifacts.
* Active boundary: read-only comparison; write only this canonical review record.
* Initial blockers: none for source review; live credential/publication gates excluded and unmet.
* Delegation: none; bounded change can be reviewed directly.

## Execution Status

* Execution status: Complete.
* Evidence: direct source/test/doc and canonical artifact comparison, plus a
  fresh combined 200-test execution during this one Review.
* This is the only post-implementation Review; it is not independent coordinator
  acceptance and must not be described as such.

## Plan-to-Change Reconciliation

| Plan scope | Changes evidence | Assessment |
| --- | --- | --- |
| P01-T01 | Installed baseline and failing-first actual shape | Reconciled; 104+43 fresh baseline, original actual-shape failure |
| P01-T02 | Contract-aware resource-bound classification | Reconciled; actual export/default resolution replaces heuristic |
| P02-T01 | Validation and durable runbook finding | Reconciled; 13 added methods, complete named suites, refusal matrix |
| P02-T02 | Runbook, existing index route and appended log | Reconciled; no broader acceptance/history rewrite |
| P03-T01 | This one Review | Executed; parent owns completion marker after return |
| P03-T02 | Commit/push/main PR | Still pending at review time; not claimed complete |

## Completed Work Assessment

* infra/scripts/setup-entra.py: only classifier and its narrow helper changed.
  Azure wrapper still scopes deployment commands to selected subscription;
  export is fixed to ama and exact list-returned bound deployment name.
* ARM declaration/value separation is correct: supplied values override that
  same parameter's default. Omitted declared literal defaults become evidence;
  missing required declarations/values and unresolved types refuse.
* Raw CLI template object is used, not REST wrapper or deployment properties.
  No current local main template or templateLink URL is used as historical truth.
* Neutral contracts add no profile. Independent app/environment and
  deploymentProfile/tags-profile evidence all remain visible; environmentName
  and tags-environment likewise cannot erase contradictions.
* Existing discovery, Graph/role/roster/admin/seed/credential/staff transport
  implementations are unchanged. Environment readback identity is now verified
  before its tags are used. No runtime cloud write is added.
* Exact outputResources matching is case-insensitive, not prefix/name matching.
  Bound non-Succeeded records refuse before export; unrelated records cannot
  authorize and are not exported.
* Test fixtures model the reported list/value/tag binding semantics and raw
  template export shape. They are fictional offline fixtures, not captured
  full live templates. Template default cases exercise the minimal relevant ARM
  contract, not a new compiled-main deployment or a fresh Azure observation.
* Runbook records added export-read prerequisite, neutral-not-approval and
  fail-closed limitations. KB log's complete original byte prefix is preserved.

## Implementation-Time Plan and Detail Update Assessment

* No material architecture/scope/intent divergence. The planned null-tags
  bound-success case was tightened, not removed or silently retained.
* Thirteen test methods stay within the locked maximum of eighteen; no test
  ownership move or generated target. Existing refused omission fixture now
  explicitly declares its real production-default meaning.
* Missing cryptography was resolved only after baseline failure using the
  existing hashed requirements; missing ruff likewise used the README pin.
* In-memory mutation-harness locator correction and changed-line formatting
  are local implementation judgments, not new user decisions or extra critique.
* Phase/checklist, changes and handoff consistently leave delivery pending.

## Critique and Material Revision Assessment

* One independent final-candidate critique executed, verdict Pass, zero findings;
  disposition recorded in plan and state.
* No incompatible critique guidance, missing required human decision or
  unjustified dependent-work resumption found.
* No second critique or post-implementation Review was run.

## Plan Follow-Up Assessment

| Follow-up | Why outside immediate scope | Owner and route |
| --- | --- | --- |
| Live credentials / initializer publication 403 | Owner explicitly limited this task to source; cloud mutation prohibited | Coordinator/platform owner, distinct authorized follow-up |
| Genuine tenant/browser/role/SQL/AI acceptance and later retirement | #360 d/e require actual live proof and separate retirement authorization | Owner/coordinator, distinct acceptance follow-up |

## Findings

No substantive source implementation defect found within this assessed boundary.

<!-- rpi:review id=RV-001 -->
### RV-001 [Medium]: Live setup acceptance remains unestablished

* Related scope: plan Follow-Up Items, not P01/P02 defects.
* Evidence: owner exclusions, infra/README.md profile follow-up and existing
  #360 live acceptance requirements; no real template export, credential
  access, initializer publication or tenant/browser/SQL/AI run performed here.
* Impact: offline parser proof cannot establish actual laptop setup success,
  export authority, publication recovery or #360 d/e completion.
* Destination: distinct follow-up, owner/coordinator and authorized platform
  operator; not a new active source implementation task.
* Smallest next action: establish permitted read-only template export and live
  credential/publication prerequisites; perform live acceptance only under
  its separate authorization. Never widen service exposure or spoof tags.

## Defects

None found within the assessed source boundary.

## Routed Findings

| Finding | Destination | Owner / reason |
| --- | --- | --- |
| RV-001 | Distinct authorized live follow-up | Owner/coordinator; unmet live acceptance, not a source defect |

No later implementation route or second Review is required by this record.
Any separately identified defect would be later work, not an alteration of
this original Review.

## Residual Work

* P03-T02 commit/push/main PR remains the current parent's delivery action.
* RV-001 and existing plan follow-ups remain outside source acceptance.
* Full repository/Bicep, Docker, SQL and Azure setup/deployment not run; none
  required for the approved parser-only boundary.
* No independent coordinator final-head approval is asserted.

## Blockers and Remaining Work

* Source/review blockers: none.
* Remaining active-plan action at review time: P03-T02 delivery.
* Live credential, publication 403 and #360 d/e remain unmet.

## Validation Evidence

| Check | Status | Evidence |
| --- | --- | --- |
| Actual-shape test on unchanged source | Failed as expected | Original Automatic demo roster refused SetupError |
| Complete setup suite | Passed | 117, including thirteen added methods/table variants |
| Complete staff_azure suite | Passed | 43; existing private/read-only transport restrictions |
| Staff initializer compatibility | Passed | 15 |
| Legacy auth delegate | Passed | 17 |
| Secret lifecycle | Passed | 8 |
| Combined during this Review | Passed | 200 tests, 5.493 seconds |
| Unsafe mutation sensitivity | Passed | All four mutations killed by focused regressions |
| README configured ruff lint/format | Passed | Three configured files, no reformat |
| Changed setup-line ruff | Passed | Zero introduced; 225 unchanged legacy diagnostics not resolved |
| compileall and diff whitespace | Passed | Both changed Python files, git diff --check |
| KB append-only prefix | Passed | HEAD bytes are exact prefix |
| Full lint/formatter on legacy setup files | Not claimed | Configured scope plus changed-line lint; avoid unrelated rewrite |
| Full repo/Bicep/Docker/SQL/Azure/live setup | Not run | Out of parser-only scope; live gates not substituted |

## Outcome

* Outcome: Residual work.
* Rationale: source-only requirements are supported with no implementation
  defect identified; delivery and separately authorized live acceptance remain.
  Do not report overall setup acceptance or coordinator Pass.

## Closeout Routing Record

| Finding class | Destination | Owner or next action |
| --- | --- | --- |
| Implementation defect | None | None identified |
| Decision gap or invalid assumption | None | None identified |
| Material in-scope evidence gap | None | Supplied fixture versus live boundary explicit |
| Non-blocking residual work | RV-001 distinct live follow-up | Coordinator/platform owner |
| Delivery | P03-T02 | Parent commits, pushes and opens main PR |

* Execution status: Complete.
* Outcome: Residual work.
* Validation coverage: complete required setup/staff plus direct compatibility,
  actual-shape failing-first, four mutation checks and scoped static checks.
* Blockers: none for source delivery; live gates remain unmet.
