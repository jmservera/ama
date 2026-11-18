<!-- markdownlint-disable-file -->
# Task Research: issue #126 restart follow-up (six-module batch and three evidence-quality gaps)

## Status

* Phase: Research (opened 2026-11-17 after the coordinator launch record; opening text persisted before substantive research)
* Research disposition: executed (read-only repository inspection of the parent table, review, changes, READMEs, test modules and rows; no external, cloud or private data)
* Planning Readiness: Ready
* Task: `issue-126-restart-followup`, parent `issue-126-residual-source-assessment`; state `.copilot-tracking/rpi-sessions/2026-11-17/issue-126-restart-followup-state.json`

## Scope and Lineage

* Start commit `23eca3a5551fe355969f07651660d1b2ce40ae5c` on `docs/rai-residual-source-assessment-126`; current main `f1df574bba2b94cd83bb2a783079ec94cd584c90` is separate provenance, not this assessment's source.
* Local only. No publication, approval, private data, capture, deployment, paid calls, production access or signature authority.
* Original records of the parent task (state, research, plan, details, critique, changes, table, Review) remain unchanged except one small additive current-update of the existing 22-row table.

## Bounded Objectives (from coordinator brief)

1. Execute the deferred six-module batch (`test_data_protection`, `test_ai_register_completeness`, `test_source_monitor`, `test_ledger_digest_blob`, `test_regulatory_privacy`, `test_challenges`) from their documented component directories, own-source install proof, clean environment, external retained logs.
2. Address three low evidence-quality gaps: thin MAP-01 test linkage, MN-3.2 tier rationale, unretained inline verifier scripts (retain exact helper externally).
3. One plan critique, one original read-only Review; no issue ticks or closure.

## Findings

* F1 source unchanged: `git diff --name-only 01baf8d3 HEAD` lists only the eight `.copilot-tracking/*/2026-11-17/` parent files; HEAD tree `27c0c2d9bb39746b016b669a59c63a4ac07ea154` differs from the assessed tree `d10bd7a918779f770da471fd3c54d8a61e14883e` only by those files. The parent table's "HEAD `01baf8d3`" source claims therefore stay valid for the start commit.
* F2 witness record: the first `research-open` call used `--evidence-dir .../evidence/issue-126` (wrong; the tool appends `issue-126` itself) and wrote a stray record to `evidence/issue-126/issue-126/events.jsonl` (seq 1, qualification "missing observed predecessor: launch"). It is retained, not deleted. The valid `research-open` is seq 2 in `evidence/issue-126/events.jsonl` after the coordinator launch seq 1. Both disclosed in the changes record.
* F3 module locations: all six modules exist in `src/core/tests/` (`test_data_protection`, `test_ai_register_completeness`, `test_source_monitor`, `test_ledger_digest_blob`, `test_regulatory_privacy`, `test_challenges`). A same-named `src/orchestrator/tests/test_source_monitor.py` is a different module (it tests `zava_forward.orchestrator.source_monitor`); the parent table's `test_source_monitor` row text (MAP-05) refers to `core/source_monitor.py`, so only the core module is in the batch and the orchestrator module is named as not run. The batch is therefore single-project (`src/core`); no api/agents module is in it, so no cross-project sequencing is required beyond one process.
* F4 documented command shape: `src/core/README.md` (source-monitor section) runs from `src/core` with `PYTHONPATH="$PWD/tests"` and an installed-distribution venv python (`python -m unittest discover -s tests -p ...`); the README also documents `PYTHONPATH=src:tests` for module runs. `src/core/pyproject.toml` has `dependencies = []` (extras `sql`, `blob`, `iothub`, `dev` are opt-in), so a stdlib-only install suffices for these modules; `test_source_monitor` imports the local `source_monitor_fixture` helper in `src/core/tests/`.
* F5 environment: system Python 3.12.15 has installed `zava-forward-{core,agents,api} 0.1.0` whose provenance against the start tree is unproven, so the batch uses an external venv with an external staged copy (`git archive HEAD src/core`) installed with pip into the venv, then hash-proves the installed module files equal the worktree files. Planned order: run the chosen command in an empty venv first, record the missing-module report, then `pip install` the staged own-source directory.
* F6 skip risk: `test_data_protection` and sibling modules contain SQL-named cases (for example `DSR-SQL-01`); opt-in SQL Server classes are skipped without `ZF_*MSSQL*` variables. Any skip stays unproven, not pass. Counts and skips are taken from the unittest verbose log, not from this research.
* F7 affected rows (grep of the table for the six modules): T-RAI-001 and MAP-02 (`test_data_protection`), GOVERN-AUDIT-01 (`test_ai_register_completeness`), GOVERN-AUDIT-04 (`test_data_protection`, `test_regulatory_privacy`), MAP-05 (`test_source_monitor`), MEASURE-03 (`test_challenges`), MN-2.3 (`test_ledger_digest_blob`). Update only after the logs show which cited behaviours the executed tests exercise; no tier changes without a directly relevant passed test, per the table's tier rule.
* F8 MAP-01 linkage: the cited `test_paired_equity...test_ai_task_paired_evaluation_and_transparent_non_ai_comparison` does not call `ranking._support` (confirmed by parent Review finding 2). Existing candidate tests that touch the behaviour (not run in this follow-up and outside the six-module batch): `src/api/tests/test_ranking_policy.py`, `src/agents/tests/test_cohort_manifest_draft.py` (`ties_with_no_adds_support_unknown_reason`). No new test is written. The additive qualification re-labels the cited test as context only and records these candidates as unperformed.
* F9 MN-3.2 rationale: the table's own tier rule makes `implemented/source-tested` conditional on the baseline finding's engineering gap being covered by a directly relevant passed test with only human or actual-environment gates left. MN-3.2 baseline gap includes model-retirement and change review (baseline PARTIAL), and the cited tests cover invalidation only; GOVERN-AUDIT-02's baseline gap is the change binding itself, which those same tests do cover. The explicit distinction is therefore the retirement-review half of MN-3.2, which has no engineering test; this will be stated as a one-sentence rationale, not a tier change.
* F10 verifier retention: the parent changes record says the 69 `path:line`, 44 symbol, 38 blob and 27 test-id checks ran inline and were not retained. Plan: write one external helper script outside the candidate (evidence directory), run it against the table and logs, retain its source hash, output and a hash of the table, and cite them by external path and SHA-256. No reusable tool is added to the repository.
* F11 focused-tier basis: the only repository changes are `.copilot-tracking` Markdown/JSON evidence and one additive update to an existing tracking table; no application, test, SQL, config, workflow, gate-tool, dependency, Dockerfile, policy, requirement, agent or skill file changes, so no control or gate semantics change. HVE is not applicable (no behaviour-bearing instruction authorship). Full tier, hosted CI and human approvals remain outside this task.

## Constraints and Boundary

* No publication, remote, deletion, stash, amend or rebase. Never edit `docs/reference/memory.md` or `docs/reference/log.md`. Original Review and parent artifacts preserved unchanged.
* Witness record is a locally writable observation: not tamperproof, not host or model attestation; asserted actor, session and model labels are not observed.
