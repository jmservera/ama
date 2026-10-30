---
title: Resident logout checks 525 independent RPI Review
description: One bounded post-implementation review of the logout assertion correction
ms.date: 2026-10-28
ms.topic: reference
---

## Opening Review State

* Interpreted review goal: independently assess the three-file logout assertion correction for PR-525-PRRT_kwDOUU8JX86xVDWZ, separately from publication readiness.
* Review scope: current uncommitted diff in src/api/checks/resident_demo_browser_check.py, src/api/tests/test_resident_demo_check.py, and src/api/README.md at HEAD 32877254ec92a6aba409a1f43b26a66a52c706e1 on feat/resident-chat-520.
* Evidence readiness: supplied research, plan, phase details, original critique and changes paths are present; detailed comparison and validation inspection pending.
* Acceptance basis: retained-token denial with exact 401, explicit signed-out session fields, request-fence non-vacuity, both call sites including retries, preservation of no-Set-Cookie, and no runtime changes.
* First comparison boundary: reconcile supplied artifact markers and dispositions against the three-file diff and read-only runtime/test context.
* Active read-only boundaries: only this canonical review record may be written. No source, plan, critique, changes, runtime or other review edits; no agents, Azure commands, publication or thread resolution.
* Initial blockers: full publication receipt requires commands prohibited by the caller. Raw validation evidence and the requested heavy lock are under /tmp, which this review worker cannot access or write under its governing restriction; inspect recorded evidence without inventing independent execution.

## Execution Status

* Independent Review execution status: Complete.
* Assessment count: exactly one post-implementation Review, performed on 2026-10-28.
* Source-correction assessment: Conformant within the supplied three-file diff.
* Overall outcome: Residual work, because the mandatory publication gate remains blocked.
* Planned delivery execution is separate: P01 is recorded complete; P02 publication is not complete. This Review completion does not complete publication.
* Independent execution comprised artifact reconciliation, bounded source/runtime comparison, whitespace/runtime-immutability checks, and dependency-free execution of the actual four new helper tests with additional precondition and mutation probes. No package suite, SQL or browser was independently rerun.

## Scope and Evidence

* Task ID: PR-525-PRRT_kwDOUU8JX86xVDWZ.
* Branch: feat/resident-chat-520, tracking origin/feat/resident-chat-520.
* Base worktree HEAD: 32877254ec92a6aba409a1f43b26a66a52c706e1. This is a review of uncommitted corrections, not a committed exact-head publication assessment or fresh remote PR assessment.
* Complete assessed diff: src/api/checks/resident_demo_browser_check.py, src/api/tests/test_resident_demo_check.py, src/api/README.md. No other implementation diff was assessed.
* Read-only runtime context: src/api/src/zava_forward/api/resident_demo/app.py and src/api/tests/test_resident_demo_api.py.
* Compared artifacts:
  * .copilot-tracking/research/2026-10-28/resident-logout-checks-525-research.md
  * .copilot-tracking/plans/2026-10-28/resident-logout-checks-525-plan.md
  * .copilot-tracking/details/2026-10-28/resident-logout-checks-525-phase-details.md
  * .copilot-tracking/plans/2026-10-28/resident-logout-checks-525-critique.md
  * .copilot-tracking/changes/2026-10-28/resident-logout-checks-525-changes.md
* Mandatory project context was consulted. This is not a UI, accessibility, whole-issue, production identity, deployment, legal or human-acceptance assessment. No web assets changed.
* The caller's completed inline search under src/ and tools/ is recorded evidence, not a new repository-wide search performed by this reviewer.

### Reviewed source fingerprints

SHA256 values bind this record to the inspected uncommitted bytes; they are not a gate receipt.

| Boundary | SHA256 |
| --- | --- |
| src/api/checks/resident_demo_browser_check.py | 296302e280230e69d274ca413c959daf267d998e86155265359e4757840349c6 |
| src/api/tests/test_resident_demo_check.py | f3507e4dd4ac319d781b8efcf9e32ca4633ec2319c9113f57545859f4409f398 |
| src/api/README.md | 149f5e88445e3e6dfb882419e54f056ddedc857cd1de9c9e99bed44562d82c1c |
| git diff -- followed by the three paths in the order above | e8b4c980347d83d044cb0bc06d463fafa35ca8f114dc7af8c06956163a1cbea7 |

## Plan-to-Change Reconciliation

| Current plan scope | Changes-record summary | Reconciliation | Gap or rationale |
| --- | --- | --- | --- |
| P01-T01 | Shared signed-in preconditions and signed-out oracle at both paths; fenced replay | Reconciled | Current diff matches requirements and PC-002 disposition. |
| P01-T02 | Four helper tests, related README explanation, SQL literal wrapping | Reconciled | Four new test methods only; literal concatenation preserves the SQL statement. |
| P01-T03 | 68 units, actual SQLite assistant/account and SQL demo browsers, Ruff and mypy | Reconciled as recorded validation | Raw external logs unavailable to this worker; no claim of independent browser/package execution. |
| P02-T01 | Original Review pending at implementation handoff | Reconciled | That prose predates this Review. This one record supplies the independent Review; the parent owns later marker updates and preservation. |
| P02-T02 | Commit and complete gate pending | Open, explicitly blocked | No complete receipt; original RPI evidence and this Review remain uncommitted at assessment. |
| P02-T03 | Conditional push and exact thread disposition | Open, correctly withheld | No publication or thread resolution is authorized by focused validation or this Review. |
| Follow-Up Items | No product follow-up; separately resolve no-az/full-gate conflict | Reconciled | Publication authority remains with the parent/owner; RV-001, not a source defect. |

## Completed Work Assessment

| Related marker | File or symbol | Evidence and assessment |
| --- | --- | --- |
| P01-T01 | signed_in_session | Captures the original cookie, requires session HTTP 200, signed_in exactly True, and a nonempty string session_id. A protected view must then return 200 using that exact fence. The check cannot start from an unauthenticated or unusable-fence state. |
| P01-T01 | check_signed_out | Requires the same original cookie value, exact view 401 with X-Resident-Session, then session HTTP 200 with signed_in exactly False and session_id exactly None. Dictionary indexing makes both fields mandatory; absent fields fail rather than default to signed out. Identity checks reject integer 0 as a false substitute. |
| P01-T01 | check_cross_case_and_logout | Captures the original token/fence before logout and invokes the shared oracle afterward. The separate replay context sends both the original cookie and fence and still requires exactly 401. Cross-case rejection and Bob's protected-view 200 remain unchanged. |
| P01-T01 | check_logout_failure | Captures original token/fence before interception for each 403, 503 and aborted request. Existing failure assertions remain. After unroute, retry and successful logout, every loop iteration invokes the same signed-out oracle. There is no retry branch retaining the stale deletion expectation. |
| P01-T02 | ResidentDemoCheckTests | Four new helper test methods cover success and exact URL/header arguments, missing/replaced cookie, view 200/409/503 rejection, session failure, true/0 signed_in, non-null session_id and missing required fields. Independent source-only execution and mutation probes confirm sensitivity to the specified regressions. |
| P01-T02 | src/api/README.md | Accurately describes retained-token 401, explicit false/null session response and the delayed-response reason for no Set-Cookie. No broader acceptance claim is introduced. |
| P01-T01/P01-T02 | Runtime preservation | git diff confirms neither runtime app.py nor test_resident_demo_api.py changed. The runtime still revokes the token and responds without cookies; the existing unit still asserts absent Set-Cookie, retained token, failed codec verification and replay 401. |

The view oracle is not a generic error check: runtime _session_bound returns 409 for a valid token with an absent/wrong fence, versus 401 for a rejected token. Establishing view 200 before logout with the same fence and requiring exactly 401 afterward rules out the identified fence-only false positive. Actual revocation remains independently specified by the unchanged runtime unit; this source review does not equate any browser-only 401 with proof of every possible internal revocation implementation.

## Implementation-Time Plan and Detail Update Assessment

| Affected area | Change and triggering evidence | Reconciliation and assessment |
| --- | --- | --- |
| P01-T01/P01-T02 | PC-002 sharpened preconditions, exact denial, field presence and request arguments | Plan Functional Requirements, Test Ownership and Budget, details, changes and source agree. Compatible clarification of confirmed intent, not a material scope expansion or unaccepted decision. |
| P01-T03 | Prior environment had missing editable-package imports; parent used a task-owned environment and actual supported browser drivers | Research, details and changes describe the failure, actual commands and storage boundaries. No new dependency-manifest or runtime change appears in the diff. Recorded, not independently re-observed here. |
| P01-T03; PC-001 | Parent rejected a worker-specific filesystem objection against its own explicit caller policy | Caller expressly confirms the parent policy and mandated shared lock. Preserve that disposition and the original critique; do not project this review worker's restriction onto the parent's execution or substitute another lock. This worker cannot inspect the external evidence or acquire the mandated lock, so it ran no heavy checks. |
| P01-T02 | SQL fixture string wrapped for explicit line limit 100 | Adjacent literals produce the same statement. Tightly coupled formatting only; no fixture behavior change. |
| P02-T02/P02-T03 | Complete gate invokes commands forbidden by caller | All supplied current artifacts preserve the blocker and conditional publication. No changed acceptance rule, fabricated receipt or unauthorized early publication is evidenced. |

## Critique and Material Revision Assessment

* Original critique outcome remains Complete / Revise, with PC-001 High and PC-002 Medium. This Review does not rewrite, supersede or relabel that original outcome.
* PC-002 is applied completely within the four-test budget. Source-only negative tests additionally demonstrate that missing headers, a broad non-200 oracle, missing fields and false-equivalent integers do not escape the regressions.
* PC-001 is explicitly rejected by the parent on the caller-confirmed policy distinction. The reviewer's actual filesystem limit is recorded as a validation-access limit, not a renewed source or parent-policy finding.
* No material implementation divergence or significant unaccepted decision was found. Plan/detail refinements are descriptive, compatible and reconciled; there is no evidence requiring another planning/critique cycle for the source correction.
* Dependent-work pause: the complete-gate conflict remains a publication stop. Neither this record nor the focused results permit P02-T03 to proceed.

## Plan Follow-Up Assessment

| Follow-up | Why distinct from source correction | Owner / next action | Assessment |
| --- | --- | --- | --- |
| Publication authority and complete exact-head receipt | Focused source/browser validation cannot satisfy a mandatory complete publication gate; required commands are prohibited | Active parent and owner/policy authority must resolve the conflict, then perform permitted complete validation and exact-head assessment | Open: RV-001. Existing P02 delivery remains incomplete; no product defect or extra P01 task is created. |
| Whole-issue #520 acceptance | Explicitly outside this thread correction | Existing issue owners and acceptance process | Not assessed or closed by this Review. |

## Findings

<!-- rpi:review id=RV-001 -->
### RV-001 [High]: Mandatory publication evidence remains blocked

* Related scope: P02-T02, P02-T03 and plan Follow-Up Items.
* Evidence: plan Acceptance Criteria, details P02-T02/P02-T03 and changes Remaining Work and Publication Boundary agree that the complete gate invokes az, prohibited by the caller. There is no complete exact-head receipt, committed correction/evidence candidate, independent committed exact-head assessment or verified publication eligibility in this review boundary.
* Impact: the source correction is conformant, but must not be pushed or used to resolve PRRT_kwDOUU8JX86xVDWZ yet. Focused success and this uncommitted-diff Review cannot substitute for the complete gate or hosted/human approval.
* Owner: active parent, with owner/policy authority for clearing the command conflict.
* Destination: distinct publication follow-up / existing P02 delivery, not rpi-implement for a source defect and not a repeat Review.
* Smallest useful next action: preserve the original Review and reported evidence; record the publication blocker. Obtain compatible authority before executing currently forbidden commands. After an eligible committed candidate exists, follow the mandatory complete gate, current-base receipt verification and independent exact-head assessment before any normal push or thread action. Do not waive gates, invent a receipt, invoke az now, or silently change protections.

## Defects

* No source-correction defect identified in the complete supplied three-file diff.

## Routed Findings

| Finding | Destination | Owner / next action | Route rationale |
| --- | --- | --- | --- |
| RV-001 High | Distinct publication follow-up and existing P02 work | Parent / policy authority: clear conflict before eligible full validation and publication | Known unresolved publication requirement, not an implementation regression. |

Later implementation or publication work does not require another RPI Review for this task. This original record and outcome must remain immutable.

## Residual Work

* Preserve and commit source and original dated RPI evidence under the required identity/trailer conventions when the parent proceeds.
* Resolve the command-authority conflict and complete all mandatory receipt and independent exact-head prerequisites before publication.
* Only then consider normal push and the exact thread reply/resolution, preserving Refs #520 and no issue-closing language. Hosted and human approvals remain distinct.

## Blockers and Remaining Work

* Blocking publication: RV-001.
* Validation-access limitation: raw focused logs, results.json and browser report are in the caller's external /tmp evidence location, unavailable to this worker. No external files were read or written by this review's commands.
* Heavy-check execution limitation: this worker cannot acquire /tmp/ama-rpi-heavy.lock. No alternate lock was substituted and no heavy checks were started.
* Remaining active work: parent record preservation and P02-T02/P02-T03 under their existing conditions. No corrective source task is recommended.
* Only this canonical Review record was written. No source/artifact correction, remote mutation, agent launch, secret/.env read or Azure command occurred.

## Validation Evidence

| Command or evidence | Scope | Status | Summary and independence |
| --- | --- | --- | --- |
| git diff --check | Current worktree diff | Passed, independently executed | No whitespace errors. |
| git diff --exit-code -- src/api/src/zava_forward/api/resident_demo/app.py src/api/tests/test_resident_demo_api.py | Runtime and contract test | Passed, independently executed | Both files unchanged. Complete implementation name-only diff contains exactly the three specified correction files. |
| python3 -B with an in-memory AST harness | Actual check, signed_in_session, check_signed_out and four new test methods | Passed, independently executed | Extracted these definitions and the test fixture/methods into memory with unittest/Mock; ran all four new tests successfully. This deliberately does not import the application packages or replace the recorded package-suite result. |
| Same in-memory harness, signed-in precondition probes | Original token/fence and invalid preconditions | Passed, independently executed | Success checks exact fence arguments; seven negative cases reject session 503, false/1 signed_in, empty/null/non-string ID and protected-view 409. |
| Same harness, five in-memory source mutations | New regression sensitivity | Passed, independently executed | Tests failed as expected for broad non-200 denial, removed fence header, defaulted missing signed_in, defaulted missing session_id and equality accepting integer 0. Files were never mutated. |
| python -m unittest -q tests.test_resident_demo_api tests.test_resident_demo_check tests.test_resident_chat_api tests.test_resident_assistant_api | Relevant package units | Passed as recorded, not independently rerun | Changes records 68 tests, 41.716s, no skips. Raw log inaccessible here. |
| python -m checks.resident_assistant_browser_check with explicit output | Actual SQLite assistant browser | Passed as recorded, not independently rerun | Changes records Chromium callback/chat and delayed logout replacement-cookie protection; raw report inaccessible. Axe was explicitly not run. |
| python -m checks.resident_account_check | Actual account browser | Passed as recorded, not independently rerun | Changes records account/logout/failure retry and expired-session checks. Account driver itself is not a SQL integration claim. |
| python -m checks.resident_demo_browser_check with task-owned loopback SQL | Actual SQL demo browser | Passed as recorded, not independently rerun | Changes records normal logout, all three retries, replay and other-resident isolation; task-owned bounded container/database and exact cleanup are reported, not freshly observed. |
| python -m ruff check --line-length 100 checks/resident_demo_browser_check.py tests/test_resident_demo_check.py | Changed Python | Passed as recorded, not independently rerun | Raw external results inaccessible. |
| python -m ruff check --isolated --select E501 --line-length 100 checks/resident_demo_browser_check.py tests/test_resident_demo_check.py | Explicit line-100 enforcement | Passed as recorded, not independently rerun | Avoids inferring coverage from a check-file exemption. |
| python -m mypy checks/resident_demo_browser_check.py tests/test_resident_demo_check.py | Changed Python | Passed as recorded, not independently rerun | Changes reports success for two files. |
| Complete publication gate and immediately verified receipt | Committed exact head/current base | Blocked, not run | Caller forbids required az commands. Focused results are not a full receipt. |

The independent source-only harness used Python standard-library AST compilation and mocks, no filesystem outputs, dependency installation, package import, browser, SQL, heavy lock or external resources. It corroborates helper logic and test sensitivity, not integrated cookie transport, actual browser behavior, lint/type outcomes or complete-gate acceptance. Recorded integrated results remain evidence supplied by the implementer, not newly audited raw observations.

## Outcome

* Independent execution status: Complete.
* Outcome: Residual work.
* Source correction: Conformant. Both stale deletion assertions are replaced with a non-vacuous shared retained-token oracle; exact 401, mandatory false/null state, both normal/retry call sites and isolated replay are correctly handled. Runtime no-Set-Cookie and its existing regression remain unchanged.
* Severity summary: 0 Critical, 1 High publication finding, 0 Medium, 0 Low; no source defect.
* Outcome rationale: the full supplied review boundary has been assessed credibly with explicit evidence limits. Source correctness and recorded focused validation do not erase the known incomplete mandatory publication requirement.

## Closeout Routing Record

| Finding class | Destination | Owner / next action |
| --- | --- | --- |
| Implementation defect | None | No rpi-implement correction recommended. |
| Significant decision gap / invalid source assumption | None identified | No source replanning recommended. Any authority change remains a separate explicit decision. |
| Material research gap preventing source verdict | None | External raw-log access is disclosed, not misreported as independent validation. |
| Source-nonblocking residual publication work | RV-001, distinct parent-owned publication follow-up | Resolve command conflict and satisfy existing complete-gate/exact-head requirements before push or thread resolution. |

| Artifact | Description |
| --- | --- |
| [.copilot-tracking/research/2026-10-28/resident-logout-checks-525-research.md](.copilot-tracking/research/2026-10-28/resident-logout-checks-525-research.md) | Supplied research and search conclusion |
| [.copilot-tracking/plans/2026-10-28/resident-logout-checks-525-plan.md](.copilot-tracking/plans/2026-10-28/resident-logout-checks-525-plan.md) | Current plan and critique dispositions |
| [.copilot-tracking/details/2026-10-28/resident-logout-checks-525-phase-details.md](.copilot-tracking/details/2026-10-28/resident-logout-checks-525-phase-details.md) | Phase contracts and publication conditions |
| [.copilot-tracking/plans/2026-10-28/resident-logout-checks-525-critique.md](.copilot-tracking/plans/2026-10-28/resident-logout-checks-525-critique.md) | Preserved original critique |
| [.copilot-tracking/changes/2026-10-28/resident-logout-checks-525-changes.md](.copilot-tracking/changes/2026-10-28/resident-logout-checks-525-changes.md) | Implementation and recorded validation evidence |
| [src/api/checks/resident_demo_browser_check.py](src/api/checks/resident_demo_browser_check.py) | Reviewed browser correction |
| [src/api/tests/test_resident_demo_check.py](src/api/tests/test_resident_demo_check.py) | Reviewed helper regressions |
| [src/api/README.md](src/api/README.md) | Reviewed contract documentation |
| [src/api/src/zava_forward/api/resident_demo/app.py](src/api/src/zava_forward/api/resident_demo/app.py) | Unchanged read-only runtime context |
| [src/api/tests/test_resident_demo_api.py](src/api/tests/test_resident_demo_api.py) | Unchanged no-Set-Cookie/revocation regression |
| [.copilot-tracking/reviews/logs/2026-10-28/resident-logout-checks-525-review.md](.copilot-tracking/reviews/logs/2026-10-28/resident-logout-checks-525-review.md) | This single original independent Review |

## Next Steps

Return this record to the active parent. Preserve the original outcome and update parent-owned handoff markers without editing this Review. RV-001 requires blocker-clearing authority and existing publication work, not a new source implementation task or repeat Review. Do not push or resolve the thread while the mandatory complete gate remains blocked.
