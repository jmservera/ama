# Issue 222 live2 research (2026-11-18)

Task: issue-222-live2. Refs #222. Research disposition: executed (opened). Existing state `issue-222-live-state.json` is preserved untouched; this run uses `issue-222-live2-state.json`.
Prior evidence: docs/reference/research/cohort-evaluation-demo-2026-11-18.md (offline only; output not retained; blocker count mismatch noted).
Goal: re-run cohort evaluation, retain raw output, probe live synthetic demo (rg ama) read-only, per-criterion proof.

## Findings

* Prior note (merged #1927) stated seven blockers; raw re-run shows eight `insufficient_sample` plus one `unapproved_thresholds`. Retained raw output now under `docs/reference/research/evaluation/cohort-eval-live-2026-11-18/`.
* Evaluation modules (`cohort_ranking_eval`, `cohort_ai_eval`) are deterministic fixtures; they do not read live data and carry no approval.
* Live demo (`ca-cutover-test-demo-api`, Running, revision 0000031, read-only GETs): `/healthz` 200; unauthenticated `/api/ranking` and `/health` 401; signed-in staff `/api/ranking/policy` 200, `/api/ranking/snapshot` 200 with 443 entries each carrying rank and reason codes but no cohort or lawful-field attributes; `/api/ai/priority` 200 with a null recommendation. Shape only retained; identifiers dropped. A screenshot showing resident names was deleted (identifiers).
* Live data cannot supply cohorts or lawful fields; OQ-018 approval is not provable for the demo.
* Planning Readiness: Ready.
