---
title: Resident startup independent RPI Review
description: One independent post-implementation review of the local resident startup diagnosis
ms.date: 2026-10-29
---

## Opening Review State

* Task ID: f568fbf4-e1b7-45d5-ae08-d7034d24a85b.
* Interpreted review goal: assess the complete local resident-startup task once against the canonical dated evidence and exact implementation diff.
* Review scope: full local task; no Azure diagnosis verification, deployment, publication or live readiness acceptance.
* Evidence readiness: supplied canonical artifact paths are identified; the branch and two-file implementation diff are available. Detailed artifact reconciliation and validation-evidence inspection are pending.
* Acceptance basis: current research, plan, phase details, original critique and its recorded disposition, changes, evidence manifest and session state, subject to the supplied local-only authorization.
* First comparison boundary: reconcile plan markers and evidence with the README prerequisite and real SQL regression; distinguish sufficient local failure from the unverified historical Azure cause.
* Active read-only boundaries: only this review record may be written. No source, state, plan, changes or critique mutations; no agents, heavy reruns, Azure commands, private inputs, commit or push.
* Initial blockers: none established; assess evidence sufficiency before assigning an outcome.

## Scope and Evidence

* Review date: 2026-10-29.
* Branch: fix/resident-startup.
* Reviewed HEAD and origin/main comparison base: d70ee60ab3d7346a9991cf64382d9985f4d09f2e.
* Assessed boundary: the full authorized local diagnosis, prerequisite documentation, one SQL regression and recorded local validation. The requested local commit follows this Review and is not yet complete.
* Research: .copilot-tracking/research/2026-10-29/resident-startup-research.md.
* Plan: .copilot-tracking/plans/2026-10-29/resident-startup-plan.md.
* Phase details: .copilot-tracking/details/2026-10-29/resident-startup-phase-details.md.
* Original critique: .copilot-tracking/reviews/plans/2026-10-29/resident-startup-plan-critique.md.
* Changes: .copilot-tracking/changes/2026-10-29/resident-startup-changes.md.
* Manifest: .copilot-tracking/changes/2026-10-29/resident-startup-evidence.json.
* State: .copilot-tracking/rpi-sessions/2026-10-29/resident-startup-state.json.
* Exact implementation diff: src/api/README.md and src/core/tests/test_resident_showcase_sql.py; 59 insertions, no removals or runtime-source changes.
* Scoped source: src/api/src/zava_forward/api/resident_demo/__main__.py, src/api/src/zava_forward/api/resident_demo/aoai.py, src/api/Dockerfile.resident-demo, src/core/src/zava_forward/core/resident_showcase_sql.py, infra/scripts/resident_showcase_sql.py and infra/sql/resident-showcase.sql.
* Context: docs/case_study_48_original.md, docs/case_study_48_addendum.md, docs/reference/README.md, docs/reference/memory.md and src/README.md.
* External evidence boundary: only the eight named validation/probe/build files listed in the manifest's external_sha256 map were read. Every SHA-256 matched. The probe JSON and validation summaries were inspected; no other session backups, credentials, private datasets or live resources were accessed.

## Execution Status

* Review execution status: Complete.
* Review execution evidence: one independent artifact/source/evidence assessment on 2026-10-29, with log-hash verification and git diff --check; no agents or heavy validation reruns.
* Planned task execution at this boundary: Partial solely because P02-T02 includes this Review and the subsequent local commit. P01 and P02-T01 are complete; the parent must record this original Review and perform the authorized local commit. This is expected sequencing, not an implementation defect or a claim that the commit already exists.

## Plan-to-Change Reconciliation

| Current plan scope | Descriptive changes-record summary | Current-state reconciliation | Gap or rationale |
| --- | --- | --- | --- |
| P01-T01 | Startup prerequisite and bounded local diagnosis | Reconciled | README explains the 17th column, read-before-bind failure, optional settings, existing port/probe and separately authorized SQL process. |
| P01-T02 | One real SQL compatibility regression | Reconciled | Exactly one test added; both reader paths reject the renamed column, finally restores the current template, restricted SELECT works afterward. |
| P02-T01 | Static, resident unit, actual SQL and image checks | Reconciled | Manifest, hash-matching logs and recorded counts agree; skipped discovery integrations remain explicit. |
| P02-T02 | Original independent Review and local commit | Intentionally open | Plan/details/changes/state consistently identify Review as current and commit as subsequent. A null state review pointer before this Review is expected. |
| Follow-Up Items | Live view/auth/secretRef and existing executor issues | Reconciled | Retained outside active implementation and acceptance; neither local SQL nor old-revision health proves cloud cause/readiness. |

## Completed Work Assessment

| Related marker | Files | What changed and why | Completion evidence | Validation | Assessment |
| --- | --- | --- | --- | --- | --- |
| P01-T01 | src/api/README.md | Makes the existing SQL prerequisite discoverable at startup guidance; explains no new mandatory app setting | Exact diff matches the reader, entry point, optional AI/agenda construction and Docker probe | Source comparison and same-image local probe record | Conformant; no instruction to perform an unauthorized live apply |
| P01-T02 | src/core/tests/test_resident_showcase_sql.py | Temporarily renames documents_json to reproduce missing named projection | Actual ProgrammingError asserted for list_rows and fetch_case; restoration uses script.render in finally | Hash-matching opted-in SQL log names the new test as passed; 34 tests, zero skips | Conformant; uses the existing unique loopback database and cleanup lifecycle |
| P02-T01 | Dated evidence manifest and named external logs | Records focused local evidence without a full-gate claim | Log hashes, counts and source-base src tree identity checked | Static/unit/SQL/image results below | Conformant within stated coverage; not a fresh independent test execution |

The regression intentionally simulates the missing projection rather than claiming to recreate all historical SQL bytes. The separate same-image experiment supplies the actual old-template comparison. Restored list/single-case restricted-principal queries are equal after an independently verified fixture read; existing permission tests also pass, so a vacuous empty-output comparison is not the sole restoration evidence.

## Implementation-Time Plan and Detail Update Assessment

| Affected area or marker | What changed and why | Triggering evidence and user decision | Reconciliation performed | Planning and critique state | Assessment |
| --- | --- | --- | --- | --- | --- |
| Research-to-plan direction; P01 | Documentation/regression instead of speculative runtime fix | Same main image fails against old view and serves after current view; confirmed request permits documenting required configuration | Current plan, details and changes describe a deployment prerequisite, not a demonstrated runtime-source bug | Ready; original critique retained | Preserves approved intent; no significant divergent decision |
| P01 and P02-T01 | Completion markers and validation summaries updated | Recorded source changes and completed local checks | Plan/details/changes/state agree on completed work and remaining Review/commit | Pre-Review reconciliation explicit | No stale completion claim |
| P02-T02 and publication boundary | Review and local commit remain open; full gate excluded from current completion | User no-az/no-push boundary | Acceptance, dependencies, details and changes preserve no receipt/hosted/human/live readiness claim | No new planning revision needed | Publication remains gated, not silently waived |

## Critique and Material Revision Assessment

* Original critique remains Complete / Revise, with PC-001 Medium; it has not been rewritten into a pass.
* The parent explicitly rejected PC-001's filesystem-premise in plan/details/changes/state and reported actual admission through the repository's shared lock. src/README.md confirms the shared-lock requirement. No substitute lock or bypass is reported.
* Host distinction matters: this reviewer's current instructions explicitly prohibit temporary-directory file operations. Accordingly this Review performed none and did not rerun lock-dependent checks. The parent's assertion about its earlier instruction context is a historical disposition, not an assertion that the prohibition is absent in this review host. Earlier host permissions were not independently established by this Review; no retroactive permission or new heavy execution is inferred.
* Existing recorded results can be assessed without repeating the disputed operation. Their matching hashes and technical outcomes support the authorized source review, independently of any claim about historical host permissions.
* No material implementation-time scope revision or unresolved user-owned decision was found. The prerequisite documentation and real SQL test fit the critiqued technical direction. No second critique or Review is required or performed.

## Plan Follow-Up Assessment

| Follow-up item | Why outside immediate scope | Owner or next action | Assessment and route |
| --- | --- | --- | --- |
| Live view/schema, auth and secretRef verification before retry | Cloud access, real SQL and rollout are prohibited here; failed-revision console unavailable | Responsible deployment/SQL operator, after separate owner authorization | Open distinct operational follow-up; confirm actual environment and review/apply view through existing process before separately authorized retry |
| Existing rollout executor secretRef/deadline findings | Previously identified executor work is not required to demonstrate or document this local SQL prerequisite | Deployment-tooling owner; take the preserved prior findings into separately scoped work | Open distinct follow-up; not folded into current source implementation |

These are not implementation defects or new active tasks. The changes record mirrors both plan follow-ups. Historical Azure causality remains unknown, not an unmet local research claim.

## Findings

No substantive, high-confidence actionable finding was identified within the authorized local implementation boundary. Severity summary: 0 Critical, 0 High, 0 Medium, 0 Low. No RV IDs are invented for expected sequencing, acknowledged unrun checks or distinct existing follow-ups.

## Defects

* None identified. No rpi-implement correction is routed.

## Routed Findings

| Finding | Destination | Owner or next action | Reason for route |
| --- | --- | --- | --- |
| None | None | Parent continues the already planned local closeout | No implementation defect, significant decision gap or material local evidence gap established |

## Residual Work

* Retain the two distinct plan follow-ups with the operational/tooling owners above. Neither blocks acceptance of the documented local prerequisite or implies permission for Azure access.
* Local commit and artifact/state reconciliation belong to the existing P02-T02 parent continuation, not a newly created follow-up or a second Review.

## Blockers and Remaining Work

* Review blockers: none.
* Remaining active work: parent records this original Review and completes the requested privacy-safe local commit with the mandated trailer; do not amend, push or claim that this review has committed anything.
* Publication remains blocked pending separately authorized complete gate/receipt and exact-head/hosted/human requirements. No such checks, receipt or approvals are established here.
* No current cloud cause, byte identity with the failed deployed image, live managed-identity authentication, secret resolution or live SQL compatibility is accepted.

## Validation Evidence

| Command or evidence | Scope | Status | Summary |
| --- | --- | --- | --- |
| Recorded main Docker build and same-image old/current SQL comparison | Unmodified source at supplied main base; task-owned constructed SQL | Passed, recorded evidence | Old 16-column view: exit 2, ProgrammingError naming documents_json. Current 17-column view: same image/settings running on 0.0.0.0:8089, allowed healthcheck 200, shell 200, unsigned view 401, wrong Host 403. |
| Recorded dummy MSI configuration with network disabled | Constructed setting names/values | Expected failure, recorded evidence | Reaches SQL authentication and exits 2 with InterfaceError; does not establish Azure authentication. |
| python -m ruff check .; python -m ruff format --check .; python -m mypy with external cache | Full core and API projects | Passed, recorded evidence | Core 104 formatted files / 157 typed source files; API 56 / 106. |
| python -m unittest discover -s tests -p 'test_resident*.py' -v | Core resident discovery | Passed with skips, recorded evidence | 306 tests, 88 opt-in integration skips. |
| Same discovery with documented cross-project test fixture paths | API resident discovery | Passed with skips, recorded evidence | 135 tests, 7 opt-in SQL/browser skips. |
| python -m unittest tests.test_dependency_rule -q | Core and API | Passed, recorded evidence | 2 tests per project, zero skips. |
| ZF_TEST_MSSQL=1 python -m unittest tests.test_resident_showcase_sql -v | Existing complete opted-in resident showcase SQL module | Passed, recorded evidence | 34 tests, zero skips; new missing-projection regression and existing permission tests explicitly passed. |
| python -m checks.resident_demo_image_check | Existing actual image contract | Passed, recorded evidence | 22 PASS assertions; startup refusals, container hardening, Host/session denial and synthetic login/isolation. Separate from same-main port/schema experiment. |
| SHA-256 verification against manifest | All eight named external evidence files | Passed in this Review | All hashes matched; validation summaries and probe observations inspected. |
| git rev-parse HEAD; base src tree comparison | Reviewed source ancestry | Passed in this Review | HEAD matches supplied base; base src tree 6684959daaa64df7f8768c4fddb24406f198a308 matches manifest. |
| git diff --check; exact two-file diff inspection | Current implementation | Passed in this Review | No whitespace errors; README links target existing files; no runtime source or permission changes. |
| Heavy test/build reruns | Independent Review | Not run | Existing scoped evidence sufficient; caller prohibits duplication. Current review host filesystem restrictions are respected. |
| Other discovery integration checks; complete publication gate; cloud/live checks | Outside current validation boundary | Skipped / not run | Opt-in skips remain explicit; no-az/no-push authorization excludes publication/live work. No full coverage or receipt inferred. |

Evidence limitations: logs are parent-executed results, not independently reproduced executions or exact-head publication receipts. Matching hashes establish consistency with the manifest, not hosted/human approval. The image is a fresh same-source build, not a claim of byte identity with the historical failed Azure artifact. Research question-table entries retain their original Open labels, but the explicit research stop/readiness text, C5-C9 and current handoff resolve them at the local-only boundary; this does not create substantive scope ambiguity.

## Outcome

* Outcome: Conformant.
* Outcome rationale: completed implementation satisfies the accepted local direction without speculative runtime changes, fabricated document facts, widened grants or cloud-causality overstatement. Recorded relevant static/unit/actual SQL/image checks support it; one independent Review is now retained. Task-wide final commit acceptance remains pending parent closeout, not represented as already fulfilled.

## Closeout Routing Record

| Finding class | Destination | Owner or next action |
| --- | --- | --- |
| Implementation defect | None | No correction established |
| Decision gap or invalid assumption | None | No significant unresolved implementation decision |
| Material evidence gap | None for local task | Historical Azure cause remains explicitly outside accepted boundary |
| Non-blocking residual work | Distinct operational and deployment-tooling follow-ups | Owners and authorization steps in Plan Follow-Up Assessment |

* Review execution status: Complete.
* Outcome: Conformant.
* Validation coverage: recorded full core/API static checks, scoped resident/dependency units, real SQL 34/0 skips and image 22 assertions; external log hashes verified, no heavy reruns.
* Blockers: none for Review; local commit pending; publication/live gates unmet and not authorized.

## Next Steps

Return this one Review to the active parent. The parent should reconcile its state and P02-T02 completion after the requested local commit with privacy-safe identity and mandated trailer. Preserve the original critique and this Review, retain separate live/tooling follow-ups, and do not push or launch a second Review. No user action is required for this local continuation.
