---
title: Inventory-managed staff intake and independent QA 132 extension E2 details
ms.date: 2026-11-11
---

## Phase 1 and 2: helpers and case A

* `test_inventory_hold_after_capture_is_not_cleared_by_acknowledgement_or_qa`: staff capture on `ZF-3` (legitimate, before the hold), `tenure_inventory_record` with `households=None` through `/api/cases/ZF-3/resident`, `field-acknowledge` by Pam (200, still `Submitted`), `quality-accept` by Quil refused 409 with the inventory and tenure hold reasons, repeated after a store restart; quality state `Submitted`; GET case shows inventory view `Unknown`.
* Success criteria: no assertion in existing tests is changed; the existing non-inventory positive control still passes unchanged.

## Phase 3: case B

* `test_inventory_hold_after_acceptance_refuses_handover_and_a_later_capture_stays_held`: capture, independent accept (200, pre-hold), inventory hold, `quality-handover` with `resident_told` refused 409 and state remains `Accepted`; a later capture records `Submitted` (actual behaviour, not a refusal) and its independent accept is refused 409.
* Runs on both the SQLite base class and the JSON subclass; the MSSQL subclass stays env-gated and skipped.

## Phase 4: validation

* New cases, full `test_staff_intake_api`, Core `-k inventory`, Core gate selectors, API `-k inventory`, role endpoint inventory and dependency rule, Ruff check and format check, mypy.
* Staff intake browser and axe observation only under a non-blocking `flock -n` of the heavy lock, with the pinned axe 4.10.3 asset hash recorded.
