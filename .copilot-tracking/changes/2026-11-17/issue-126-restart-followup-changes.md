<!-- markdownlint-disable-file -->
# RPI Changes: issue #126 restart follow-up

* Task slug: `issue-126-restart-followup` (parent `issue-126-residual-source-assessment`)
* Plan: `.copilot-tracking/plans/2026-11-17/issue-126-restart-followup-plan.md`
* Details: `.copilot-tracking/details/2026-11-17/issue-126-restart-followup-phase-details.md`
* Deliverable: additive section in `.copilot-tracking/changes/2026-11-17/issue-126-residual-source-assessment-table.md`

## Execution Status

* Status: Complete for P03 (Implement); P04 Review and P05 commit follow
* Completed markers: P01, P02, P03, P03-T01..P03-T05; remaining: P04, P05
* Blockers: none

## Completed Work

* P03-T01: staged `git archive 23eca3a5 src/core` and a venv outside the candidate under `/mnt/tmp/ama-run-81a96abb-126-20261117T1332/evidence-restart-126/` (EV). Probe in the empty venv: `ModuleNotFoundError: No module named 'zava_forward'` (`run/probe-missing-dependency.log`). Then `pip install` of the staged core succeeded (`run/pip-install.log`). `run/own-source-proof.txt`: 11 modules (six under test plus `ai`, `lawstore`, `rulecards`, `rule_engine`, `ledger`) SHA-256 equal to the start-commit blobs and under the venv; `ALL_MATCH_AND_UNDER_VENV True`.
* P03-T02: one sequential command from `src/core`, `env -i` (PATH, HOME, TMPDIR, ZF_DATA external), `PYTHONDONTWRITEBYTECODE=1`, `PYTHONPATH=<worktree>/src/core/tests`: `python -m unittest -v test_data_protection test_ai_register_completeness test_source_monitor test_ledger_digest_blob test_regulatory_privacy test_challenges`. Result: exit 0, `Ran 125 tests in 1.272s`, `OK`, 0 skipped. Per module 32, 5, 29, 22, 18, 19. Log `run/batchC.log` SHA-256 `b2ffa2db3661bdf7dc271b868626b50744c5c40db368fdaedc4b7d302b95fcf9`. Single project (`src/core`); the orchestrator `test_source_monitor` is a different module and was not run. Local JSON/SQLite doubles and a fake blob transport only; not SQL Server, Azure, real-model or human evidence.
* P03-T03: appended "Restart Follow-Up Update" to the existing table (38 insertions, 0 deletions against the start commit; original text unchanged): batch C record, per-row dispositions for 7 rows (T-RAI-001, GOVERN-AUDIT-01, MAP-02, GOVERN-AUDIT-04, MAP-05, MEASURE-03, MN-2.3), MAP-01 context-only label, MN-3.2 rationale, verifier reference. Tiers unchanged for all 22 (1 source-tested, 1 proposed, 20 insufficient, 0 observed, 0 accepted, 0 closed).
* P03-T04: reconstructed external verifier `EV/verify/verify_table_refs.py` (SHA-256 `2807748302e94fe4f94b8f386d2e59684546a544a160a22c525de0c8db629cd5`), output `EV/verify/verify-output.txt` (SHA-256 `b220938be20873a9568b07dd0fc86c9fb2674a310d0a0d0a24c2521380b0e423`) run against the table with SHA-256 `2b7f725d08cfaf0a073046fa82726f02f525cd81d30635dcc93a9b4a755e1e5c`: 68 path:line references, 0 bad; 42 symbol-near-line checks, 42 matched; 42 blob rows, 0 mismatches; 27 qualified test ids all defined in test sources; the 23 distinct test names in the new section all have `ok` in batch C (the 12 other bare names in the "not in logs" output line are module names, not tests). Qualified parent ids from batches A/B cannot be checked against passed results because the parent logs are not retained at their original location (`ama-run-74bd1fe9...` path absent); this is a reconstructed verifier, so its counts (68/42/42/27) differ from and do not replace the parent's historical inline counts (69/44/38/27).
* Source scope: `git status --short` shows only the modified table plus untracked `.copilot-tracking/` files; no application, test, SQL, config, workflow, policy, requirement, agent or skill file changed; no `log.md` or `memory.md` edit.

## Disclosures

* Witness: the first `research-open` call used a wrong `--evidence-dir` and wrote a stray record to `evidence/issue-126/issue-126/events.jsonl` (seq 1, qualification "missing observed predecessor: launch"); it is retained and not deleted. The valid sequence is in `evidence/issue-126/events.jsonl`.

## Validation Record

| Check | Scope | Status | Evidence |
| --- | --- | --- | --- |
| Own-source proof | 11 installed core modules vs start blobs | Passed | `run/own-source-proof.txt` |
| Six-module unittest batch | `src/core` | Passed (125 run, 0 skipped) | `run/batchC.log` |
| Reconstructed reference verifier | table incl. new section | Passed (0 bad refs, 0 blob mismatches) | `verify/verify-output.txt` |
| Additive table diff | table vs start commit | 38 insertions, 0 deletions | `git diff --stat` |

## Qualifications and Limits

* Witness records are locally writable observations: not tamperproof, not host or model attestation, not proof of unobserved reasoning; actor, session and model labels are asserted. A first mis-directed `research-open` call wrote a stray record to `evidence/issue-126/issue-126/events.jsonl` (retained, disclosed above); the valid chain is `evidence/issue-126/events.jsonl` (launch seq 1, research-open seq 2, plan-done seq 3, implement-start seq 4).
* Focused validation tier: tracking-only evidence and an additive tracking table update, no executable or control change; the complete local gate, hosted CI, independent exact-head assessment and human approvals are not supplied here. HVE not applicable.

## Not Performed

* SQL Server, browser, container, Azure, real-model, human-study, full suites, the orchestrator `test_source_monitor`, the candidate MAP-01 ranking tests, any register write; qualified owner, DPO, Legal, Finance, restore and EU-applicability approvals; issue ticks or closure; publication.

## Post-Review Handling

* Review executed once (witness `review-done` seq 6), outcome Partial: `.copilot-tracking/reviews/logs/2026-11-17/issue-126-restart-followup-review.md` (unchanged after the witness record). Criteria A, B, C, E, F, G passed; D failed on one claim.
* Finding 1 (Medium): the MAP-01 wording "does not exercise `_support`" was overstated (the cited test runs the ranking function, which can call `_support`; the `support_unknown` reason is not asserted). Corrected after Review in the table's follow-up section ("not asserted" wording); tier and context-only label unchanged. Because the table changed after the Review and after the earlier verifier run, the table SHA-256 `2b7f725d...` and the P03-T04 counts above describe the pre-correction table; the final-HEAD verifier rerun and hashes are recorded in the final report and external `evidence-restart-126/verify/` outputs.
* Findings 2 and 3 are disclosure items already recorded here.
