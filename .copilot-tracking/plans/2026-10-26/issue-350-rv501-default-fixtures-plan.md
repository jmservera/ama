<!-- markdownlint-disable-file -->
---
title: Issue 350 RV-501 default fixture correction plan and details
description: Prospective plan and phase details for correction cycle 1
ms.date: 2026-10-26
---

Prospective; written before the critique and any source edit.

* [ ] Phase 1: one independent critique; commit research, plan and critique before any source edit.
* [ ] Phase 2: add failing regressions first: default `bundle()` `case_write` and `ai` equal the runtime baseline, and a runtime-baseline field that the checker reads cannot be changed without the test failing.
* [ ] Phase 3: move `core_helpers` and `RuntimeFixture` above the helpers; cache baselines (`functools.lru_cache` keyed by outcome, returning `copy.deepcopy`); `case_write(outcome, restart)` and `ai_record()` return runtime-produced deep copies; `restart=False` is a mutation of the baseline flag; rename the 40-cap constructor use to `handcrafted_contact` with a comment on why; replace `SkipTest` with a clear failure.
* [ ] Phase 4: run `PYTHONDONTWRITEBYTECODE=1 /home/azureuser/rehearsal-350/venv/bin/python -m unittest tools.test_check_demo_feedback`; adapt tests that hard-code hand values to read them from the baseline without weakening assertions; remove `__pycache__`.
* [ ] Phase 5: one independent review; changes, state records; local commit; stop before any gate.

Details: runtime baseline for AI is `Store.ai_priority(user, 1)` with scripted `_chat` naming `ZF-4` and citation `Open safety issues: 1`; contact baseline is `RuntimeFixture.case_write()` for case `ZF-1`. A blocker is recorded if the checker contract cannot accept runtime shapes without a checker change.
