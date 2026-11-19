# Research: issue 223 live audit (run 2, 2026-11-18)

Refs #223. Disposition: executed (re-verification of the earlier note `docs/reference/research/human-review-effectiveness-live-demo-2026-11-18.md`). Planning Readiness: Ready.

Scope: synthetic desktop demo, tier FOCUSED, no src change planned, no rpi-checks --all. Live Azure only for the existing apps; no resource created.

Questions: re-run offline gate and focused tests; re-prove live review retention; classify each unticked criterion; separate production-only items.

## Findings

* Prior note and code exist: `src/agents/.../review_effectiveness.py`, `src/core/.../human_review_effectiveness.py`, golden file, 43 tests.
* Offline gate exit 0, passed true, 11 checks true; 37 + 6 tests OK.
* Live: reject without reason 400; reject with reason 200 with reviewer, reason, source hashes, compared outputs retained; second review 400.
* Live app has template-only summaries; no seeded-defect set, no model task. Seeding is a src change (FULL tier), out of scope.
* Evidence: `.copilot-tracking/evidence/2026-11-18/issue-223-live-r2/`; note `docs/reference/research/issue-223-live-r2-2026-11-18.md`.

Planning Readiness: Ready.
