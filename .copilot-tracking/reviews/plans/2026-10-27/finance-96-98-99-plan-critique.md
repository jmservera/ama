<!-- markdownlint-disable-file -->
# RPI Plan Critique: Finance draft review and held decisions

## Metadata

* Task ID: finance-96-98-99
* Critique date: 2026-10-27
* Plan: .copilot-tracking/plans/2026-10-27/finance-96-98-99-plan.md
* Phase details: .copilot-tracking/details/2026-10-27/finance-96-98-99-phase-details.md
* Critique execution status: Complete
* Verdict: Revise
* Severity summary: 0 Critical, 1 High, 2 Medium, 0 Low
* Assessment: single final-candidate critique; one complete actionable finding set.

## Inputs and Criterion Boundary

* Read the supplied plan, phase details and research in full. Checked research C1..C9 against forms.py, change_provenance.py, grants.py, Store.detail and the HTTP form handlers; inspected the directly relevant SQLite writer, scan helpers, existing form tests and component typing configuration.
* Checked PRD FR-038..043 and AC-046..051/053/054, BRD RULE-010..012 and OD-12/15, and ADR 0006. Read the required project context, reference index, owner memory and relevant housing-association primer context. Memory supplies preferences, not authority.
* Retrieved the explicitly scoped GitHub issues #96/#98/#99 and prerequisite #97, including comments, on 2026-10-27. The latest #97 comment confirms engineering completion with every schema still Unapproved. Earlier fictional proposal material does not supply actual authority.
* The caller authorizes one draft PR covering all three issues with Refs unless all criteria are proven. Missing human decisions must be durably held; implement the independent slice and stop dependent functionality. No invented amounts, approved templates, financial rules, envelopes or tolerances.
* Approved-rule validation, reviewed packs, transitive downstream approval invalidation, approved tolerance breaches and restart are expressly excluded. Their absence is not a request to expand this candidate.
* Validation boundary: local relevant tests only; no full --all gate. At most one locked --changed is permitted for a large change, not required for this bounded slice. This critique neither ran tests nor initiated implementation, publication, another critique or any follow-on lifecycle.
* P02-T01's ownership and limits remain fixed: no test removals, at most two new core test classes and six added HTTP methods in the existing class. Findings below must fit that ownership, using subtests and existing fixtures where useful.

## Coverage Assessment

| Requirement, research, phase, or task ID | Coverage | Evidence or concern |
| --- | --- | --- |
| User delivery boundary; P02-T02 | Covered | One draft PR to main, Refs #96/#98/#99, no issue checkbox edits or merge, explicit partial/blocked acceptance matrix. No whole-issue success implied. |
| FR-038/039; C1/C2; W1; #97 | Covered within boundary | Exact registered unapproved schema and immutable staging can support working notes only. Approved preparation remains blocked. |
| FR-040; AC-048/053; P01-T01 | Partial | Individual decisions, history, source/reason, actor and no authoritative side effects are specified. The scan/save interaction needs PC-001; value interpretation needs PC-002. |
| FR-041; AC-049; P01-T01 | Partial | Confirmed-only draft diagnostics and permanently held approved readiness are correct. PC-002 addresses deterministic type/condition semantics, not missing approved calculations. |
| FR-042; AC-050/054; P01-T01 | Covered within boundary | Diagnostic manifest binds fields, evidence, versions, attachments and history; not a reviewed pack, submission, eligibility finding or financial state change. AC-050 remains blocked. |
| FR-043; AC-051; P01-T01/P02-T01 | Covered within boundary | Bound-source versus all schema-bound stale sets, prior values and unrelated decisions are specified. Read/action-time draft freshness is not transitive approval invalidation; full AC-051 remains unproven. |
| C6/C9; P01-T02 | Covered as a requirement | Dedicated authenticated endpoint, strict keys, current actor, ordinary-detail/private-key stripping and quarantine non-disclosure are explicit. Tests must cover manifests and historical values/reasons, not only current fields. |
| C7; P01-T01/P02-T01 | Partial | Controlled rollback, SQL actor recheck, reopen and failure injection are appropriate foundations. PC-001 covers nested scanner commits; PC-003 corrects the backend concurrency claim. |
| C8; RULE-010 | Covered | Existing synthetic designation is not generalized into actual Finance/template/Board approval. Authority-bearing categories remain forbidden. |
| RULE-011/012; OD-12/15; #99 | Covered within boundary | Durable missing-decision records with null approval/amount inputs, actor/time, owner role and correction path; diagnostic Pause only. Neither #99 criterion is fully satisfied. |
| Held-decision ledger; P01-T01/P02-T01 | Covered as a requirement | Per-case durable records and JSON/SQLite reopen are specified. Template/rule authority and Board limits must both appear in the evidence; a Board hold on a case is not a programme-wide gate. |
| ADR 0006; P02-T01 | Covered | Core module and external tests, reused synthetic fixtures, no UI/model/dependency expansion, focused core suites, complete requested API discovery and relevant Ruff/mypy. Narrow typing integration is allowed; blanket suppression would not prove checking. |
| P01 to P02 dependencies | Covered | Core controls precede the adapter; validation precedes documentation/publication. Human authority blocks only explicitly excluded dependent functionality. |

## Verdict

* Verdict: Revise.
* The selected independent slice is credible and the financial authority boundaries are honest. Missing Finance/Board decisions do not block planning or implementation of working review notes and held records.
* Three bounded planner corrections are needed before implementation: explicitly separate source scan commits from review mutations, define typed diagnostic interpretation, and scope concurrency guarantees to the actual storage mechanisms. None requires new financial figures, approval machinery, expanded test ownership or a full gate.
* Whole-issue acceptance for #96, #98 and #99 remains partial or blocked regardless of a later engineering test pass.

## Findings

<!-- rpi:critique id=PC-001 -->
### PC-001 [High]: Separate source scanning from the review mutation transaction

* Related IDs: C2/C7, P01-T01, P01-T02, P02-T01; field isolation, rollback and quarantine requirements.
* Evidence: .copilot-tracking/details/2026-10-27/finance-96-98-99-phase-details.md:26-30 requires controlled writes while reusing forms helpers and checking clean current sources. src/core/src/zava_forward/core/forms.py:299-308 calls ensure_scanned in _document; its staging write explicitly reacquires the case after a possible scan save. src/core/src/zava_forward/core/doc_controls.py:158-186 shows that scans can save, audit, remove document metadata and delete infected bytes. src/core/src/zava_forward/core/change_provenance.py:108-163 bases rollback/committed-outcome handling on the case snapshot. src/core/tests/test_form_staging.py:242-291 already exercises post-scan save failure and conflict.
* Concern: The candidate does not say whether review evidence validation is non-mutating or can invoke that saving scan helper, nor when review/hold mutations occur relative to it. Merely wrapping both in controlled does not make an intermediate scan save part of one atomic review transaction. A scan can persist partial working edits, clear SQLite touched-case tracking, or make rollback confuse a scan commit with a completed review. JSON restoration must also not resurrect metadata for quarantined/deleted evidence.
* Impact: The promised no-partial-review and no-source-side-effect guarantees can fail, and quarantine recovery can become inconsistent, even though final save failure tests pass on already-clean sources.
* Smallest useful change: Specify a source preflight before any review/history/hold mutation. Either require already-clean evidence and return an owned recovery response for pending/missing scans, or complete permitted scans separately, then reacquire current case/actor/source, recheck draft version and re-enrol the case before the review transaction. Do not silently include source scanning in the pure diagnostic path. Distinguish any separately committed scan/quarantine event from review success or failure.
* Action owner: Planning parent, P01-T01/P01-T02 author.
* Exact resolving evidence: Revised phase details with the chosen operation order and backend rollback boundary; P02-T01 cases for pending/missing scans, clean and infected outcomes, and final review audit/save failure or conflict after preflight. Assert no review/hold success or partial history, retained legitimate quarantine outcome, no hidden historical disclosure, and JSON/SQLite reopen. Reuse existing classes/fixtures within the fixed limits.
* Decision route: Direct planner correction. No user response or financial authority is needed.

<!-- rpi:critique id=PC-002 -->
### PC-002 [Medium]: Define raw-to-typed draft values and conditional comparison semantics

* Related IDs: C1/C2, FR-040/041, P01-T01, P02-T01; draft type and conditional-required diagnostics.
* Evidence: src/core/src/zava_forward/core/forms.py:23 defines string, integer, number, boolean, date and enum types; _scalar permits several Python scalar types. stage_candidates stores raw_value as text, not a parsed schema-typed value. The schema allows typed enum options and required_when equals values. .copilot-tracking/details/2026-10-27/finance-96-98-99-phase-details.md:28-30 introduces manual scalars and confirmed-only type/condition checks without defining how accepted raw text becomes a typed input.
* Concern: A valid sourced number/boolean/date can remain a string and falsely fail, or permissive conversion can silently alter evidence. Python equality can conflate True and 1 in enum membership or conditions. The candidate also leaves multiple required_when predicates and unknown/invalid controlling fields undefined. These are engineering semantics, not missing Finance calculation authority.
* Impact: Two plausible implementations can produce different required-field and conflict results for the same confirmed inputs, undermining the deterministic independent slice.
* Smallest useful change: Specify whether acceptance preserves raw text with explicit typed correction, or uses a small documented deterministic conversion contract while retaining raw evidence. Define exact supported type/date/finite-number checks, type-aware enum/condition equality, the combination of required_when predicates, and Unknown behavior when a controlling input is absent, invalid or stale. Do not infer units, currency conversions or unapproved formulas; report unsupported verification as not evaluated.
* Action owner: Planning parent, P01-T01 author.
* Exact resolving evidence: Revised diagnostic/value contract and bounded table-driven P02-T01 coverage for all six supported field types, bool-versus-integer ambiguity, invalid date/non-finite input, typed enum membership, multiple conditions and missing/stale/invalid controlling values. Confirm unreviewed candidates never become condition inputs and readiness stays held.
* Decision route: Direct planner correction within draft diagnostics; not a request for financial rule approval.

<!-- rpi:critique id=PC-003 -->
### PC-003 [Medium]: Bound concurrency acceptance by backend rather than imply JSON cross-writer protection

* Related IDs: C7, P01-T01, P02-T01; optimistic version and persistence acceptance.
* Evidence: .copilot-tracking/plans/2026-10-27/finance-96-98-99-plan.md:63 combines JSON/SQLite reopen, rollback and concurrent-writer conflict without a backend qualification. src/core/src/zava_forward/core/store.py:44-59 loads JSON once with an instance-local RLock; save at :102-108 replaces the whole file without checking a persisted revision. src/core/src/zava_forward/core/sqlstore.py:665-700 uses a database writer transaction and rowversion comparison. controlled reuses these mechanisms; it does not add JSON file-level concurrency control.
* Concern: A draft version compared against one JSON Store instance protects stale requests to that instance, but not another independently opened Store holding an older copy of the same file. Both can accept the same draft version and overwrite one another. The existing JSON mechanism cannot support an unqualified multi-writer claim.
* Impact: Evidence from same-instance stale requests or SQLite conflicts could incorrectly be reported as durable concurrency protection for both backends.
* Smallest useful change: State the supported boundary explicitly: JSON is single-Store/single-writer with in-instance optimistic draft checks; SQLite owns cross-instance concurrent-writer protection. Document that distinction in acceptance, tests and component guidance. If cross-process JSON support is instead intended, plan actual persisted revision/locking work rather than infer it from controlled; do not broaden the slice implicitly.
* Action owner: Planning parent, P01-T01/P02-T01 author.
* Exact resolving evidence: Backend-qualified acceptance text; stale-version tests for each supported backend and a two-independent-SqlStore conflict test with reopen/history/audit assertions. JSON documentation must not claim cross-process protection absent its implementation and proof.
* Decision route: Direct planner correction to align the independent slice with existing storage architecture; no user response is required to avoid the unsupported claim.

## Strengths and Residual Risk

* Accepting a working field never satisfies an approval. Original staging, sibling fields, consent, ranking and finance/grant states remain unchanged; history and manifest lineage are explicit.
* The source-disclosure requirement correctly covers quarantined historical values/reasons, ordinary staff detail and contractors, not just hiding UI controls. Retaining history internally does not authorize returning it after its source becomes unavailable.
* Current registered actor checks, strict server-owned keys, exact source/schema bindings, isolated case persistence and typed/local test ownership are suitable foundations, subject to the findings.
* The held ledger is an honest deliverable: absence is recorded with null approved inputs, ownership and recovery routing. No zero/default envelope, artificial tolerance breach, restart authority or live programme hold is invented.
* Source/schema freshness is intentionally read/action-time and draft-only. Full rule/input transitive invalidation and re-export blocking remain excluded and unproven, not silently counted as AC-051.
* A diagnostic manifest cannot satisfy a Finance-reviewed application/claim export. Explicitly accepted scope excludes that dependent behavior.
* No request is made to remove tests, expand the fixed class/method limits, run --all, consume the optional heavy gate, change checks/protection, or start a retry loop.

## Questions or Blocking Evidence Gaps

* No additional human answer is required to resolve PC-001..003.
* Actual template/source/rule approval, reviewer delegation and route authority remain Finance/template-owner decisions. OD-12 envelope/liquidity/covenant evidence and OD-15 downside tolerances remain Finance/Board decisions. Preserve them in the held ledger and draft PR; stop the dependent functionality.
* These missing inputs block full issue acceptance, not this critique's execution. A passing engineering review must not tick or close the currently unmet issue criteria.

## Limitations

* This is a plan credibility assessment, not an implementation review, runtime test result, independent exact-head approval, hosted check or publication authorization.
* The research's reported 17-test baseline was not rerun or independently reproduced. It is not evidence that the planned module already exists or passes.
* No private datasets, Azure resources, secrets, financial approvals or new regulatory-currentness claims were accessed or created. Review stayed within the supplied artifacts and directly relevant cited evidence.
* Existing untracked plan/research/state inputs were left intact. Only this critique artifact was written.

## Recommended Next Action

* Highest-impact finding: PC-001.
* Action owner: Planning parent.
* Smallest next action: Specify non-mutating evidence checks or separate scan preflight, then make the typed-diagnostic and backend concurrency corrections directly in the plan/details and record all three dispositions.
* User response required: No for these planner corrections. Finance/Board responses remain prerequisites only for the excluded dependent behavior.
* This single critique is complete. Preserve it unchanged; return to the active planning parent for direct disposition without another critique or automatic follow-on execution.

| Artifact | Description |
| --- | --- |
| [.copilot-tracking/plans/2026-10-27/finance-96-98-99-plan.md](.copilot-tracking/plans/2026-10-27/finance-96-98-99-plan.md) | Assessed final-candidate plan |
| [.copilot-tracking/details/2026-10-27/finance-96-98-99-phase-details.md](.copilot-tracking/details/2026-10-27/finance-96-98-99-phase-details.md) | Assessed phase details |
| [.copilot-tracking/research/2026-10-27/finance-96-98-99-research.md](.copilot-tracking/research/2026-10-27/finance-96-98-99-research.md) | Supplied evidence synthesis |
| [.copilot-tracking/reviews/plans/2026-10-27/finance-96-98-99-plan-critique.md](.copilot-tracking/reviews/plans/2026-10-27/finance-96-98-99-plan-critique.md) | Complete single critique and finding set |

## Next Steps

Active planning parent: resolve PC-001..003 directly, retain this original outcome and finalize the independent-slice boundary. No user action is required for those corrections. Stop here; no implementation, tests, publication or peer lifecycle stage is invoked by this critique.
