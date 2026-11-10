---
title: Issue 131 E1 missing households key (details)
ms.date: 2026-11-10
task_id: 131-extension1-1110
---

## Phase 1 test

In `test_resident_decisions.py` add `test_inventory_missing_households_key_is_malformed_but_null_is_unknown` after the existing corrupt-history test. Setup as that test (scope, two reports, record an inventory, trigger, second revision), then inject histories under the store lock plus `save`:

* `missing key singleton`: the first good revision without `households`.
* `missing key earlier revision`: good revision without `households` as version 1 followed by a valid version 2.

For each, assert the view is Malformed, the gate lists "malformed" first and the hold last, scope is refused with no mutation, and the writer with the right `expected_version` is refused with no mutation (`unchanged_failure`). Control: history with `households=None` reads Unknown, and the writer appends the next revision, which survives reopen. Types: typed locals, no casts.

## Phase 2 fix

`_inventory_history_ok`: add `or "households" not in revision` before `_history_rows_ok(revision["households"])`.

## Phase 3 to 5

As in the plan. Raw logs and exit codes are saved unmasked under `phase131-extension1-evidence-1110/run/`.
