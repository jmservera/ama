# Issue 76 hazard clock and owner plan (2026-11-14)

Research: [.copilot-tracking/research/2026-11-14-issue-76-hazard-clock-owner-research.md](../research/2026-11-14-issue-76-hazard-clock-owner-research.md)

* [x] Add additive clock fields in `taskqueues.context`: `kind` (Hazard or Safeguarding), `accountable_owner` (named, else explicit `ESCALATION_OWNER`), `clock_text` (elapsed hours, target window, response state in words).
* [x] Render `clock_text` and `Accountable owner` in `workSummary` with a fallback owner when the payload omits it. No colour-only meaning, no new aria attributes.
* [x] Add `src/api/tests/test_workbench_hazard_clock_owner.py` (core payload plus real JS render via node).
* [x] Focused validation: new and neighbouring tests, mypy and ruff with /tmp caches in `src/core` and `src/api`.

Critique (single pass, final candidate): compatible with confirmed decisions; existing `owner` semantics retained; no significant divergence.
