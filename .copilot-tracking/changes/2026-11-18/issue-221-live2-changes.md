# Issue 221 live2 changes (2026-11-18)

Refs #221. Docs and evidence only; no src change; Focused tier (no FULL trigger; `rpi-checks.py --all` not run). Earlier run artifacts `issue-221-live-*` are preserved unchanged; this run uses `issue-221-live2-*`.

## Added

* `docs/reference/research/issue-221-live-suspension-restart-evidence-2026-11-18.md`
* `docs/reference/research/operator-suspension-live-221-2026-11-18/` (probe script, two probe JSON files, drill test output, one screenshot)
* index entry in `docs/reference/README.md`, entry in `docs/reference/log.md`

## Per-criterion table (unticked criteria)

| Criterion | Status | Basis |
| --- | --- | --- |
| Guardrail breach record names restart authority per RULE-024 | Partly proven. Repository tests prove it; live record stores authority and RULE-024; deployed build accepted placeholder `TBD` (adverse) | `test-core-drill.txt` (6 OK), `live-probe-1-unintended-suspension.json` |
| Suspension and manual fallback drill is tested (NFR-014) | Repository drill proven; live suspension, AI block with manual route message and restart denial observed; live restart and witnessed operator drill unproven | `live-probe-2-while-suspended.json`; drills excluded; no `ai_restart` holder |

## Side effect and adverse evidence

* Probe 1 unintentionally opened `SUS-1` (scope `all`) on `ca-cutover-test-demo-api`. Not cleared: restart needs a distinct human with the `ai_restart` capability and the gate state is delete-protected. Owner decision recorded in the evidence note. No Azure resource was created.

## Validation

* `PYTHONPATH=src:tests python3 -m unittest tests.test_operator_suspension_drill -v` in `src/core`: 6 tests OK (raw output retained).
* mypy and ruff: not run; no `src/` or `infra/` file changed. The evidence probe script under `docs/` is not CI-checked and `ruff format` would reformat it (observed; raw output not retained).
* Hosted CI: not observed; no push.
