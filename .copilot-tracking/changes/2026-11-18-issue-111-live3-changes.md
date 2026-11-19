# Changes: issue 111 live3

Docs and evidence only; no src change; Tier FOCUSED (documentation and evidence, no gate-tool or infrastructure change). No Azure resource created or modified; read-only `az containerapp show`.

## Per-criterion table

| Criterion | Proven for the demo? | Basis |
| --- | --- | --- |
| C1 Outputs reproducible from retained readings (ticked) | Proven as engineering evidence, not newly endorsed | 26 core sensor tests OK; live payload `retained-reading-view-v2`, repeat read same content (one earlier byte-hash difference unexplained) |
| C2 Thresholds sourced or labelled exercise values (ticked) | Proven | `EXERCISE_LABEL` and `ANALYSIS_VERSION` in `sensor_analysis.py`; label validation |
| C3 R1 to R3 complete before beyond-exercise use (unticked) | Unproven, not provable for the demo | Needs named R2 reviewer/Asset sign-off, R3 agreed limits, R1 standards texts; gate only in PR #1641 |

## Files

* docs/reference/research/issue-111-live3-sensor-evidence-2026-11-18.md and issue-111-live3-raw/
* docs/reference/README.md, docs/reference/log.md
* .copilot-tracking artifacts for live3 and the state file

## Validation

* `cd src/core && PYTHONPATH=src:tests python3 -m unittest tests.test_sensor_analysis tests.test_sensor_non_authority`: 26 tests OK (expected failures=1).
* Live probes: see raw files. mypy/ruff not applicable (no source change).
* Hosted CI not read (not pushed).
