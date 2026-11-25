# Changes r14

## Files

* `src/api/checks/assistant_real_ai_acceptance.py`: `admitted()` accepts the listing's `"in force"` marker (observed live) instead of an object with an `id`.
* `src/api/tests/test_assistant_real_ai_acceptance.py`: fixture and admission test updated.
* `docs/reference/research/issue-107-live-r14-release-records-2026-11-25.md`, `docs/reference/README.md`, `docs/reference/log.md`: evidence note, index, log.
* `.copilot-tracking/evidence/107-live-r14/`: redacted scripts and outputs.

## Azure changes (demo, resource group ama)

* `ca-cutover-test-demo-api`: appended the demo user's app identity to `ZF_ASSIST_RELEASE_APPROVERS` (revision 0000076, healthy). Not reverted; owner asked for the demo user to be an approver.
* Temporary `Cognitive Services OpenAI User` role assignment for the az login user on the AI account: created and deleted.
* Five release records created through the API (ids in `post_releases.json`); kept.

## Validation (tier FULL by src edit; rpi-checks --all not run)

* `unittest tests/test_assistant_real_ai_acceptance.py`: 8 OK; ruff check, ruff format --check, mypy in `src/api`: clean.
* Live: five POSTs 201; listing shows five "in force". Harness live runs: 0 measured tokens (401, then 403 public access disabled).

## Divergences

* The harness could not complete the live batch; no network or allowance control was changed.

## Per-criterion table

| Unticked criterion | Status | Evidence |
| --- | --- | --- |
| Independent SQL connection/worker and race tests cover material mismatches, revocation and restart; old images/restarts cannot restore revoked approval or replenish finite allowances | Unproven in this pass (proven for 11 of 13 fields in r12 on constructed fixtures; no real older image) | r12 note |
| A matching approved exercise record permits bounded proposals only; delivered-build acceptance needs version-linked real AI, actual SQL and Azure evidence (CON-009/AC-057) | Partly proven: five actual release records in force on the deployed build (201, bounded-proposals note). Unproven: real-AI tokens (0 measured; AI account private-endpoint only; app invoke off without operator allowance) | r14 note; `post_releases.json`, `diag_status.txt` |
