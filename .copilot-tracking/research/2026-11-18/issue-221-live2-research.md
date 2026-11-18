# Issue 221 live demo research (2026-11-18)

Refs #221. Scope: synthetic desktop demo; owner decisions of 2026-11-18 apply (live Azure authorised, rg `ama`, cap USD 700, no drills, no Key Vault rotation, no production change). Focused tier; src changes would raise it to FULL, so none are made.

## Research disposition

Disposition: executed. Unticked criteria: (5) guardrail breach record names restart authority per RULE-024; (6) suspension and manual fallback drill tested (NFR-014). Baseline code: `src/core/src/zava_forward/core/continuity.py`, `restart_authority.py`; test `src/core/tests/test_operator_suspension_drill.py`. Prior note on the same repository tests: `docs/reference/research/issue-221-restart-authority-and-drill-evidence-2026-11-18.md`.

## Findings

* Local: `tests.test_operator_suspension_drill` 6 tests OK (`test-core-drill.txt`). Covers placeholder, AI-named, self-designated and unappointed authority refusals, multi-actor separation, and an end-to-end suspension, manual fallback, hazard and restart drill.
* Live (`ca-cutover-test-demo-api`, revision 0000031, image digest sha256:5368f4e4...): a probe meant to prove refusals instead created an open suspension of scope `all` (`SUS-1`). The first negative request, restart authority `TBD`, was accepted by the deployed build (HTTP 200, authority stored as `TBD`); the repository code refuses it (`_PLACEHOLDER_PATTERNS`), so the deployed image predates that check or differs from the worktree. The following three negative requests were refused only because `all` was by then already suspended, so they do not prove the authority refusals live.
* While suspended: AI run returns a template with a suspension reason naming the manual route (hazard duties never paused); cases remain readable; restart-propose, restart-decide and automatic-restart flags all return 403; no account holds the OID-bound `ai_restart` capability.
* The gate state cannot be deleted by design (SQL triggers `continuity_gate_no_delete`, monotonic epoch); restoring would need a decide by a distinct authorised human or a PITR restore. Neither was performed.

## Planning readiness

Ready: record evidence note, per-criterion table, unintended-side-effect disclosure. No source edit.
