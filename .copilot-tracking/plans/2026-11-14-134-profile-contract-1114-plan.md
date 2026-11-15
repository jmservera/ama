---
title: "#134 profile journey contract helper plan"
ms.date: 2026-11-14
---

* [x] Add `profile_journey_contract.py` with `validate` (blockers only, `accepted` always false) and `gaps` (derived from the walkthrough register).
* [x] Add `src/core/tests/test_profile_journey_contract.py`.
* [x] Run ruff check, ruff format --line-length 100 --check and focused unit tests in `src/core`.
* Critique (single pass): compatible; no UI edit, no acceptance claim, no push. Tier: focused (non-gate core helper).
