# Issue 2203 research

Research disposition: executed. Planning Readiness: Ready. Tier: FOCUSED (docs only; no src change).

Findings: [live evidence note](../../../docs/reference/research/issue-2203-runbook-live-2026-11-21.md).

* Runbook `docs/capstone/demo/runbook.md` (468 lines) carries a five-home 2026-11-12 target section and live-route text that predates the 20-home, 5-minute simulator with a 10/10 consent mix (#184 note, 2026-11-20).
* `src/core/tests/test_generated_dataset.py` parses the `### The five homes` table (5 rows, fixed headers). Constraint: relabel that section, never remove it or change its header or row count.
* Live probes ran against the demo (staff and resident); results are in the evidence note.
* Gaps that cannot be proven live: offline-24h alert, deployed resident checkbox, operator-triggered AI scope, wrong-role denial.
