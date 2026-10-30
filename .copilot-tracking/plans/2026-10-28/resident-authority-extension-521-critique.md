---
title: Resident demo authority extension independent plan critique
description: Single final-candidate critique for issue 521
ms.date: 2026-10-28
---

## Metadata

* Task ID: 521.
* Critique date: 2026-10-28.
* Branch: chore/resident-authority-extension-521.
* Plan: .copilot-tracking/plans/2026-10-28/resident-authority-extension-521-plan.md.
* Phase details: .copilot-tracking/details/2026-10-28/resident-authority-extension-521-phase-details.md.
* Critique execution status: Complete.
* Assessment: one independent final-candidate assessment; no additional workers.

## Inputs and Criterion Boundary

* Caller direction: full ordered RPI; source-only extension through January 31
  UTC; no Azure, any az invocation, secrets, .env, source edits or additional
  workers during this critique. Write only this artifact and stop.
* Supplied research: .copilot-tracking/research/2026-10-28/resident-authority-extension-521-research.md,
  C1-C8, including its named source, test, operations and gate pointers.
* Required context considered: docs/case_study_48_original.md,
  docs/case_study_48_addendum.md, docs/reference/README.md and
  docs/reference/memory.md. Memory is context, not authority.
* Source evidence inspected within those pointers: packaged runtime authority,
  resident Bicep, secret/deploy helpers and their tests, SQL template/renderer,
  core SQL/domain tests, real-loopback API tests, component guides and the
  publication runner. No open-ended or external research was performed.
* Decisions and acceptance criteria: shared 2027-02-01T00:00:00Z maximum
  configuration expiry and exclusive serving end; all existing admission,
  per-row, session, isolation, provenance, principal, private-path and what-if
  guards retained; no row renewal or independent inference tariff extension;
  no test removals and at most eight added test methods; USD700 all-in ceiling;
  separate owner approval for live operations; mandatory publication gate.
* Assessment boundary: correctness and coverage of the proposed plan, not an
  implemented diff, SQL execution result, deployment acceptance or spending
  authorization. Publication blocking under no-az is explicitly accepted.

Input fingerprints at assessment:

| Input | SHA-256 |
| --- | --- |
| Plan | 529519eef4d20e4c972138ea064dcb9f1fb6a3b749bf406efd30af02f8679176 |
| Phase details | 2690f68dfd54a9469efc2d0a9c603d0b32c9e3857ae499029361ef4471ee5540 |
| Research | d127b2b7f8d62d0ca38a81a59e6054e617283272f9b0e88e7cf2b0dda3308ef1 |

## Coverage Assessment

| Requirement, research, phase, or task ID | Coverage | Evidence or concern |
| --- | --- | --- |
| C1-C2; shared authority and inclusive configuration maximum | Covered | Existing JSON, runtime import, Bicep load and helper alias form a coherent single source; fixed target date and over-limit checks are planned. |
| C3-C4; P01-T01; existing SQL migration | Partial | Transaction, WITH CHECK and rollback design are appropriate; acceptance evidence does not yet distinguish successful reapply from failed-migration restoration (PC-002). |
| P01-T02; serving/session boundary and unchanged guards | Covered | Constructed rows, fake clock and real loopback HTTP are planned alongside existing guard suites; SQL-specific evidence needs PC-002. |
| C5-C6; P02-T01; independent live and inference expiries | Covered | Source cap does not renew SQL rows, vault expiry, deployed image/configuration or model admission. Historical decisions remain historical. |
| C8; P02-T01; rotation and cost | Covered | Modify refusal, version overlap, session invalidation, private operation approval, conditional cost assumptions and all-in headroom check are explicit. |
| P02-T02; no-az validation | Partial | Avoiding compiled-template classes alone misses a compiled call inside CommandTests (PC-001). |
| P03-T01; independent Review and immutable adverse evidence | Covered | One fresh Review and original outcome preservation are explicit; no repeated critique is needed. |
| C7; P03-T02; exact-head publication prerequisites | Partial | Full gate blocker is correctly retained; the final fetch/verification/independent exact-head assessment sequence is incomplete (PC-003). |
| Test ownership and maximum additions | Covered with correction | Existing owner suites and eight-method ceiling are explicit; resolve PC-002 within that ceiling, without removing tests. |

## Verdict

* Verdict: Revise.
* Severity counts: 0 Critical, 1 High, 2 Medium, 0 Low.
* Rationale: the shared authority design and source-only approval boundary are
  credible. Three actionable planning gaps remain: a prohibited subprocess
  reachable from a nominally permitted suite, insufficiently explicit SQL
  migration proof, and an incomplete publication closeout sequence.
* This is the complete actionable PC-xxx set for the supplied boundary.
  Publication remains blocked independently of these planner corrections.

## Findings

<!-- rpi:critique id=PC-001 -->
### PC-001 [High]: The proposed no-az suite exclusion misses a direct compiled call

* Related IDs: P02-T02; no-Azure/no-az requirement; helper validation acceptance.
* Evidence: phase details P02-T02 says to avoid compiled-Bicep test classes.
  In infra/tests/test_resident_demo_deploy.py, TemplateTests.setUpClass calls
  compiled(), but CommandTests.test_compiled_inventory_including_guard_passes_and_unknown_nested_is_refused
  also calls compiled() directly. That function executes az bicep build.
* Concern: excluding TemplateTests while selecting CommandTests, or using
  ordinary infra discovery, can still run the explicitly forbidden command.
  The file's fake-CLI description does not establish that every test is
  offline under this request.
* Impact: a plausible execution of the current validation plan violates a
  confirmed user restriction, even without authenticating to Azure.
* Smallest useful change: specify the permitted existing test selectors before
  execution. Exclude both TemplateTests and the named CommandTests method;
  inspect any wider selected suite's subprocess paths before running it.
  Record their unperformed coverage explicitly. Do not remove tests, replace
  compilation with a claimed equivalent, invoke az to probe availability or
  weaken the complete publication gate.
* Action owner: planning parent; implementation executor applies the selectors.
* Exact resolving evidence: revised P02-T02 contains concrete selectors and
  names both exclusions. Execution evidence lists actual selected test IDs,
  exits and omitted compiled checks, with no az invocation. Existing fake-CLI
  expiry, rollback and what-if refusal checks still run where permitted.
* Decision route: Direct planner correction. No user response is required;
  the prohibition already resolves the tool choice.

<!-- rpi:critique id=PC-002 -->
### PC-002 [Medium]: Migration acceptance does not explicitly prove rollback, trust and preservation

* Related IDs: C3-C4; P01-T01; P01-T02; SQL acceptance criteria.
* Evidence: infra/sql/resident-showcase.sql currently creates
  ck_allowed_case_window only with a new table and includes both
  valid_to > valid_from and its old upper bound.
  infra/scripts/resident_showcase_sql.py renders GO-separated batches, and
  its apply connection uses autocommit=True. Existing
  src/core/tests/test_resident_showcase_sql.py covers fresh creation, principal
  denials and the old cap, but not constraint replacement or rollback.
  Phase details promises transactional replacement and rollback, while the
  test task says only "new/old existing SQL constraints" and treats real SQL
  migration coverage as optional.
* Concern: renderer token/date assertions and a successful legacy migration
  do not prove rollback after dropping the old constraint, an enabled/trusted
  replacement, idempotent reapply, or preservation of rows and other guards.
  This is a missing acceptance contract, not evidence that the proposed
  transaction is itself incorrect.
* Impact: the source change could appear complete while a deployed table keeps
  the old cap, a failed replacement leaves altered protection, or an unchecked
  replacement admits invalid windows.
* Smallest useful change: add an explicit migration assertion matrix to
  P01-T02 and the acceptance criteria:
  * Fresh creation and an existing November-limited named constraint both
    produce the same rendered shared cap, retaining valid_to > valid_from.
  * A second reapply succeeds without changing existing row values, revocation
    flags, provenance checks, view isolation or principal permissions.
  * Check sys.check_constraints for the replacement's enabled/trusted state;
    verify cap equality succeeds and one second later, a reversed window and
    blank provenance fail.
  * An invalid legacy-data fixture, deliberately established only in the owned
    disposable database with an absent or disabled historical check, makes
    WITH CHECK fail. Verify the exception propagates, no transaction remains
    open, row values are unchanged and any prior named constraint definition
    and enabled/trusted state are restored to their pre-attempt state.
  * Keep drop/add/commit and rollback handling in one rendered batch so the
    existing autocommit/batch executor does not expose a committed gap.
* Action owner: planning parent defines acceptance; implementation executor
  supplies assertions in the existing SQL owner suite.
* Exact resolving evidence: revised task details map these assertions to
  existing methods or a bounded addition list. For example, one successful
  legacy/reapply method and one rollback method plus the planned HTTP method
  use three additions; extend existing fresh/renderer/guard tests rather than
  duplicating them. Actual SQL proof requires recorded successful runs against
  the approved owned-loopback fixture. If that cannot run within the no-secrets
  and other restrictions, record the SQL assertions as unverified, not passed;
  retain the mandatory gate/publication blocker. No secret access is requested.
* Decision route: Direct planner correction. No new authority, test removal,
  more than eight additions or significant user decision is necessary.

<!-- rpi:critique id=PC-003 -->
### PC-003 [Medium]: The publication task omits the final independent exact-head assessment

* Related IDs: C7; P03-T01; P03-T02; publication acceptance.
* Evidence: src/README.md, Local RPI gate, requires another main fetch and
  receipt verification immediately before independent exact-head review and
  push; changed head/base or dirty inputs invalidate evidence. The plan
  schedules original independent Review, then commit/gate/verification/push.
  P03-T02 does not explicitly schedule the final independent exact-head
  assessment or the final refetch and invalidation response.
* Concern: original pre-commit RPI Review and a full receipt are not, by
  themselves, the complete publication authorization chain. A future executor
  could follow the task list and push without the final assessment or against
  a moved origin/main.
* Impact: even a genuinely available complete receipt could be used outside
  the repository's exact-head/current-base publication requirements.
* Smallest useful change: make the conditional publication sequence explicit:
  preserve original Review; commit the final source and dated evidence; obtain
  the required complete exact-head receipt only under permitted tools; refetch
  main; verify that external receipt against current origin/main and clean,
  unchanged HEAD; obtain the independent exact-head assessment; only then
  push once and create the PR with Refs #521. Stop if head/base/inputs changed
  or either assessment or verification is unavailable. This final assessment
  is distinct from repeating or overwriting the original RPI Review.
* Action owner: planning parent and publication executor.
* Exact resolving evidence: P03-T02 names this order, assessment evidence and
  invalidation stop conditions. Under the current prohibition, the closeout
  explicitly records full gate/publication Blocked and no push/PR; it does not
  run tools/rpi-checks.py --all, whose preflight invokes az bicep version.
  No alternate/partial receipt is accepted as full coverage.
* Decision route: Direct planner correction. The current task needs no user
  response. Any later change in live/tool authority is a separate owner
  decision, not a prerequisite to completing source-only work.

## Strengths and Residual Risk

* The existing packaged policy is the appropriate source of truth.
  AUTHORITY_END in Python, the Bicep JSON load and helper aliases already share
  it. Rendering a whole-second UTC SQL value from that authority avoids a new
  executable date copy. The planned transaction retains the full window
  predicate; WITH CHECK, XACT_ABORT and rollback/rethrow are the right design
  direction. No separate correctness defect in that design is established.
* Maximum accepted configuration expiry may equal 2027-02-01T00:00:00Z while
  serving and sessions deny at that instant. This is coherent, not an
  off-by-one conflict. The January 31 final-second HTTP test must use a
  January-valid row and configured service/session expiry at the new cap,
  rather than the existing October fixture's six-hour expiry.
* Rotation appropriately remains a separately approved exact-operation plan:
  preserve SID/permissions/private access, maintain deliberate version overlap
  and session invalidation, and do not broaden the new-secret-only helper's
  Modify refusal. No live rotation was authorized or performed.
* Cost wording distinguishes zero incremental resources/actions in this
  source-only change from ongoing resource charges. The USD30 historical
  resident allowance is not renewed funds or a tariff; the longer-window
  estimate must stay assumption-labelled. Unknown actual/delayed liabilities,
  reserve, remaining-resource costs and January funding keep paid action
  blocked under the USD700 all-in ceiling.
* Existing SQL row windows, vault-secret expiries and deployed images remain
  independent. No automatic renewal, production identity acceptance, new
  minimum replicas or extension of inference tariff/ledger authority is
  implied.
* The no-az/full-gate incompatibility is accepted and correctly retained as a
  publication blocker. It is not a request for permission to invoke az.

## Questions or Blocking Evidence Gaps

* No unresolved significant/divergent user decision blocks the planner-owned
  corrections or the source-only implementation.
* Real SQL execution evidence, fresh all-in headroom and live renewal remain
  unavailable at this plan assessment boundary. They must not be inferred
  from source inspection, mocks or optional-test skips.
* Publication remains Blocked unless every unchanged repository prerequisite
  can genuinely be satisfied within confirmed authority. Current no-az
  direction does not permit obtaining a new complete gate receipt.

## Limitations

* This was a bounded read-only plan critique, not an implementation review.
  No application tests, SQL, build, gate, Azure command, secret/.env read,
  installation, live cost query or remote operation was run.
* Existing untracked plan/research/session files were left in place. Only the
  requested critique artifact was written; no plan, details, research, source
  or prior outcome was edited.
* No new legal, operational, pricing or cloud state claim is established.

## Recommended Next Action

* Highest-impact finding: PC-001.
* Action owner: planning parent.
* Smallest next action: correct the no-az test selection, then directly
  disposition PC-002 and PC-003 in the final plan/details before implementation.
* User response required: No.
* Preserve this original Revise verdict. Finalize by direct disposition, not a
  second critique. No other RPI stage is invoked by this assessment.

## Artifacts

| Artifact | Description |
| --- | --- |
| [.copilot-tracking/plans/2026-10-28/resident-authority-extension-521-plan.md](.copilot-tracking/plans/2026-10-28/resident-authority-extension-521-plan.md) | Assessed plan, unchanged |
| [.copilot-tracking/details/2026-10-28/resident-authority-extension-521-phase-details.md](.copilot-tracking/details/2026-10-28/resident-authority-extension-521-phase-details.md) | Assessed phase details, unchanged |
| [.copilot-tracking/research/2026-10-28/resident-authority-extension-521-research.md](.copilot-tracking/research/2026-10-28/resident-authority-extension-521-research.md) | Supplied C1-C8 evidence |
| [.copilot-tracking/plans/2026-10-28/resident-authority-extension-521-critique.md](.copilot-tracking/plans/2026-10-28/resident-authority-extension-521-critique.md) | Complete independent critique; Revise |

## Next Steps

Return to the active planning parent for direct correction and disposition of
PC-001 through PC-003, without another critique or user confirmation. Preserve
the current publication blocker. This assessor stops after this single
critique; no user action is required.
