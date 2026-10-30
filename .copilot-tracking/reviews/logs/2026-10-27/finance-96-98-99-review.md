<!-- markdownlint-disable-file -->
# Review: finance-96-98-99

## Scope and Evidence

* Task ID / slug: finance-96-98-99
* Date: 2026-10-27
* Scope: full independent-slice P01/P02 plan, not whole-issue approval acceptance.
* Plan: .copilot-tracking/plans/2026-10-27/finance-96-98-99-plan.md
* Details: .copilot-tracking/details/2026-10-27/finance-96-98-99-phase-details.md
* Critique: .copilot-tracking/reviews/plans/2026-10-27/finance-96-98-99-plan-critique.md
* Changes: .copilot-tracking/changes/2026-10-27/finance-96-98-99-changes.md
* Research: .copilot-tracking/research/2026-10-27/finance-96-98-99-research.md
* Baseline and fetched origin/main: 09099ecd1a66ee9d37ad993707d1f2eda07cdfd4.

## Opening Review State

* Goal: independently compare the complete supplied source/test/doc/artifact diff with the plan, requirements, critique dispositions and honest authority boundary.
* Evidence readiness: P01/P02 markers, details, changes and local checks reconciled. Core 199 tests (54 optional skips), API 1124 (314 optional skips), Ruff and targeted mypy successful.
* Acceptance basis: working field isolation/history, deterministic held diagnostics/manifests, current actor/source checks, persistence and explicit missing Finance/Board decisions; full #96/#98/#99 acceptance remains partial/blocked.
* First comparison: source/test behavior and documentation claims, then plan/critique/change reconciliation.
* Read-only boundary: only this review record may be written; no source, plan, original critique or changes edits, no fix/Review loop.
* Initial blockers: no actual approved template/source/rules or OD-12/15 Board inputs. No reviewed export, actual approved envelope, breach/restart or programme-wide acceleration enforcement is claimed.

## Execution Status

* Review execution status: Complete.
* Planned independent-slice execution: Complete as recorded by P01/P02 and the changes record; this is not a finding of defect-free behavior or whole-issue acceptance.
* Review outcome: Not accepted.
* Severity summary: 0 Critical, 0 High, 2 Medium, 0 Low implementation findings.
* This is the task's one independent post-implementation Review. No nested agent, second Review, source correction, gate, deployment or broad test run was performed.
* HEAD and locally fetched origin/main were independently read as 09099ecd1a66ee9d37ad993707d1f2eda07cdfd4. The assessed candidate includes the supplied dirty tracked files and untracked new module/tests, not just HEAD.

## Evidence Boundary

Read the complete tracked diff and complete new src/core/src/zava_forward/core/form_review.py and src/core/tests/test_form_review.py. Tracked changes assessed:

* src/core/src/zava_forward/core/store.py
* src/core/pyproject.toml
* src/core/README.md
* src/api/src/zava_forward/api/server.py
* src/api/tests/test_form_staging_api.py
* src/api/tests/test_role_endpoint_inventory.py
* src/api/README.md
* docs/reference/README.md
* docs/reference/log.md

Read the complete canonical plan, details, original critique, changes and research. Checked the directly relevant forms actor/schema/staging helpers, controlled rollback and SQL actor recheck, SQLite lock synchronization/rowversions, document availability/storage behavior, case projection and HTTP error mapping. Compared PRD FR-038..043 and AC-048..051/054, BRD RULE-010..012 and OD-12/15, and relevant original/addendum, reference-index, memory and customer context. Memory and constructed exercise assumptions are not financial authority.

The supplied acceptance matrix and research's scoped issue evidence are the issue boundary; no fresh GitHub issue retrieval or hosted-state verification was performed. No private datasets, Azure, secrets/.env, uv or financial approvals were accessed. Review wrote only this record.

## Plan-to-Change Reconciliation

| Current plan scope | Changes-record summary | Current-state reconciliation | Gap or rationale |
| --- | --- | --- | --- |
| P01-T01: core review, diagnostic manifest and held ledger | Isolated field reviews and held manifests | Reconciled in scope; defects found | The module implements the agreed independent slice, but missing-byte historical disclosure and unqualified stale-candidate conflict reporting remain RV-001/002. |
| P01-T02: authenticated HTTP and projection isolation | Adapter and documentation integration | Reconciled | Dedicated endpoint delegates to core guards; ordinary detail strips both new private keys. Core defects also affect endpoint output. |
| P02-T01: local proof | Validation Record | Reconciled with limitations | Core/API totals and skips match supplied logs. Existing tests do not exercise RV-001/002; green results do not prove those boundaries. |
| P02-T02: documentation and pre-Review handoff | Adapter/documentation; Pre-Review Reconciliation | Reconciled | Documentation is explicit about unapproved authority, partial acceptance and parent-owned publication. Broad missing-evidence wording exceeds the implementation at RV-001. |
| Follow-Up Items | Human Decisions Required; Follow-Up Items | Reconciled and still open | Actual Finance/template authority and Board OD-12/15 inputs remain separate human prerequisites, not implementation completion claims. |

## Completed Work Assessment

| Related marker | Files | What changed and why | Completion evidence | Validation | Assessment |
| --- | --- | --- | --- | --- | --- |
| P01-T01 | src/core/src/zava_forward/core/form_review.py; src/core/tests/test_form_review.py | Isolated open/review/diagnose records, immutable prior/new field history, exact staged-source anchors and permanent Held readiness | Read full implementation and tests; field updates target one field and append history; original staging is not overwritten | Parent core checks; review's constructed read-only repro | Substantially implemented; RV-001/002 prevent acceptance of the promised evidence/diagnostic boundary. |
| P01-T01 | src/core/src/zava_forward/core/form_review.py | Held template/rules and OD-12/15 records | Null approved inputs/evidence, owner role, recorder/time and correction path; no authority transition API | Both-backend persistence tests in supplied suite | Conformant to independent-slice ledger contract, not actual Board or Finance acceptance. |
| P01-T02 | src/api/src/zava_forward/api/server.py; src/core/src/zava_forward/core/store.py | Authenticated dedicated route and ordinary-projection isolation | Exact-key validation, current actor checks, existing error patterns, private-key removal | Three new HTTP methods and expanded all-role inventory; complete parent API discovery | Conformant adapter structure; inherits core findings. |
| P02-T01 | src/core/tests/test_form_review.py; src/api/tests/test_form_staging_api.py; src/api/tests/test_role_endpoint_inventory.py; src/core/pyproject.toml | Synthetic regressions and narrow migrated-helper typing accommodation | One new core class, three new HTTP methods, no removed tests; override disables untyped-call rejection only for named modules | Parent Ruff and targeted mypy reported passed | Within fixed ownership limits; no broad type-checking or production proof inferred. |
| P02-T02 | src/core/README.md; src/api/README.md; docs/reference/README.md; docs/reference/log.md; canonical tracking artifacts | Document actual scope and required human decisions | New links, append-only log entry, explicit no-approved-export/no-programme-gate statements | Parent link check; review diff and whitespace inspection | Financial claims are appropriately bounded; missing-source guarantee requires RV-001 correction. |

### Behavior and Authority Assessment

* Field isolation: review changes its selected working field and append-only history; diagnose appends a deep-copied snapshot; holds and draft versions are the declared additional metadata. No source, authoritative Finance/grant, consent or ranking mutation is introduced.
* Source binding: sourced accept/correct checks same case, exact draft schema ID/version/digest, field ID, permitted kind, clean scan, source metadata and current byte hash. Acceptance preserves raw text; correction requires an explicit finite scalar and reason. A candidate from an old source is refused for acceptance.
* Disclosure: metadata removal, generated sources, missing/pending/infected scan state and forbidden current source kind block affected history before return. Historical checks do not always verify actual source-byte availability: RV-001. This is not a demonstrated bypass of infected-scan or role checks.
* Freshness: source changes mark currently source-bound working fields stale; a newer schema version marks all fields of that draft stale. Prior records remain intact. Rule/input/pack/downstream approval propagation is explicitly absent and is not accepted as AC-051. Unreviewed conflict alternatives do not receive equivalent source freshness qualification: RV-002.
* Optimistic writes/rollback: exact positive draft versions, controlled case rollback, audit-before-save, SQL rowversion conflicts and current actor rechecks are present. JSON protection is explicitly one Store/writer, not independent processes. No hidden scan/save is introduced inside review. Existing failure-injection tests cover open and existing-history failures, and independent SQLite writers.
* Scalar/conditional semantics: all six declared types, exact scalar-type equality, finite floats, calendar-valid ISO dates, no implicit conversion, confirmed/current/valid inputs only, and OR with Unknown fallback match PC-002's contract. Invalid corrections may remain working notes but produce Fail and never approved readiness. No unit, currency, formula or eligibility authority is inferred.
* Diagnostic snapshots: report and history copies are detached; diagnose persists a versioned frozen report, and subsequent view exposes current diagnostics alongside explicitly recorded snapshots. Snapshots remain Held and cannot be submitted or approved. RV-001 also matters to disclosure of these retained snapshots; RV-002 can be frozen into one.
* Unauthorized actions: strict request keys and allowed actions reject actor/status/approval injection and approve/submit/reviewed-export/restart requests; human-only categories are denied. Existing actor checks run before dedicated reads and within controlled writes. No source-based or financial delegation is invented.

## Implementation-Time Plan and Detail Update Assessment

| Affected area | What changed and why | Triggering evidence and user decision | Reconciliation performed | Planning and critique state | Assessment |
| --- | --- | --- | --- | --- | --- |
| P01-T01/P02-T01 | Non-mutating already-clean evidence preflight | PC-001; existing scan helper can save/quarantine; no new user financial decision needed | Plan, details and changes describe separate scan/recovery | Original Revise retained; direct disposition recorded | Chosen transaction correction is implemented; broader missing-evidence disclosure remains incomplete at RV-001. |
| P01-T01/P02-T01 | Raw acceptance, explicit typed correction, exact conditions and OR/Unknown | PC-002; staged values are raw text | Plan/details/docs/code align | Original critique retained | Compatible engineering clarification, no divergent decision requiring new authority. |
| Acceptance/P02-T01 | JSON single-writer versus SQLite cross-writer protection | PC-003; existing backend mechanisms | Backend-qualified plan, details, docs and tests | Original critique retained | Resolved; no cross-process JSON claim remains. |
| P02-T02/Handoff | Completion means documentation/pre-Review handoff, not completion of future parent Review/publication | Avoid circular implementation completion; caller requests one independent Review | Current plan, details and changes consistently assign continuation to parent | No material scope expansion or new critique needed | Justified clarification; publication is not falsely marked done. |

## Critique and Material Revision Assessment

* PC-001: direct no-scan/transaction disposition is implemented. _document uses require_clean, not forms._document or ensure_scanned. Pending/infected/deleted metadata tests prove the chosen scan separation. Its broader history-disclosure aim is not fully proven because actual missing blobs are omitted from those tests and disclosure preflight; see RV-001.
* PC-002: direct semantic disposition is implemented. Tests exercise six types, raw numeric acceptance followed by explicit correction, non-finite rejection, bool/int distinction, unknown/invalid controllers and an OR-true branch. Not every conditional branch is independently tested, but no additional semantic implementation defect was identified in the confirmed-input logic.
* PC-003: resolved by backend-qualified acceptance/documentation and the independent SQLite writer race test. Same-instance draft-version checks are not misreported as cross-process JSON protection.
* Original critique outcome remains Complete / Revise, unchanged; its disposition is not rewritten into an original pass.
* No significant divergent implementation decision or financial approval workaround was identified. No additional rpi-plan or rpi-research cycle is required to correct the two implementation defects.

## Plan Follow-Up Assessment

| Follow-up item | Why outside immediate scope | Owner or next action | Assessment and route |
| --- | --- | --- | --- |
| FU-FINANCE: actual template/source/rules/route/delegation | No approved authority supplied; every registered schema remains Unapproved | Finance/template owner supplies versioned actual decisions and evidence; parent reports requests in draft PR | Open distinct human follow-up, not a software defect and not a new active P01 task. |
| FU-BOARD: actual OD-12/15 inputs and restart ownership | No Board-approved envelope, liquidity/covenant/downside limits or restart authority supplied | Finance/Board/control owners supply approved scope, inputs and owners; parent reports requests in draft PR | Open distinct human follow-up; both #99 criteria remain unproven. |

These are known approval blockers, not research gaps that an agent can resolve by guessing. They neither justify invented figures nor require fictional approval APIs.

## Findings

<!-- rpi:review id=RV-001 -->
### RV-001 [Medium]: Historical values can be disclosed without available source bytes

* Related scope: P01-T01/P01-T02/P02-T01; missing-evidence non-disclosure and diagnostic snapshot safety.
* Evidence: src/core/src/zava_forward/core/form_review.py:84-105 validates historical evidence using metadata presence, scan status and source kind only. Actual blob reads occur only in _current at :108-114. _report at :194 short-circuits _current when the schema is stale; rejected/replaced historical evidence is not otherwise byte-checked. The report returns full history at :263, and view returns recorded diagnostics at :288.
* Constructed reproduction: used the existing test_form_staging.schema fixture and tiny in-memory records with a clean document metadata entry, a synthetic accepted D/history note, and a docstore.get that raises KeyError for the absent blob. With schema version 2 and a version-1 draft, _report returned D and the history note, marked both fields Stale, and made zero blob reads. With the latest schema restored to version 1 and the current field Rejected, it still returned historical D with zero blob reads.
* Test gap: src/core/tests/test_form_review.py:281-309 interprets missing as missing scan metadata or deleted document metadata. It does not cover an absent blob with retained clean metadata, historical-only evidence, or stale-schema short-circuiting. The component documentation's broader missing/deleted evidence disclosure guarantee is therefore not fully supported.
* Impact: an authorized endpoint can return retained values/reasons/manifests even though their required source is unavailable. Read/actions can bypass the intended availability preflight depending on current field/schema state. This does not establish unauthorized-role access or an infected-scan bypass; those guards are present.
* Destination: later rpi-implement.
* Smallest useful next action: make non-mutating availability preflight cover every distinct source represented in current/history/snapshots independently of freshness short-circuits. Preserve the no-scan and rollback contract and classify absent bytes versus storage-service failure explicitly. Add bounded regressions for missing current/historical blobs and schema-stale drafts without changing original evidence or weakening the guarantee.

<!-- rpi:review id=RV-002 -->
### RV-002 [Medium]: Conflict diagnostics silently count obsolete or no-longer-permitted candidate sources

* Related scope: P01-T01/P02-T01; exact-source freshness and field-specific deterministic diagnostics.
* Evidence: src/core/src/zava_forward/core/form_review.py:208-225 builds Unknown-field conflict alternatives from matching schema batches and an ID with scan.status clean. It does not check the staged source version/hash/kind, actual bytes or current field source policy. By contrast, _candidate at :118-150 refuses a candidate whose bound source is no longer current or permitted.
* Constructed reproduction: an Unknown epc field had two version-1 staged values D/E, while its sole clean document metadata entry was version 2. _report returned Conflict / Unreviewed source alternatives with zero blob reads, although neither staged candidate could pass the review source-freshness checks. The output did not identify that both alternatives were obsolete.
* Test gap: src/core/tests/test_form_review.py:249-265 proves two current permitted alternatives produce Conflict. The exact-source freshness test at :182-204 covers already-confirmed fields, not unknown-field alternative selection, leaving these two diagnostic paths inconsistent.
* Impact: current diagnostics and saved snapshots can present obsolete, changed-kind or unverifiable candidates as unqualified review alternatives, misleading the reviewer about what can actually be accepted. Held readiness prevents an approval bypass, but does not make the structural diagnostic accurate.
* Destination: later rpi-implement.
* Smallest useful next action: apply explicit current-source/policy qualification to conflict alternatives, or report historical/stale/unavailable alternatives separately with owned recovery reasons. Preserve original staging; do not silently relabel history as current evidence. Add a bounded stale-source/changed-kind conflict regression and assert exact diagnostic output.

## Defects

* RV-001: incomplete source availability preflight before historical disclosure; later rpi-implement.
* RV-002: unqualified obsolete/unusable alternatives in current conflict diagnostics; later rpi-implement.
* Neither defect requires Finance approval to correct; neither authorizes implementing the excluded approval-dependent functions.

## Routed Findings

| Finding | Destination | Owner or next action | Reason for route |
| --- | --- | --- | --- |
| RV-001 | rpi-implement | Parent routes non-mutating all-history source-availability correction and bounded regressions | Implementation falls short of accepted missing-evidence disclosure contract. |
| RV-002 | rpi-implement | Parent routes source-qualified conflict diagnostics and bounded regressions | Implementation diagnostic path does not use or disclose the source qualification required for review. |
| FU-FINANCE | Distinct human follow-up | Finance/template owner; report in draft PR | Missing authority, not a software defect or discoverable agent decision. |
| FU-BOARD | Distinct human follow-up | Finance/Board/control owners; report in draft PR | Missing actual approved inputs; not a fictional threshold task. |

Later implementation of routed findings does not require another Review. This record and its original outcome must be preserved.

## Residual Work

* The active parent owns any later disposition of RV-001/002, evidence commit and the explicitly requested single draft PR with Refs #96, Refs #98 and Refs #99. This review is not publication authorization or a gate receipt.
* Approved form preparation, approved-rule eligibility/calculation, actual reviewed application/claim export, full transitive downstream invalidation and actual Board gate/breach/restart/programme-wide enforcement remain outside this slice. They need future authorized scope after the human follow-ups, not automatic expansion here.

## Blockers and Remaining Work

* Software acceptance blockers for this candidate: RV-001 and RV-002 remain unresolved; no fixes were made during Review.
* Human approval blockers: FU-FINANCE and FU-BOARD remain Held. Preserve them in the draft PR and stop the dependent functionality.
* Active P01/P02 implementation markers are all checked. This Review found defects in that completed implementation rather than pretending its tasks never executed.
* #96 remains Partial: working field review/lineage and structural diagnostics are delivered, but approved binding/export/rule and full invalidation criteria are not proven.
* #98 remains Partial: isolated working field edits/history and diagnostic linkage are delivered, not approved validation or actual reviewed packs.
* #99 remains unproven on both criteria: null held inputs and a diagnostic Pause are not actual human-approved envelope/tolerances, breach containment, restart or programme-wide acceleration enforcement.
* No issue checkboxes, issue closures, human sign-offs, hosted checks, deployed health or operational acceptance are established by this Review.

## Validation Evidence

| Command or evidence | Scope | Status | Summary |
| --- | --- | --- | --- |
| Parent consolidated core unittest selection; finance-core-unittest.log | Forms, finance, grants, provenance and rescans | Passed, supplied execution independently read | Ran 199 tests in 63.263s; 54 existing optional SQL Server skips; 145 executed. Not rerun by reviewer. |
| From src/api: PYTHONPATH=../core/tests:../agents/tests python -m unittest discover -s tests -q; finance-api-unittest.log | Complete requested API unittest discovery | Passed, supplied execution independently read | Ran 1124 tests in 599.297s; 314 existing optional skips; 810 executed. Not rerun by reviewer. |
| Parent Ruff on touched Python and targeted mypy on new module/tests and HTTP tests | Changed Python | Passed as reported by parent/changes | No fresh independent lint/type execution claimed. Narrow untyped-helper accommodation inspected. |
| Parent changed documentation links/anchors | New sections of four touched Markdown files | Passed as reported by changes | Five relative links/anchors; review also read full changed documentation diff. |
| PYTHONDONTWRITEBYTECODE=1 external task-venv Python, stdin-only synthetic _report reproduction | RV-001/002 | Completed; defects reproduced | Existing schema fixture, in-memory records, no store/data files written; absent-blob historical disclosure and obsolete-source Conflict observed. |
| Preliminary reproduction import | Repro harness only | Failed setup, corrected | Initial optional helper class import did not exist; removed that import and used existing Store.require_clean. Not a source/test failure. |
| git diff --check; git rev-parse HEAD origin/main | Tracked whitespace and baseline | Passed | No whitespace errors; both SHAs match stated baseline. |
| Full --all, scoped --changed, deployment, Azure/SQL Server, browser, hosted CI and human acceptance | Outside authorized validation | Not run | Explicit caller restrictions; optional heavy gate unused. Existing optional test skips remain skips, not passes. |

External logs read:

* /home/azureuser/.copilot/session-state/8679bc17-dbcf-44f6-966b-ca6fddfb0ecf/files/finance-core-unittest.log
* /home/azureuser/.copilot/session-state/8679bc17-dbcf-44f6-966b-ca6fddfb0ecf/files/finance-api-unittest.log

The initial source import and successful reproduction used the existing external task venv. The repro is a narrow function-level execution, not a new package suite, backend durability run or endpoint integration proof.

## Outcome

* Review execution: Complete.
* Outcome: Not accepted.
* Rationale: two reproduced implementation gaps remain in the explicitly promised source-disclosure and exact-source diagnostic boundary. Broad passing parent tests do not cover those cases. The module otherwise preserves the intended independent, unapproved working-note and held-decision design.
* No significant divergent planning assumption or additional material research gap was identified. Missing actual financial authority is already honestly ledgered and must remain distinct from the software defects.
* The current documents and changes do not falsely claim full #96/#98/#99 acceptance. Their preserved partial/blocked claims are appropriate; the broad missing-evidence safety statement is subject to RV-001.

## Closeout Routing Record

| Finding class | Destination | Owner or next action |
| --- | --- | --- |
| Implementation defect | Later rpi-implement | Parent disposition of RV-001/002; no implementation or second Review performed here. |
| Decision gap or invalid assumption | None newly identified | Preserve accepted independent-slice scope; do not invent approval paths. |
| Material evidence gap | None newly routed to rpi-research | Actual Finance/Board decisions belong to named human follow-ups, not agent research substitution. |
| Non-blocking residual work for the independent slice | FU-FINANCE; FU-BOARD | Human owners supply actual decisions; blockers continue to apply to excluded issue acceptance. |

* Validation coverage: supplied local suites/log summaries assessed, code and tests read, two narrow defects reproduced; no new gate or broad test execution.
* Next owner: active parent. Retain the single critique and Review outcomes and disclose findings and held authority in the draft PR.

| Artifact | Description |
| --- | --- |
| [.copilot-tracking/plans/2026-10-27/finance-96-98-99-plan.md](.copilot-tracking/plans/2026-10-27/finance-96-98-99-plan.md) | Current checked independent-slice plan and human follow-ups |
| [.copilot-tracking/details/2026-10-27/finance-96-98-99-phase-details.md](.copilot-tracking/details/2026-10-27/finance-96-98-99-phase-details.md) | Reconciled operation, semantics and validation contracts |
| [.copilot-tracking/reviews/plans/2026-10-27/finance-96-98-99-plan-critique.md](.copilot-tracking/reviews/plans/2026-10-27/finance-96-98-99-plan-critique.md) | Preserved original Revise verdict and PC-001..003 |
| [.copilot-tracking/changes/2026-10-27/finance-96-98-99-changes.md](.copilot-tracking/changes/2026-10-27/finance-96-98-99-changes.md) | Implementation, local validation and honest issue matrix |
| [.copilot-tracking/research/2026-10-27/finance-96-98-99-research.md](.copilot-tracking/research/2026-10-27/finance-96-98-99-research.md) | Authority boundary and scoped issue evidence |
| [.copilot-tracking/reviews/logs/2026-10-27/finance-96-98-99-review.md](.copilot-tracking/reviews/logs/2026-10-27/finance-96-98-99-review.md) | This single Complete / Not accepted Review |

## Next Steps

Active parent: retain and report this Review, route RV-001/002 to a later rpi-implement disposition without another Review, and preserve both human follow-ups in the single draft PR using Refs #96, Refs #98 and Refs #99. Do not mark the candidate accepted or complete the held issue criteria. No user answer is required to identify the software corrections; actual Finance/template/Board decisions remain prerequisites only for the excluded dependent functions.
