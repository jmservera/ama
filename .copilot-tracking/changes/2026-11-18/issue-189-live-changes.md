# Changes: issue 189 live (2026-11-18)

Docs and evidence only; no src change; FOCUSED tier (classification basis: no source, workflow, infra or SQL edit). Note: the evidence files were created during research, before this record and before the implement-start witness; the witness is observational and this order is recorded honestly.

Files: docs/reference/research/simulator-run-controls-live-189-2026-11-18.md and its folder (login.py, probe.py, local_exercise.py, three raw outputs); docs/reference/README.md; docs/reference/log.md; .copilot-tracking artifacts.

## Per-criterion table

| Criterion | Proven | Evidence or reason it cannot be proven |
| --- | --- | --- |
| Cost estimate for N homes before any run (ticked) | Proven, consistent | B1 allocation and capacity rows; observed spend USD 5.16 (retained raw) |
| Quota headroom against #140 tier (ticked) | Proven, consistent | B1 capacity 1 live; 135 messages in 24 h; N=5000 refused (retained raw) |
| Run has an owner | Proven for demo | Hub owner tag live; blank owner refused offline |
| Run has a time limit | Unproven live | Enforced in code (expiry required, 14 day cap; offline start/stop retained). No simulator job exists; admin role grant not authorised |
| Run has a budget alert | Configuration proven; firing unproven | USD 25 budget with two enabled notifications; control has no alert field; firing needs spend to threshold |

## Validation

* `python3 docs/reference/research/simulator-run-controls-live-189-2026-11-18/local_exercise.py` with PYTHONPATH set: ran as recorded.
* Live probe: staff 403 on all admin paths. No resource created, nothing to delete.
* Not run: src tests, mypy, ruff (no source change); rpi-checks --all (prohibited).
* Link and diff review of the markdown.
