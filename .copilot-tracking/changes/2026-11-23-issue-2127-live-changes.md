# Changes: issue 2127 (live)

Tier: focused (documentation and evidence only; no src change, no rpi-checks run).

## Files

* docs/reference/research/issue-2127-run-controls-live-2026-11-23.md (new evidence note)
* docs/reference/README.md (index row), docs/reference/log.md (entry)

## Per-criterion table

| Criterion | Proven | Unproven or owner-gated |
| --- | --- | --- |
| Run has an owner | Code and 11 tests; hub and job owner tags live | Per-run owner inside mounted control.json not read live |
| Run has a time limit | Code cap 3600 s; live replicaTimeout 270 s, one-shot schedule | Bicep says 240, live 270 (drift, owner to reconcile) |
| Run has a budget alert | Live actual80 and forecast100 on a hub-scoped USD 25 budget | Email delivery not exercised (no drills); recipient is an .invalid placeholder address |

Excluded by owner decision (not needed for demo): billing reconciliation, DPO/Legal approval, person-run AT testing. Azure estate unchanged.
