<!-- markdownlint-disable-file -->
# Phase Details: issue #126 restart follow-up

Plan: `.copilot-tracking/plans/2026-11-17/issue-126-restart-followup-plan.md`. External evidence root (outside the candidate): `/mnt/tmp/ama-run-81a96abb-126-20261117T1332/evidence-restart-126/` (called `EV`).

## P03-T01 Own-source install proof

* `git archive 23eca3a5551fe355969f07651660d1b2ce40ae5c src/core | tar -x -C EV/stage` (clean copy; no build metadata in the worktree).
* `python3 -m venv EV/venv` (no system site packages). Chosen command: from `<worktree>/src/core`, `env -i PATH=EV/venv/bin:/usr/bin:/bin HOME=EV/home TMPDIR=EV/tmp ZF_DATA=EV/data/zavaforward.json PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=<worktree>/src/core/tests EV/venv/bin/python -m unittest ...`. Run once first to record the missing-dependency report (`zava_forward` not importable), then `EV/venv/bin/pip install EV/stage/src/core` (pip only after that report; stdlib-only `dependencies = []`, setuptools build backend needs `setuptools>=77`; if the network is unavailable, record it and use `--no-build-isolation` with the venv's setuptools if present, otherwise blocker).
* Prove import path: print `zava_forward.core.<module>.__file__` for the six source modules (`data_protection`, `ai_registry`, `source_monitor`, `ledger_digest_blob`, `regulatory_privacy`, `challenges`) plus `ai`, and SHA-256 each against `git show 23eca3a5:src/core/src/zava_forward/core/<module>.py`; all must match; installed path must be under `EV/venv`.

## P03-T02 Six-module batch

* One command, single process, sequential: `python -m unittest -v test_data_protection test_ai_register_completeness test_source_monitor test_ledger_digest_blob test_regulatory_privacy test_challenges` from `src/core`, `PYTHONPATH=<worktree>/src/core/tests` only (`source_monitor_fixture` is in that directory). No `ZF_*MSSQL*`/model/credential variables. Local stdlib SQLite and JSON doubles inside the modules run and are labelled "local double, not SQL Server evidence" (critique PC-001); SQL Server opt-in classes skip and are unproven. Capture exit code, `Ran N`, `OK (skipped=K)` or failures, per-test skip reasons, log SHA-256 under `EV/run/`.
* A failure is recorded as a failure with the log; no re-run to mask it, no source edit. Any skip is reported as unproven.
* The orchestrator `test_source_monitor` is a different project module and is not run; stated in the update.

## P03-T04 External verifier (reconstructed; run after P03-T03, critique PC-002..PC-004)

* `EV/verify_table_refs.py` (not committed) is a reconstructed verifier, not the original inline script; its counts are reported separately from the parent's historical inline counts. Order: P03-T04 adds the table section first, then this script runs against the table and the logs, then script/output/table SHA-256 are recorded only in `EV/verify/` and the changes record (never inside the hashed table; the table section cites only the external path and script SHA-256). It resolves aliases `core/` to `src/core/src/zava_forward/core/` and `agents/` to `src/agents/src/zava_forward/agents/` before checks. Checks: referenced file exists and line within length, backticked symbol at or near the line, blob ids equal `git rev-parse 23eca3a5:<path>`, cited test ids appear as `ok` in available logs (new batch log always; parent batch logs only if still present, otherwise reported as not re-verified).

## P03-T03 Additive table update (before P03-T04)

* Append a section "Restart Follow-Up Update (2026-11-17, additive)" after Cross-Row Limits and before the Blob Index, or at the end, leaving all original row text unchanged. Content: new batch command/result/log references; per-row disposition (tier unchanged unless a directly relevant executed passed test covers the baseline gap and open items are human/qualified); MAP-01 context-only label with candidate unperformed tests; MN-3.2 tier rationale sentence; verifier evidence reference; unchanged absent approvals.
* Do not add a "closed" or "accepted" disposition for any row.

## P03-T05 Changes record and Review prerequisites

* Changes record lists files, commands, counts, skips, qualifications, witness records (including the disclosed stray first record), validation and not-performed items; plan markers reconciled; then witness `implement-done`.

## Witness protocol

`python3 tools/rpi_phase_witness.py record --repo <worktree> --issue 126 --evidence-dir /mnt/tmp/ama-run-81a96abb-126-20261117T1332/evidence --state <abs state> --session rpi-126-restart --actor worker --claim-model claude-sonnet-5.5 <event>`; artifacts persisted and state updated before each event; `commit-complete --claim-commit <SHA>` only after the actual commit.
