---
title: Issue 134 demo preflight research
ms.date: 2026-11-13
---

## Evidence read

* `docs/capstone/demo/runbook.md` (five-home table; seed 20260901, as-of 2026-10-13). It states the regression does not check damp history, sensors, simulator cohort, AI scope or the private store.
* `src/core/tests/test_generated_dataset.py`: `test_runbook_five_home_cohort_is_reproduced_by_seed_and_as_of` builds the seed with a fictional test register and asserts open, no hazards, property type and stage only.
* `Store(data_path)` loads a JSON seed and exposes `home_case_view(user, id)` and `detail(id, user)`; no network needed. `src/api/tests/test_case_journey.py` runs shipped JavaScript via node (present); no browser.
* Case-record key names for damp history, sensors and conflicts are unconfirmed; the script will introspect keys rather than assume them.

## Findings and gaps

* Local facts are limited to the fictional-register replay; deployed store, simulator cohort and AI scope stay Not run.
* Scope is tracking-only: no `src/` or `docs/` edits.

Research disposition: executed. Planning Readiness: Ready.
