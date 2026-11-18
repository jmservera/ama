# Changes: issue 189 live evidence (2026-11-18)

Divergence recorded honestly: the evidence note, index and log entries were drafted during Research, before the `implement-start` witness call. No source file under `src/`, `infra/` or `tools/` changed.

Files: `docs/reference/research/issue-189-simulator-run-controls-live-evidence-2026-11-18.md` (new), `docs/reference/README.md` (index paragraph), `docs/reference/log.md` (entry).

Validation (FOCUSED, documentation only): `python3 -m unittest tests.test_simulator_run_controls_189 tests.test_simulator_run_budget_controls` in `src/core`: 32 tests OK. mypy, ruff and web checks not applicable (no source or web change). Hosted CI not observed (no push). `rpi-checks.py --all` not run, by instruction.

## Per-criterion table

| Criterion | Result | Basis |
| --- | --- | --- |
| Cost estimate recorded before any run (ticked) | Proven (consistent) | Estimate helper output: B1, 1 unit, 30 messages. |
| Quota headroom against tier from #140 (ticked) | Proven (consistent) | Live hub B1 capacity 1; 400000 per day quota. |
| Run has an owner | Proven in code; hub tag only live | Hub `owner` tag live; RUN_OWNER_REQUIRED refusal in code. |
| Run has a time limit | Unproven live; proven in code | RUN_DEADLINE halt; no simulator job deployed, deployment is a production-affecting owner step. |
| Run has a budget alert | Proven (configuration) | USD 25 budget, 80 percent actual and 100 percent forecast alerts enabled; firing not demonstrated (no spend, no drills). |

Overall: the issue criterion stays unticked pending a deployed run; Refs #189 (not Closes).
