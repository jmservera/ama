# Changes: issue #128 live run 2

Refs #128. Docs and evidence only; no src change; FOCUSED tier (no `rpi-checks.py --all`).

## Per-criterion table

| Criterion | Result | Basis |
| --- | --- | --- |
| Direct user research protocol agreed | Unproven | Draft only; agreement record has no named person or date; demo waivers are not agreement |
| Usability measures aggregate only | Proven at source level (demo) | 26 core tests OK; no participant/usability storage in src/api/src; live route inventory 404 so live absence not proven |
| Keyboard and screen reader (ticked, deferred #1907) | Unproven, production-only | Person-run AT not needed for demo; axe 0 violations on 3 loaded desktop pages (the resident signed-in scan ran on a loading page and is not counted) |

Ticked criteria (human review of missing data; RAI cohort set) not re-audited.

## Files

* docs/reference/research/issue-128-live2-equity-evidence-2026-11-18.md (new)
* docs/reference/README.md, docs/reference/log.md (index, log)
* .copilot-tracking/evidence/2026-11-18/issue-128-live2/ (evidence)
* .copilot-tracking/{research,plans,details,changes,reviews}/2026-11-18-issue-128-live2-*; critique under .copilot-tracking/critiques/2026-11-18/
* .copilot-tracking/rpi-sessions/2026-11-18/issue-128-live2-state.json (new; run 1 state file unchanged)

## Validation

* `cd src/core && PYTHONPATH=src:tests python3 -m unittest test_usability_programme test_journey_register`: 26 tests OK.
* Playwright live proof: rc 0, axe 0 violations. mypy and ruff: not applicable (no Python source changed).
* Markdown link and diff review.
