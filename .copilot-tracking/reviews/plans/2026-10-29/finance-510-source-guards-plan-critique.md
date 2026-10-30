<!-- markdownlint-disable-file -->
# RPI Plan Critique: Finance review source guards

## Metadata

* Task ID: finance-510-source-guards
* Critique date: 2026-10-29
* Plan: .copilot-tracking/plans/2026-10-29/finance-510-source-guards-plan.md
* Phase details: .copilot-tracking/details/2026-10-29/finance-510-source-guards-phase-details.md
* Critique execution status: Complete
* Original verdict: Pass
* Severity counts: Critical 0; High 0; Medium 0; Low 0

## Inputs and Criterion Boundary

* Caller requirements: independently assess the single final candidate for RV-001 and RV-002 on PR #510, branch docs/finance-96. Do not implement, delegate or alter source artifacts. Write only this critique.
* Research considered: .copilot-tracking/research/2026-10-29/finance-510-source-guards-research.md, claims C1-C6.
* Source evidence inspected: src/core/src/zava_forward/core/form_review.py; src/core/src/zava_forward/core/documents.py; src/core/src/zava_forward/core/change_provenance.py; src/core/src/zava_forward/core/doc_controls.py; src/core/tests/test_form_review.py; the schema, batch and store fixtures in src/core/tests/test_form_staging.py; relevant source-policy references in src/core/src/zava_forward/core/forms.py and the working-review contract references in src/core/README.md.
* Repository context: required case-study and knowledge-base introductory material, plus read-only working-tree inspection. The supplied plan, details, research and session-state files were already untracked. No source changes were present in that inspection.
* Decisions and dependencies: bounded full RPI loop; local commit only; no push, Azure or rubric-score edits; no generated targets or removals; at most eight new methods in the existing external test file; existing JSON/SQLite fixtures; requested core checks and related staging tests.
* Assessment boundary: implementation readiness of FR1-FR4, non-functional cache/error/read-only requirements, AC1-AC6 and P01/P02. This assessment does not establish implementation correctness, successful validation, actual PR comment provenance, financial authority, publication readiness or hosted approval.

## Coverage Assessment

| Requirement, research, phase, or task ID | Coverage | Evidence or concern |
| --- | --- | --- |
| RV-001; FR1-FR2; C1/C3 | Covered | P01-T01 requires independent byte reads before disclosure, including stale-schema and rejected/replaced states. This addresses the current schema-gated `_current` call and metadata-only `_visible`. |
| Retained traversal; AC1; P01-T01 | Covered | Current fields, both prior/new history evidence, stored diagnostic fields/history and attachment source records are explicitly named. Snapshot-only retention is a required regression, so traversal cannot rely solely on live history. |
| Availability versus historical freshness; C1/C5 | Covered | Research explicitly preserves history when bytes remain available despite historical version mismatch. The plan separates document digest availability from exact-tuple freshness rather than requiring historical evidence to become current. |
| Cache scope; AC3; C5 | Covered | The digest cache is local to a report/action, shared between action preflight and its resulting report, never stored globally. Standalone reports start afresh. Candidate acceptance retains independent validation. |
| Exact identity and field policy; FR3; C6; P01-T02 | Covered | Freshness stays memoized by ID/version/hash/kind, while policy is checked per field outside that cache. Existing distinct-identity and shared-source tests remain unchanged. |
| Missing versus outage; FR2/FR4; AC5; C3 | Covered | Only the byte-reader's missing-source KeyError is translated. Alternatives catch DocumentUnavailable only; DocumentStoreError propagates. Retained-source failure denies the report rather than excluding returned evidence. |
| RV-002; FR3-FR4; C2/C6 | Covered | Alternatives must match case and exact schema/digest, select the relevant non-human-only field, satisfy source policy and pass `_current`, including actual bytes. Unusable alternatives are excluded without staging edits. |
| Conflict controls; AC4; P01-T02 | Covered | Required matrix includes valid conflicting alternatives, version/hash/kind/byte drift, missing bytes, pending/deleted/generated metadata and field-disallowed kinds. Persisted diagnose output and staging retention are included. |
| Non-mutation and persistence; AC2; C4 | Covered | Both stores, durable records, failed-action versions/audit, source-write/scan spies and existing rollback behavior are included without widening staging or storage implementation scope. |
| Test ownership; P01-T03 | Covered | External FormReview class only; maximum eight additions with bounded helpers and parameterized coverage feasible using the existing dual-store fixture. No removals or generated outputs. |
| Validation; AC6; P02-T01 | Covered | All four exact requested core commands and related staging tests are listed. Baseline failure of the new regressions is required before accepting the fix; missing tooling requires actual failure evidence first. |
| Independent Review and local delivery; P02-T02 | Covered | One later independent implementation Review, preserved original outcome, privacy-safe identity and local commit are planned. No push, Azure, rubric edit or publication-gate claim is authorized. |

## Verdict

* Verdict: Pass
* Rationale: the final candidate addresses both supplied defects with a coherent availability/freshness split, explicit retained-snapshot traversal, field-specific policy checks outside tuple caching, and narrow exception handling. It supplies regression and persistence obligations within the locked test surface. No substantive plan correction or unresolved user choice is identified from the supplied boundary.
* This is the original independent critique verdict, not a disposition of an earlier adverse critique or an implementation acceptance.

## Findings

No actionable PC findings. Critical 0; High 0; Medium 0; Low 0.

## Strengths and Residual Risk

* Separate caches serve separate questions: document-ID digest reuse proves availability/read economy, while exact-source tuple memoization determines currentness. Neither substitutes for per-field policy.
* The distinction between retained and unreviewed sources is explicit: missing retained bytes deny disclosure; unusable unreviewed alternatives do not become conflicts.
* Existing history remains intact, including when source metadata changes but bytes are still available. Failed checks do not authorize a rescan, source save or deletion.
* Tests must still demonstrate the promised traversal and error behavior. Passing this critique does not accept a missing snapshot-only regression, cross-report cache, swallowed outage or weakened existing read-count assertion.
* No implementation residual risk waiver is inferred. Tool availability and actual check results remain validation dependencies, not reasons to substitute or claim checks.

## Questions or Blocking Evidence Gaps

None for implementation readiness. No significant or divergent user decision is required.

## Limitations

* Read-only static assessment; no application, unit-test, formatter, linter or type-check execution was performed.
* Research claims were checked against the bounded source and test evidence, not live storage services or private data.
* The final implementation, independent implementation Review and local commit do not yet exist as assessed evidence.
* The complete publication gate remains outside this local-only critique; no exemption for future publication is established.

## Recommended Next Action

* Highest-impact finding: none.
* Action owner: planning parent.
* Smallest next action: record the Pass disposition without changing this original critique, then proceed to P01-T01 under the confirmed bounded RPI request.
* User response required: no.

| Artifact | Description |
| --- | --- |
| [.copilot-tracking/plans/2026-10-29/finance-510-source-guards-plan.md](.copilot-tracking/plans/2026-10-29/finance-510-source-guards-plan.md) | Assessed final candidate |
| [.copilot-tracking/details/2026-10-29/finance-510-source-guards-phase-details.md](.copilot-tracking/details/2026-10-29/finance-510-source-guards-phase-details.md) | Assessed implementation and validation details |
| [.copilot-tracking/research/2026-10-29/finance-510-source-guards-research.md](.copilot-tracking/research/2026-10-29/finance-510-source-guards-research.md) | Supplied C1-C6 research |
| [.copilot-tracking/reviews/plans/2026-10-29/finance-510-source-guards-plan-critique.md](.copilot-tracking/reviews/plans/2026-10-29/finance-510-source-guards-plan-critique.md) | Original Complete / Pass critique |

## Next Steps

The active planning parent may finalize the plan and continue with P01-T01. No user action is required. This independent worker stops after recording this critique; it does not implement, run another agent or commit.
