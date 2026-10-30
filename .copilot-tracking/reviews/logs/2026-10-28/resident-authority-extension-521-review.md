---
title: Resident demo authority extension Review
description: Original independent post-implementation assessment for issue 521
ms.date: 2026-10-28
---

## Opening Review State

Task 521, original Review, full supplied source-only candidate.
Research, plan/details, original critique and changes share the
resident-authority-extension-521 slug and 2026-10-28 date.
Goal: assess the implemented diff and evidence against exact January boundary,
guard preservation, SQL migration, rotation/cost and publication requirements.
Independent assessor may write only this record; no source corrections,
gate execution, Azure, az, secrets or .env access.

Evidence readiness: source reviewable; required runtime/SQL/lint validation
blocked by foreign heavy-lock admission and missing packages.
Eight independent lightweight tools safety tests passed, zero skips.
Final AST/JSON/added-line lengths/relative-link targets and git diff --check
passed (exit 0) immediately before opening Review.
No full gate or publication receipt exists; no Azure apply is authorized.

## Execution Status

* Review execution status: Complete.
* Outcome: Residual work. Acceptance is withheld.
* This is the one original independent post-implementation RPI Review for
  issue #521, dated 2026-10-28. Complete describes this evidence comparison,
  not completion of implementation validation, publication or live acceptance.
* Branch: chore/resident-authority-extension-521.
* Assessed HEAD and initial base: 413ccaf253fce4566e855bae9d0a924b2a82b506.
  The candidate is the current uncommitted diff, not a committed exact-head
  publication candidate. No receipt or final publication assessment exists.
* This assessor inspected source and supplied records only. No tests,
  installation, heavy run, lock retry/poll, Azure/az command, secret/.env read,
  private dataset read, foreign run-output read or child agent was used.
  Only this review record was written.

## Scope and Evidence

The complete twelve-file tracked source diff was compared with the supplied
research, plan, phase details, original critique and changes record. The
opening facts above are preserved. Acceptance basis: the plan's requirements,
acceptance criteria, locked test ownership and PC-001 through PC-003
dispositions, within the caller's source-only restrictions.

Compared artifacts:

* .copilot-tracking/research/2026-10-28/resident-authority-extension-521-research.md
* .copilot-tracking/plans/2026-10-28/resident-authority-extension-521-plan.md
* .copilot-tracking/details/2026-10-28/resident-authority-extension-521-phase-details.md
* .copilot-tracking/plans/2026-10-28/resident-authority-extension-521-critique.md
* .copilot-tracking/changes/2026-10-28/resident-authority-extension-521-changes.md

Entire tracked diff:

* src/core/src/zava_forward/core/resident-demo.json
* infra/scripts/resident_showcase_sql.py
* infra/sql/resident-showcase.sql
* src/core/tests/test_resident_showcase.py
* src/core/tests/test_resident_showcase_sql.py
* src/api/tests/test_resident_demo_api.py
* infra/tests/test_resident_demo_secrets.py
* infra/tests/test_resident_demo_deploy.py
* infra/README.md
* src/api/README.md
* docs/reference/README.md
* docs/reference/log.md

Supporting unchanged paths inspected: src/core/src/zava_forward/core/resident_showcase.py,
src/core/src/zava_forward/core/resident_showcase_sql.py,
src/api/src/zava_forward/api/resident_demo/app.py, infra/resident-demo.bicep,
infra/scripts/resident_demo_secrets.py, infra/scripts/resident_demo_deploy.py,
infra/scripts/credential_arm.py, infra/sql/resident-assistant.sql,
src/README.md and tools/rpi-checks.py.
Repository context: docs/case_study_48_original.md,
docs/case_study_48_addendum.md, docs/reference/README.md,
docs/reference/memory.md and
docs/reference/research/sector/housing-association-primer.md.
Memory supplies context, not acceptance evidence.

## Plan-to-Change Reconciliation

| Current plan scope | Changes and current evidence | Reconciliation | Gap or rationale |
| --- | --- | --- | --- |
| P01-T01 | JSON cap, SQL renderer and existing-constraint transaction authored | Reconciled as source | No runtime or SQL execution proof; RV-001 |
| P01-T02 | Existing boundary tests updated; five methods added, none removed | Reconciled as authored coverage | Checked markers mean tests authored, not passed; RV-001 |
| P02-T01 | Infra/API guides, index and append-only log updated | Reconciled | Live renewal/funding explicitly pending, not delivered |
| P02-T02 | Unchecked; namespace import and feedback test failed; package setup and dependent validation blocked | Reconciled as incomplete | Eight lightweight tests do not satisfy this task; RV-001 |
| P03-T01 | Previously unchecked pending this original Review | Review executed by this record | Parent may record completion without altering this outcome or repeating Review |
| P03-T02 | Unchecked; commit, full receipt, current-base verification, exact-head assessment and publication unavailable | Reconciled as incomplete | No push/PR permitted; RV-002 |
| Follow-Up Item 1 | Exact live apply, rotation, row renewal and cost evidence pending | Distinct follow-up | RV-003; not new active implementation scope |
| Follow-Up Item 2 | No-az/full-gate incompatibility explicitly retained | Distinct follow-up | RV-002; no waiver or substitute gate |

The changes record retains an opening "P01-T01 active" statement, but its
later Implementation Handoff and the details' Current Execution Reconciliation
unambiguously identify authored source work and blocked validation. The
closing state, not that opening activity descriptor, is used here. No
completion, test-pass or publication claim is inferred from checked
source-authoring markers.

## Completed Work Assessment

### Shared boundary and actual test coverage

The JSON now defines 2027-02-01T00:00:00Z. Unchanged runtime loading uses the
packaged JSON; unchanged Bicep loads that file directly; the secret helper
aliases AUTHORITY_END and the deployment helper calls its expiry parser.
The SQL renderer now imports the same authority and substitutes both template
occurrences as whole-second UTC DATETIME2 literals. No second executable
January authority constant was introduced.

Configuration equality is deliberately permitted, whereas admission,
sessions and serving deny at the instant:

* src/core/src/zava_forward/core/resident_showcase.py:242-247 retains row
  window exclusion and now >= AUTHORITY_END; config_from_env refuses expiry
  above the cap and startup at/after configured expiry.
* SessionCodec retains min(configured expiry, AUTHORITY_END), the 1800-second
  limit, signed/process-bound tokens and exact now >= expiry denial.
* src/api/src/zava_forward/api/resident_demo/app.py:101 and :255-258 retain
  the capped app expiry and pre-dispatch expired-service denial.
* The added core admission method covers November 1, the prior December
  maximum, January 31 at 23:59:59.999999, exact February 1 and one second
  later. Existing configuration tests now accept equality and reject both
  one-second and fractional-second excess.
* The new real-loopback HTTP test constructs a January-valid row, identity
  map, app and codec using the shared end, rather than relying on the
  October fixture's six-hour expiry. It asserts login/view success one
  second before the end, token rejection at the end, and HTTP 503 for
  existing-session access and a new login. Its password is a labelled
  synthetic fixture, not an operator credential.
* Infra tests cover old cutoffs, January and exact-cap configuration plus
  one-second/fractional excess. The compiled Bicep test already compares the
  loaded policy with the helper; it was not run and is not substitute proof.

Five additions are identifiable: core admission, SQL rendering, SQL
legacy/reapply, SQL rollback and HTTP boundary. Existing methods were
extended or renamed without removing their guard assertions. This stays
within the eight-method ceiling. These are source-level coverage findings,
not observed test passes.

### SQL transaction and migration

infra/sql/resident-showcase.sql:24-45 keeps XACT_ABORT, BEGIN TRANSACTION,
the named constraint drop, WITH CHECK add, COMMIT and rollback/rethrow in one
GO-delimited batch. The replacement retains both valid_to > valid_from and
the shared maximum. The renderer returns that whole batch to the existing
autocommit executor; there is no batch boundary that commits the drop alone.
Successful replacement should be enabled/trusted; failure should restore
the previous constraint through transactional rollback. No separate source
correctness defect in this design was established.

The migration does not update rows, clear revocation, create a new principal
or alter permissions. Subsequent existing view/grant batches remain outside
the constraint transaction; this is atomic constraint replacement, not a
claim that every script batch forms one transaction.

src/core/tests/test_resident_showcase_sql.py now provides:

* Rendering assertions for two shared-cap predicates, absence of unresolved
  tokens and the single migration batch's transaction/error clauses.
* Existing fresh-fixture checks for blank provenance, one second over cap,
  a zero-length window and cap equality. The fixture executes the normal
  rendered creation and replacement sequence.
* A legacy November constraint, a revoked provenance-bearing row, two full
  reapplies, exact row preservation, enabled/trusted catalog checks,
  view access, base-table denial and verify_rights after each success.
  A newly admitted row exercises November/January and exact-end exclusion.
* An intentionally disabled check with invalid future data in the owned
  disposable fixture. The test snapshots definition/state and rows,
  expects replacement to throw, checks @@TRANCOUNT on the failing connection,
  verifies restoration from another connection and restores fixture checks.

The real-SQL class remains explicitly opt-in and loopback-bounded. None of
these assertions has executed for this candidate. Driver result handling,
actual transactional DDL restoration, trust and idempotence therefore remain
unproven; renderer-string inspection cannot close PC-002's execution debt.
The existing provenance, principal-denial and view-shaping tests remain
present, but are also unrun. See RV-001.

### Unchanged guards and architecture

No diff changes resources, role assignments, routes, private SQL/vault paths,
the min0/max1 replica envelope, per-row approval, synthetic provenance,
revocation or own-case isolation. Runtime and helper control flow remain
unchanged apart from the shared policy's new value.

The secret helper is still new-secret-only:
infra/scripts/credential_arm.py:174-192 rejects any actionable change that
is not Create and requires the exact distinct selected-vault secret set.
infra/tests/test_resident_demo_secrets.py:320-347 retains the explicit Modify
refusal and no-write assertion. No guard was relaxed to implement rotation.
The deployment helper's separate Modify capability is not authorization for
the credential helper to rotate existing secrets.

infra/sql/resident-assistant.sql:37 still denies inference admission at the
2026-11-01 cutoff; no tariff/model authority source was changed. Broader
resident access is not extended paid-inference permission.

### Prospective operations and cost

infra/README.md retains the dated December decision and marks its JSON
maximum and November SQL mismatch as historical. Its new dated #521 section,
the current API guide, knowledge index and appended log consistently describe
the prospective shared source cap without claiming deployed renewal.

Rotation preserves separate exact-operation approval, private access,
SID/narrow rights, individually approved row renewal, provenance/revocation,
bounded version overlap and rollback, session invalidation, expiry alerts,
and verification before disabling old versions. It explicitly says the
unchanged Create-only helper cannot rotate existing secret names. Actual
versions, image, SQL row approvals and intervals are deferred to the exact
owner decision, rather than fabricated.

The cost arithmetic is internally consistent: a labelled USD0.50/day proxy
gives USD46 for 92 days or USD15.50 for January's 31 days, not both added
together; USD10 reserve gives USD56 or USD25.50. USD700 minus USD25.50 is
USD674.50. The two-month proxy is an author assumption, not a tariff or
observed usage. The text excludes additional inference and workload changes,
requires explicit re-estimation for build/egress/logging increments, and
counts non-overlapping accrued, delayed, outside-group and remaining-resource
liabilities. Source-only USD0 is not a zero-running-cost assertion.
January funding and actual headroom remain Unknown. These qualifications
support a planning estimate only, not spend approval or live readiness.

## Implementation-Time Plan and Detail Update Assessment

| Affected scope | Update and trigger | Reconciliation and decision assessment |
| --- | --- | --- |
| P02-T02 / PC-001 | Direct compiled call discovered inside CommandTests | Details name both TemplateTests and the specific CommandTests exclusion; compatible with existing no-az direction, no new decision |
| P01-T02 / PC-002 | Migration proof needed beyond textual rendering | Details define trust, idempotence, preservation and failed-replacement matrix; source tests implement the matrix, execution unavailable |
| P03-T02 / PC-003 | Original Review does not replace final exact-head publication assessment | Details add commit, permitted complete gate, refetch, receipt verification, independent exact-head assessment, then push/PR; blocked today |
| P02-T02 / handoff | Missing namespace and foreign heavy-lock admission prevented setup | Current execution reconciliation leaves task unchecked and describes lightweight results separately; no mocked or partial acceptance substituted |

These updates preserve the confirmed authority boundary and are compatible
direct planner corrections. No significant divergent implementation decision,
scope expansion or unaccepted new architecture assumption was found.

## Critique and Material Revision Assessment

The original critique remains Complete / Revise, with its original one High
and two Medium findings. Its historical verdict is not upgraded by this Review.

* PC-001: selector correction applied in details. Both az-dependent routes
  were independently inspected. Planned permitted suites did not execute,
  so refusal coverage is retained in source, not demonstrated here.
* PC-002: required assertions are materially represented in the source;
  actual SQL proof is outstanding and routed through RV-001.
* PC-003: conditional publication order and invalidation stop conditions
  are explicit. No gate/verification/exact-head assessment or push occurred;
  RV-002 retains that blocker.
* No early resumption of prohibited validation or live dependent work is
  evidenced. Proceeding to Review with disclosed unvalidated source does
  not mean P02-T02 or publication was completed.

No repeat critique, source correction or second original Review is requested.

## Plan Follow-Up Assessment

| Follow-up | Why outside immediate source scope | Owner / next action | Assessment |
| --- | --- | --- | --- |
| Plan Follow-Up Item 1 | Deployment, credential writes, SQL row renewal and paid operation require separate authority | Exercise owner and separately approved operator define exact operation and cost evidence | Open; RV-003, not a source defect or new active phase |
| Plan Follow-Up Item 2 | Current no-az direction conflicts with an unchanged mandatory publication prerequisite | Parent/owner resolve permitted future gate authority without waivers | Open; RV-002, not permission to publish now |

Both are mirrored in the changes record's execution boundary/handoff and
operational guide. Neither is silently converted into completed work or
added to active implementation scope.

## Findings

<!-- rpi:review id=RV-001 -->
### RV-001 [High]: Required runtime and real-SQL validation is unexecuted

* Related scope: P01-T01/T02 acceptance and P02-T02.
* Evidence: the changes record's Validation Admission Blocker and Actual
  Lightweight Results; the details' Current Execution Reconciliation;
  src/core/tests/test_resident_showcase_sql.py migration methods and
  src/api/tests/test_resident_demo_api.py January HTTP method.
  Namespace import and the feedback suite failed with ModuleNotFoundError.
  No core/API/infra runtime, SQL, lint or type result succeeded.
* Impact: the source design and authored boundary matrix cannot establish
  actual admission/HTTP behavior or SQL error propagation, rollback/trust,
  preservation and idempotence. Required acceptance evidence is missing.
  This is validation debt, not a demonstrated SQL implementation defect.
* Destination: later rpi-implement, completing the existing validation task;
  no new research question or source fix is established.
* Smallest useful next action: after a separate coordination event permits
  heavy-run admission, install the existing distributions with pip under the
  required admission control and run the focused changed-path tests, actual
  owned-loopback SQL matrix, permitted infra selectors and planned lint/types.
  Preserve failures/skips. Do not retry/poll the current lock, run az, inspect
  private credentials or claim opt-in discovery skips as SQL success.
  If approved owned SQL cannot be provided within authority, keep acceptance
  blocked and record that evidence boundary.

<!-- rpi:review id=RV-002 -->
### RV-002 [High]: Mandatory publication prerequisites cannot be satisfied under current authority

* Related scope: P03-T02; PC-003; plan Follow-Up Item 2.
* Evidence: src/README.md Local RPI gate requires the complete gate for SQL
  changes and current-base verification before independent exact-head
  assessment/push. tools/rpi-checks.py:1322-1331 includes
  az bicep version in preflight. The caller prohibits every az invocation.
  The candidate is uncommitted and has no complete receipt.
* Impact: neither this completed Review nor the eight tool-contract passes
  permits push or PR. This is a known publication blocker, not evidence that
  the gate itself should be weakened or that a source defect exists.
* Destination: distinct follow-up, plan Follow-Up Item 2, owned by parent/owner.
* Smallest useful next action: retain no-push/no-PR status. Resolve future tool
  authority separately without invoking prohibited commands or inventing an
  alternate receipt. Only when genuinely authorized and available, follow
  the recorded commit/full-gate/refetch/current-base receipt verification/
  independent exact-head assessment sequence. Changed inputs invalidate
  evidence; original adverse records remain immutable. A commit alone does
  not clear this blocker.

<!-- rpi:review id=RV-003 -->
### RV-003 [Medium]: January live renewal and funded headroom remain a separate pending operation

* Related scope: P02-T01 operational handoff; plan Follow-Up Item 1.
* Evidence: infra/README.md January authority source renewal, Credential and
  SQL access rotation plan, Added-cost estimate and Separate live apply;
  src/api/README.md #521 qualification. Existing app/secret/row expiries are
  not changed by the JSON edit; cost evidence is assumption-labelled.
* Impact: the candidate cannot establish January live access, actual budget
  availability or completed rotation. This is deliberately deferred live
  work, not a defect in the source-only candidate or a new active plan task.
* Destination: distinct follow-up, plan Follow-Up Item 1, owned by the
  exercise owner and separately approved operator.
* Smallest useful next action: present the exact reviewed image/configuration,
  constraint and approved row set, credential-version operations, bounded
  refresh/verification/rollback interval and fresh non-overlapping USD700
  liabilities/headroom evidence for explicit owner confirmation. Keep live
  apply Pending; do not broaden Modify, roles, routes or replicas, renew
  paid inference or infer funding from the USD30 historical envelope.

## Defects

No independently established source correctness defect was found in the
supplied diff. Absence of such a finding is not validation success or
conformant acceptance. RV-001 through RV-003 remain actionable.

## Routed Findings

| Finding | Destination | Owner / next action |
| --- | --- | --- |
| RV-001 | Later rpi-implement | Parent completes existing P02-T02 when admission and approved fixture prerequisites genuinely permit |
| RV-002 | Distinct Follow-Up Item 2 | Parent/owner resolves publication authority; otherwise hold publication |
| RV-003 | Distinct Follow-Up Item 1 | Exercise owner selects and funds exact separate live operation |

Later implementation of a routed finding does not require repeating this
original Review. No new rpi-plan or rpi-research invocation is justified by
an established divergent decision or unanswered local research question.

## Validation Evidence

| Check | Status | Evidence and limit |
| --- | --- | --- |
| Initial namespace import | Failed | Caller/changes record: ModuleNotFoundError before setup |
| tools/test_check_demo_feedback.py discovery | Failed | Import failed with missing zava_forward; chained climate test did not run |
| Eight lightweight tool-contract tests | Passed | Recorded 1.347 seconds, zero skips; five GateTests refusal/selection contracts plus test_climate_paired_blocker, not application/gate success |
| Final changed-Python AST, JSON, added-Python line lengths, relative-link targets | Passed | Caller reports final exit 0 immediately before Review; not rerun by assessor |
| Final git diff --check | Passed | Caller reports final exit 0 immediately before Review; not a runtime assertion |
| Initial line-length probes | Failed, then corrected/narrowed | Changes record distinguishes pre-existing renderer line 51 from a newly wrapped SQL-test line; original failure retained |
| Package setup / core/API/infra permitted runtime suites | Unavailable | Foreign heavy-lock admission and missing namespace; no setup admitted |
| Real SQL fresh/migration/rollback/principal tests | Unavailable | No owned-fixture execution result; no skipped discovery treated as proof |
| Ruff / mypy / broader migration validation | Unavailable | Required tooling/setup and heavy admission not satisfied |
| Compiled Bicep TemplateTests and named compiled CommandTests method | Not run | Both invoke az bicep build and are prohibited |
| Complete publication gate / receipt verification / final exact-head assessment | Unavailable | Required az preflight prohibited; no fake or partial substitute |
| Azure/live apply, credential rotation and cost verification | Not run | Outside current authority; pending separate exact owner confirmation |

The recorded heavy admission evidence is lslocks showing foreign python3
PID 3991262 holding /tmp/ama-rpi-heavy.lock, followed by ps confirming that
process exists. It is an admission observation, not permission to inspect
foreign outputs or to install/run alongside it. This Review did not recheck
or poll the lock. Lightweight test results and static exits are supplied
implementation evidence, not newly executed independent validation.

## Blockers, Residual Work and Limitations

* P02-T02 remains incomplete under RV-001. Source-authoring completion does
  not establish all plan acceptance criteria.
* P03-T02 remains incomplete under RV-002. Commit is separable from publication;
  no push, PR, receipt fabrication, cloud fallback or protection change is
  authorized by this record.
* RV-003 remains non-blocking for source authorship but blocks live-readiness
  claims. USD700 remains an all-in cap, not verified headroom.
* The supplied artifact set is sufficiently reconciled for a credible source
  verdict; missing execution evidence limits acceptance, not completion of
  this bounded Review.
* No live legal, pricing, operational, cloud-currentness or production identity
  conclusion is established. No external source retrieval was needed.
* This Review is not the final committed exact-head publication assessment.
  Later source/base changes must retain this original outcome and follow the
  separate publication requirements.

## Outcome

* Review execution: Complete.
* Outcome: Residual work.
* Severity summary: 0 Critical, 2 High, 1 Medium, 0 Low.
* Acceptance: withheld. The shared boundary, guarded SQL design, authored
  coverage and qualified operational guidance are coherent on inspection.
  Required runtime/SQL/lint/types evidence and the full publication gate
  remain unavailable. This is not Conformant or Conformant with justified
  divergence, whole-issue closure, deployment readiness or permission to spend.
* Original critique outcome: Revise, preserved unchanged.

## Closeout Routing Record

| Finding class | Destination | Next owner/action |
| --- | --- | --- |
| Implementation defect | None established | No source fixes requested by this Review |
| Incomplete planned validation | Later rpi-implement, RV-001 | Parent resumes P02-T02 only after genuine prerequisite clearance |
| Significant decision gap / invalid source assumption | None established | Preserve current accepted source-only direction |
| New material research question | None established | Do not repeat local research to bypass unavailable execution evidence |
| Publication blocker | Distinct Follow-Up Item 2, RV-002 | Parent/owner resolves permitted gate authority or leaves publication blocked |
| Non-blocking source-scope residual live work | Distinct Follow-Up Item 1, RV-003 | Exact owner confirmation and fresh cost evidence before any live operation |

## Artifacts

| Artifact | Description |
| --- | --- |
| [.copilot-tracking/research/2026-10-28/resident-authority-extension-521-research.md](.copilot-tracking/research/2026-10-28/resident-authority-extension-521-research.md) | Compared C1-C8 source research |
| [.copilot-tracking/plans/2026-10-28/resident-authority-extension-521-plan.md](.copilot-tracking/plans/2026-10-28/resident-authority-extension-521-plan.md) | Compared scope, markers and distinct follow-ups |
| [.copilot-tracking/details/2026-10-28/resident-authority-extension-521-phase-details.md](.copilot-tracking/details/2026-10-28/resident-authority-extension-521-phase-details.md) | Compared task details and PC dispositions |
| [.copilot-tracking/plans/2026-10-28/resident-authority-extension-521-critique.md](.copilot-tracking/plans/2026-10-28/resident-authority-extension-521-critique.md) | Original Complete / Revise critique, preserved |
| [.copilot-tracking/changes/2026-10-28/resident-authority-extension-521-changes.md](.copilot-tracking/changes/2026-10-28/resident-authority-extension-521-changes.md) | Compared implementation and validation evidence |
| [.copilot-tracking/reviews/logs/2026-10-28/resident-authority-extension-521-review.md](.copilot-tracking/reviews/logs/2026-10-28/resident-authority-extension-521-review.md) | One original Review: Complete / Residual work |

## Next Steps

Return this completed original Review to the active parent. Preserve the
critique and this outcome. Route RV-001 to later rpi-implement only after
prerequisite clearance; retain RV-002 and RV-003 as their distinct existing
follow-ups. Do not fix sources, retry the lock, repeat Review, invoke az,
fabricate a receipt, push or create a PR in this assessment. No further
assessor action is required.
