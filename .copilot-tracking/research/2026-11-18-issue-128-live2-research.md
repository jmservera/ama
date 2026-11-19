# Research: issue #128 live audit, run 2 (2026-11-18)

Status: opened. Task: audit #128 against repo and live synthetic demo, desktop only, FOCUSED tier, docs/evidence only.

Prior run (preserved, committed on main): `.copilot-tracking/*/2026-11-18-issue-128-live-*` and
`docs/reference/research/issue-128-live-equity-evidence-2026-11-18.md`. That run's evidence kept only summary
lines of the core tests and no route inventory. This run re-executes with retained commands and raw output.

Unticked criterion: "Direct user research protocol agreed; usability measures aggregate only".
Owner decisions: DPO/Legal approval, person-run AT testing and billing reconciliation are not needed for the demo.

## Findings

* One unticked criterion. Repo: protocol is a draft with blank agreement record; usability_programme.py enforces aggregate-only, masking below 5 and audit-use agreement; 26 core tests pass; no participant or usability storage in src/api/src.
* Live: axe 4.10.3, 0 violations on 4 desktop pages; /openapi.json and /docs return 404.
* Research disposition: executed. Planning Readiness: Ready.
Evidence: `.copilot-tracking/evidence/2026-11-18/issue-128-live2/`.
