# Research: #1259 unusable ranking archive paths (live demo lane, run 2)

Date: 2026-11-18. Disposition: executed (reuses the run-1 note at docs/reference/research/2026-11-18-ranking-archive-unusable-1259-failing-first.md as prior evidence). Planning Readiness: Ready.

Open question: run 1 recorded the red-before result as observed with raw output not retained, and used a mocked stat failure. Can the unticked criteria be proven with retained raw output and real-filesystem synthetic runs, without any model or cloud call?

Unticked criteria: AC4 (regressions plus failing-first) and AC5 (FULL receipt, exact-head assessment, hosted checks).

Plan: re-run the red-before overlay and a real-filesystem CLI reproduction (regular file, dangling link, absent directory) and record raw output; read hosted CI state for the fix commit; no src change; no Azure action (filesystem logic).
