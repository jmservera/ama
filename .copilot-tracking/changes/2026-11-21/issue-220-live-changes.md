# Issue 220 live changes (2026-11-21)

Status: implementation starting. Planned: `resident_decisions.py` helper fix, one test, research note, index and log entries. The per-criterion table is completed at the end of this record.

## Changes made

* `src/core/src/zava_forward/core/resident_decisions.py`: `_same_signed_in_person` requires email and code to match and oid only when the roster row records one; `_owner_rights` uses it.
* `src/core/tests/test_challenge_signed_in_principal_220.py`: regression for an oid-less roster row.
* `docs/reference/research/issue-220-live-r8-oid-less-roster-2026-11-21.md`, index row, log entry.
* Evidence: `.copilot-tracking/evidence/2026-11-21/issue-220-live-r8/`.

Validation (tier FULL for src, coordinator runs gates; no `rpi-checks.py --all`): 491 related core tests OK (162 skipped); ruff clean; mypy 3 pre-existing errors in unrelated files. Hosted CI not read (no push).

## Per-criterion table

| Criterion | Status | Evidence / reason |
| --- | --- | --- |
| Digital and staff-recorded routes work | Ticked; offline proven, live blocked until redeploy | tests; live 403 |
| Explanations, owner, next update, resolution visible | Ticked; offline proven, no live challenge | core tests |
| Only dependent proposals and reviews stale | Ticked; offline proven | core tests |
| No consent, refusal, sanction, unrelated closure or hazard-clock change inferred | Ticked; offline proven, live refusals and unchanged hashes | r8 run1.out.txt |
| No retaliation, inferred refusal or delayed hazard response | UNPROVEN live: fix undeployed (redeploy not authorised); retaliation over time and hazard-response delay are production-only | r8 note |
