<!-- markdownlint-disable-file -->
# RPI Changes: issue #126 residual and unassessed-check source assessment

* Task slug: `issue-126-residual-source-assessment`
* Plan: `.copilot-tracking/plans/2026-11-17/issue-126-residual-source-assessment-plan.md`
* Details: `.copilot-tracking/details/2026-11-17/issue-126-residual-source-assessment-phase-details.md`
* Deliverable: `.copilot-tracking/changes/2026-11-17/issue-126-residual-source-assessment-table.md`

## Execution Status

* Status: Complete for declared scope P02, P03, P04 (P01 completed in Research; P05 Review follows)
* Completed markers: `P01`, `P02`, `P02-T01`, `P02-T02`, `P03`, `P04`; remaining active-plan markers: `P05` (Review phase)
* Blockers: none

## Completed Work

* P02: 22 rows (11 residuals, 11 unassessed) assessed against HEAD `01baf8d3df86a28f754da8545d0e8f12012bf350` with baseline status/verdict, code references with line numbers, executed-and-passed tests, version evidence (none recorded for task/release), proposed or inferred accountable role, tier and missing-evidence/resume condition. Files: the table above (new).
* P03: two bounded batches, own-source `PYTHONPATH`, sanitised `env -i`, no SQL opt-ins. Batch A: exit 0, 251 tests, OK, 18 skipped (SQL opt-in). Batch B: exit 0, 270 tests, OK, 67 skipped (SQL opt-in). Logs and SHA-256 are in the table and under `evidence-126-assess/run/`.
* P04: mechanical verification (inline, nothing committed): 69 `path:line` references are within file length and 44 sampled symbol-at-line checks matched; 38 blob-index identities match `git rev-parse HEAD:<path>`; 27 cited test ids found as executed and passed (one, `test_failed_audit_write_rolls_back_revocation_and_denies`, prints a stderr line before `ok`, confirmed passed at log line 492-493 of batch A).
* Source scope: no application, test, SQL, config, gate, agent or policy file edited. `git status --short` shows only `.copilot-tracking/*/2026-11-17/` additions.

## Outcome Counts (assessment, not closure)

* implemented/source-tested (component, not closed): 1 (GOVERN-AUDIT-02); proposed: 1 (MN-4.1); insufficient: 20; observed: 0; independently accepted: 0; closed: 0 of 22.

## Implementation-Time Plan and Detail Updates

* Local judgment: `test_data_protection` and four other related modules were left unperformed because of the two-batch cap; rows citing them state "unperformed" in their HEAD tests line. No plan structure changed.
* The research artifact was recreated once after the witness `research-open` record because the edit tool cannot overwrite; its opening text is preserved at `evidence-126-assess/research-opening-snapshot.md`.

## Validation Record

| Check | Scope | Status | Evidence |
| --- | --- | --- | --- |
| Batch A unittest | 9 core modules | Passed | 251 run, 18 skipped, exit 0 |
| Batch B unittest | 4 api modules, 1 agents module | Passed | 270 run, 67 skipped, exit 0 |
| Reference existence and blob match | table references | Passed | inline script, output summarised above |
| Source boundary | worktree | Passed | only untracked RPI tracking paths |

## Not Performed

* Full suites, SQL Server, browser, container, Azure, real-model, human-study and `test_data_protection` runs; qualified owner/DPO/Legal/EU decisions; any register write.

## Follow-Up Items

* Per-row resume conditions in the table (human, DPO/Legal, real-model, witnessed restore, EU applicability).
* Authorised later bounded batch for `test_data_protection`, `test_source_monitor`, `test_ledger_digest_blob`, `test_regulatory_privacy`, `test_challenges`, `test_ai_register_completeness`.
* Publication of this candidate requires separate authorisation (none given).
