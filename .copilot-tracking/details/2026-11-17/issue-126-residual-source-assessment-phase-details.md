<!-- markdownlint-disable-file -->
# Phase Details: issue #126 residual and unassessed-check source assessment

Plan: `.copilot-tracking/plans/2026-11-17/issue-126-residual-source-assessment-plan.md`

## P02 Row evidence capture

For each ID, a row carries: baseline status, severity and verdict (report 2026-10-14, baseline `1cb398c7`); current assessed commit `01baf8d3`; code references as `path:line symbol`; test references as `path::Class.method` or file; blob ids from `git rev-parse HEAD:<path>`; version evidence (`REGISTRY_VERSION`, `EVALUATION_VERSION`, PRD 0.21.0, distribution 0.1.0, or "none recorded"); accountable ROLE (report remediation roles; inferred for unassessed rows and labelled); disposition tier; test evidence id; missing evidence; resume condition.

* Role labelling (PC-001): roles are shown as "proposed role (report remediation checklist)" for residuals and "inferred role (this assessment)" for unassessed rows; no accepted delegation or appointed person is implied.
* Version fields (PC-004): separate `task_id/task_version`, `release_version` and (EU rows) `applicability/nonapplicability` columns. Registry, evaluation or PRD versions appear only as "related version evidence", never substituted for an approved task/release version; absent approvals are stated.
* Vocabulary mapping (PC-005): `implemented/source-tested` = implemented/source-tested; `deployed-observed` = observed; `proposed`; `insufficient`; `independent-acceptance` = independently accepted. Observed and independently accepted are listed as unavailable (no external evidence) for every row.
* Disposition rules: `implemented/source-tested` only where HEAD source and a test directly cover the narrow control named in the row and the batch result passes; a control gap or absent human/real-model/restore/privacy/legal evidence is `insufficient`; design or checklist-only items are `proposed`. `deployed-observed` and `independent-acceptance` are never assigned without recorded external evidence (none exists).
* A row may state a narrow source-tested component while its overall disposition remains `insufficient`; the table shows both columns (control component, overall disposition).

## P03 Bounded verification

* Test-evidence rule (PC-002): a `implemented/source-tested` claim names the specific executed and passed test(s) (from verbose output); skipped or unrun tests never support it. Batch pass counts alone are not row evidence.
* Sanitised environment (PC-003): run under `env -i` with only PATH, HOME under the evidence root, `TMPDIR` under the evidence root, `PYTHONDONTWRITEBYTECODE=1`, `ZF_DATA` under the evidence root and the `PYTHONPATH` below; no `ZF_*MSSQL*`/`ZF_TEST_MSSQL` or other inherited `ZF_*` variables. Confirm afterwards that `git status --short` shows only RPI tracking paths.
* Environment: `PYTHONPATH=<worktree>/src/core/src:<worktree>/src/agents/src:<worktree>/src/api/src:<worktree>/src/core/tests:<worktree>/src/agents/tests:<worktree>/src/api/tests`; `ZF_DATA` set to a directory under the external evidence root; run from `/tmp` to prove no cwd shadowing; `timeout` on each batch.
* Batch A (core, pure unit): `test_governance`, `test_rai_release_invalidation`, `test_rai_threshold_live_approval_guard`, `test_recovery`, `test_paired_equity`, `test_cohort_eval`, `test_monitoring_coverage`, `test_human_review_effectiveness_223`, `test_heldout_eval`.
* Batch B (api and agents): api `test_assistants`, `test_assistant_release`, `test_rai_harm_threshold_incident`, `test_restart_audit`; agents `test_chat_eval`.
* Opt-in MSSQL, browser, container, Azure and full-suite commands are excluded; skipped counts are reported as skipped.
* Failures are recorded verbatim and reflected in rows; no test or source is edited to make them pass.

## P04 Assemble

* Table artifact: `.copilot-tracking/changes/2026-11-17/issue-126-residual-source-assessment-table.md`.
* Changes record: `.copilot-tracking/changes/2026-11-17/issue-126-residual-source-assessment-changes.md` (created before implement-start with status in progress, finalised at implement-done).
* Mechanical check script is run from the shell and its output copied into the changes record; the script is not committed.

## P05 Review

One original Review log at `.copilot-tracking/reviews/logs/2026-11-17/issue-126-residual-source-assessment-review.md` over the 22 rows, using inline verifier evidence (re-run of the existence check and spot re-reads), lineage and fidelity, and gaps. Findings route to later work; no second Review.
