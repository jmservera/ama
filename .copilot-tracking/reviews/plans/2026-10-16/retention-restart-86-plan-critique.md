---
title: Resident retention restart final-candidate plan critique
ms.date: 2026-10-16
---

## Metadata

* Task ID: issue-86-retention-restart
* Task slug: retention-restart-86
* Critique date: 2026-10-16
* Plan: .copilot-tracking/plans/2026-10-16/retention-restart-86-plan.md
* Phase details: .copilot-tracking/details/2026-10-16/retention-restart-86-phase-details.md
* Critique execution status: Complete
* Assessment count: One final-candidate critique; no implementation or delegated review.

## Inputs and Criterion Boundary

* Caller requirements and latest owner decision supplied in this task are authoritative:
  five years from first recorded contact after deletion, not a decision date or
  permanent expiry. Replace the named pinning test, cover returning residents,
  repeated expiry/renewal and personal-data-free tombstones, and remove the README limit.
* Planning evidence: the plan, phase details and
  .copilot-tracking/research/2026-10-16/retention-restart-86-research.md.
* Code evidence: src/core/src/zava_forward/core/resident_decisions.py,
  src/core/src/zava_forward/core/store.py (log_call),
  src/core/src/zava_forward/core/doc_controls.py (retention delegation), and
  src/core/tests/test_resident_decisions.py. Supporting configuration/privacy
  checks used src/core/pyproject.toml and
  src/core/src/zava_forward/core/projection.py.
* Requirements boundary includes installed src-layout packages, external tests,
  isolated pip-venv unit/Ruff/mypy validation, no new SQL/schema/dependencies,
  no private data or excluded-file access, no Docker/Azure execution, append-only
  reference logging and references-only PR linkage. Test ownership, the single
  removal and maximum five additions remain locked.
* Assessment covers implementation credibility and planned acceptance evidence,
  not implementation correctness, live-platform acceptance, legal approval or
  historical erasure. No tests or remote operations were performed.

## Coverage Assessment

| Requirement, research, phase, or task ID | Coverage | Evidence or concern |
| --- | --- | --- |
| Owner rule and superseded pinning behavior | Covered | Explicit decision and named obsolete test removal; no new product decision needed |
| P01-T01 shared contact boundary | Covered | log_call and safe_contact_record both use remember_first_contact; count boundary avoids same-day timestamp ambiguity |
| Retained general contacts and independent purposes | Covered | Prefix exclusion rather than deletion; complaint/contact preservation is explicit |
| Legacy date-only tombstones | Partial | Conservative fallback is specified; positive recovery and its distinction from modern same-day recovery need explicit test assertions, PC-001 |
| Returning resident and repeated renewal | Partial | Clock scenarios are listed, but successful fresh scoped acceptance and independently exercised contact origins need explicit acceptance assertions, PC-001 |
| Privacy, gates and legal hold | Covered | Metadata-only tombstone, cleared scoped fields, retained gate checks, exact-key/type and canary assertions |
| P01-T02 original-code failure proof | Partial | Mutation proposal allows a method-only substitution without specifying helper/import binding coverage, PC-002 |
| P01-T02 local validation constraints | Partial | Pip-venv/core/API/Ruff/mypy are required; existing test scratch allocation needs an explicit compliant root, PC-003 |
| P01-T03 documentation and delivery | Covered | README replacement, routing row, append log, review, noreply identity, trailer, normal push and Refs #86 only |
| Ownership, additions and dependencies | Covered | JSON tests inherited by SQLite, exact single removal, maximum five additions; publication follows validation/review |

## Verdict

* Verdict: Revise
* Rationale: The proposed implementation is credible and the owner rule is
  resolved. Three bounded evidence/execution corrections are needed before the
  plan can substantiate its acceptance claims. None requires changing the
  architecture, expanding the locked test count or obtaining a new owner decision.
* Severity summary: Critical 0; High 0; Medium 3; Low 0.

## Findings

<!-- rpi:critique id=PC-001 -->
### PC-001 [Medium]: Make the positive recovery paths independently observable

* Related IDs: P01-T01, P01-T02; returning resident, both contact routes,
  same-day boundary and legacy fallback requirements.
* Evidence: The P01-T02 bullets name same-day general contact and fresh safe
  contact, earliest date, old contacts and legacy tombstones, but do not require
  each route to establish an origin from Unknown independently, nor explicitly
  require successful new scoped acceptance. In
  src/core/src/zava_forward/core/resident_decisions.py, either writer can set the
  shared cached marker; exercising the second writer after the first can mask a
  broken origin path. The existing owner-rule pinning test asserts refusal,
  not positive recovery.
* Concern: A combined sequence can satisfy the listed clock assertions while
  one contact route remains broken. Negative legacy filtering alone can also
  pass when legacy cases never regain a period.
* Impact: Tests could miss a returning resident still being blocked, or fail to
  detect a date-only filter incorrectly applied to modern same-day contacts.
* Smallest useful change: Within the existing maximum five JSON methods, specify
  independent fixtures/subtests for general-only and safe-contact-only recovery.
  For the modern general-contact case, retain a pre-deletion contact on the same
  day/minute as the new contact and assert that only the appended suffix supplies
  the origin. For a legacy date-only tombstone, keep same-day old contacts and a
  stale cached marker, assert Unknown, then record a later-day contact and assert
  its exact origin/due. Include a fresh scope/Accepted decision after recovery,
  with no automatic acceptance before it. Reopen the stores for the asserted
  persisted result.
* Action owner: Planning parent, then implementer.
* Exact resolving evidence: Revised P01-T02 assertions covering these independent
  sequences within the locked ownership/count, followed during implementation
  by passing JSON/SQLite cases, exact origin/due and scoped acceptance results.
* Decision route: Direct planner correction; the owner has already resolved the rule.

<!-- rpi:critique id=PC-002 -->
### PC-002 [Medium]: Pin what the original-code failure experiment actually replaces

* Related IDs: P01-T02; acceptance criterion that new tests fail without the code change.
* Evidence: Phase details permit loading the original resident_decisions
  implementation in memory or temporarily substituting only its methods.
  first_contact and remember_first_contact are module-level functions;
  src/core/src/zava_forward/core/store.py imports remember_first_contact
  directly. Restoring a class method does not necessarily restore those
  functions or the already-bound store alias.
* Concern: The proposed alternative leaves the regression experiment's executed
  behavior ambiguous. A failure caused only by restoring deletion, or by module
  loading/import errors, is not complete evidence that the new restart tests
  detect the intended original behavior through both writers.
* Impact: The required failure-without-implementation claim can be overstated or
  depend on an accidental mixture of original and changed code.
* Smallest useful change: Specify a coherent original-code baseline for all
  changed production behavior. If in-memory substitution is retained, name the
  helper globals and directly imported aliases that must execute the baseline,
  and require assertion failures for the selected new restart scenarios rather
  than import/setup failures. Identify the selected test names and restoration
  check in the changes evidence.
* Action owner: Planning parent, then implementer.
* Exact resolving evidence: A precise baseline procedure in P01-T02 and, later,
  selected original-code assertion failures for JSON/SQLite plus green restored
  execution and an unchanged production diff after mutation cleanup.
* Decision route: Direct planner correction; no user decision required.

<!-- rpi:critique id=PC-003 -->
### PC-003 [Medium]: Route test scratch allocation inside the project

* Related IDs: P01-T02; environment prohibition on temporary-directory locations.
* Evidence: src/core/tests/test_resident_decisions.py setUp uses
  tempfile.TemporaryDirectory() without a directory argument. The plan requires
  these tests but does not specify a project-local scratch root. The supplied
  execution constraints prohibit file operations under /tmp or /var/tmp.
* Concern: An ordinary invocation can allocate the synthetic store and SQLite
  database outside the permitted project location.
* Impact: Required validation could violate the execution boundary or fail under
  enforcement despite using synthetic data.
* Smallest useful change: Set an existing project-local scratch directory as
  TMPDIR before starting each test Python process, keep the venv project-local,
  and clean generated scratch files afterwards. Do not change the canonical
  test ownership or add methods for this execution-only adjustment.
* Action owner: Planning parent, then validation implementer.
* Exact resolving evidence: P01-T02 specifies the project-local paths/environment;
  implementation validation records the effective tempfile root and commands,
  and final status shows no leftover generated scratch artifacts.
* Decision route: Direct planner correction; no user decision required.

## Strengths and Residual Risk

* The shared helper/count design addresses both retained general contacts and
  same-day ordering without SQL changes or copying personal values.
* Existing date-only tombstones cannot reconstruct historical same-day order.
  The supplied design explicitly chooses conservative exclusion for general
  contacts on/before that date. Document this limitation distinctly from modern
  count-boundary behavior; do not claim exact legacy same-day recovery.
* Safe-contact history is removed by RESIDENT_FIELDS deletion, making fresh
  history a separate post-deletion evidence source. Its source/reference/actor
  fields must remain outside the tombstone.
* Exact metadata keys/types and canary checks are appropriate privacy evidence.
  Retaining separately purposed contacts and complaint outcomes is intentional;
  metadata minimization is not whole-case anonymization or historical erasure.
* Approval delegation in doc_controls.py already reaches the shared deletion
  method. No extra endpoint, schema or backend-specific implementation is needed.
* Existing formatter exclusions and mypy ignore_errors cover the migrated
  production module. Successful configured checks must not be described as
  comprehensive static verification of that module; behavioral tests remain essential.

## Questions or Blocking Evidence Gaps

* No unresolved owner decision or decision-critical research blocker.
* The latest owner decision and branch lifecycle are accepted from the supplied
  task/research; this critique does not re-fetch the issue or repeat research.

## Limitations

* Static final-candidate assessment only. No implementation, test execution,
  mutation, installation, private data access, Azure operation or deployment.
* The original plan, phase details and research were not edited. Pre-existing
  untracked planning artifacts remain in place on
  feat/retention-restart-after-deletion-86.

## Recommended Next Action

* Highest-impact finding: PC-001.
* Action owner: Planning parent.
* Smallest next action: Clarify the independent recovery and legacy positive
  assertions in P01-T02; resolve PC-002 and PC-003 in the same direct revision.
* User response required: No.
* Finalize after disposition of this single critique; do not run another critique.

| Artifact | Description |
| --- | --- |
| .copilot-tracking/plans/2026-10-16/retention-restart-86-plan.md | Final candidate assessed |
| .copilot-tracking/details/2026-10-16/retention-restart-86-phase-details.md | Implementation and validation details |
| .copilot-tracking/research/2026-10-16/retention-restart-86-research.md | Supplied reused evidence |
| .copilot-tracking/reviews/plans/2026-10-16/retention-restart-86-plan-critique.md | Complete single-pass finding set |

## Next Steps

Planning parent: directly revise and dispose of PC-001 through PC-003, preserving
the locked test ownership/removal/addition limits, then finalize the plan under
the active orchestration. No user action is required. This critique stops here.
