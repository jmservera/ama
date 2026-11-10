---
title: Issue 131 inherited correction batch for the household inventory primitive (details)
ms.date: 2026-11-10
task_id: 131-inherited-repair-1110
---

## Step 1: shared history validator

In `resident_decisions.py` next to `_inventory_managed`, add `_household_ref_ok(ref)` (string, not blank, equal to its strip, at most 100 characters) and `_inventory_history_ok(inventories, case_id)`:

* a non-empty list; each element a dict whose `version` is an exact int equal to its 1-based position and whose `case_id` equals the case id;
* `households` is null, or a list of 1 to `INVENTORY_MAX_ROWS` dict rows with exactly `household_ref`, `report_version` and `report_digest`; references pass `_household_ref_ok` and are unique by `casefold`; a null link has a null digest; an int (not bool) link at least 1 has a string digest.

It does not compare historical digests with current reports and mutates nothing. `_inventory_rows` uses `_household_ref_ok` for the input reference check so the rules share one definition.

## Step 2: view

`_inventory_fill` calls the validator on the whole stored history and raises `ValueError` (Malformed) on failure, then drops its now redundant partial type checks for the version, households list, reference and link. The reports shape check stays.

## Step 3: writer

`_res_tenure_inventory_record` refuses, before `_version`, a present but invalid stored history or malformed reports with the existing malformed message; nothing is recorded and no audit entry is written. The absent field (first revision) is unchanged.

## Step 4: refusal reasons

After the existing unverified reason add two count-only reasons for linked reports with report data:

* stored `identity_state` Unknown, Ambiguous or not a string: "N linked tenure reports still have an unresolved or ambiguous household identity.";
* `decision_route` not a string in the values of `TENURE_ROUTES`: "N linked tenure reports have no recorded decision route or an invalid one.".

No reference, owner, source or digest appears in these texts. `resident_gate` and `_res_scope_record` already forward the reasons plus `TENURE_HOLD`.

## Step 5: tests (existing file only)

* New `test_inventory_corrupt_history_is_malformed_and_never_extended`: through the supported action record a valid inventory; with corrupt-store injection (under the store lock and `save`) set a version-99 singleton, a malformed earlier dict before a valid-looking last revision, blank and duplicate latest rows, a wrong case id and an empty list. For each: the view is Malformed, the gate and a refused `scope_record` contain the hold, the writer raises `ValueError` and the stored history and audit are unchanged. Control: a valid history whose first snapshot digest is stale after a trigger still accepts a new revision.
* New `test_inventory_identity_and_route_are_count_only_refusal_reasons`: verify both reports through the supported actions (intake stores Ambiguous), record and link both, assert the identity reason and a refused scope; inject an Unknown route into one stored report and re-record so digests are current; assert the route reason; assert the texts carry no canary reference, source, owner or digest.
* Update the existing refreshed-data expectation that asserted no reasons for Verified plus Ambiguous.
* Typing and format: in `inventory` build a typed `dict[str, Any]` and update it, annotate the `bad` collection, narrow `other` with `assert isinstance(other, SqlStore)` as the file already does, then `ruff format` that file only.

## Step 6: README

One bounded sentence in the Core README inventory section: reasons now include count-only unresolved identity and invalid route, malformed history is refused, the hold is unchanged.

## Step 7: baseline and red/green

After the main merge, run the baseline selectors on the composed head. Add the tests, show them failing on the unfixed module and passing on the fixed one, then run the validation commands in the plan and keep every raw command, log and exit code under the external evidence directory.
