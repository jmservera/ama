---
applyTo: ".copilot-tracking/changes/2026-11-13/153-c1-remaining-notices-1713-changes.md"
---

<!-- markdownlint-disable-file -->
# Plan: issue 153 criterion 3 remaining notices

Details: [details](../../details/2026-11-13/153-c1-remaining-notices-1713-details.md). Research: [research](../../research/2026-11-13/153-c1-remaining-notices-1713-research.md).

## Phases

* [ ] Phase 1: add Owner and Next action to notices in `ops.js`, `assistants.js`, `simulator-control.js`, `staff-intake.js`, `panels.js`.
* [ ] Phase 2: extend `test_content_standard.py` so every covered notice module asserts ordered Owner and Next action.
* [ ] Phase 3: run `test_content_standard`, impacted screen tests, `ruff`, `mypy` in `/tmp/venv-153c1-1713`; review; commit.
