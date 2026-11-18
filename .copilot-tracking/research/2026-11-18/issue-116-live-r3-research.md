# Issue 116 live research, round 3 (2026-11-18)

Research disposition: executed. Planning Readiness: Ready.

Open criteria: OD-14/OD-19 reason roles; provider-boundary allowlists; output permission recheck; document AI derivative/necessity.
Prior rounds: docs/reference/research/issue-116-live-demo-evidence-2026-11-18.md and the r2 note.

Findings: one employee role only (Retrofit Programme Manager); second role unobtainable (no directory privilege; resident account not in Entra). New angle: sweep all 88 GET paths in `src/api/tests/test_role_endpoint_inventory.py` live and count literal reason values. First sweep gave 379 false positives from the word "None" (kept as adverse); corrected sweep gives 0. Seven endpoints return 500 and nine 503 for this role (out of scope, noted). Offline tests re-run green. Outcome: no criterion can be ticked.
