---
title: Issue 79 research, corrective continuation r7 (malformed archived publication date)
ms.date: 2026-11-06
---

## Chronology statement (prospective)

This research and the plan and details files were written before any r7 test or source edit. They do not repair, backdate or regrade the original r4 chronology failure: in the original run, the runner and tests were created before the r4 research, plan and details. That failure is confirmed and preserved. The r5 and r6 records are unchanged and are not evidence of initial chronology.

## Identity and pins

* Task `issue-79-r7-archived-date-validation`, parent `issue-79-r6-main-preparation`. Branch `feat/ranking-publication-runner-79`, frozen head `2b95538bc34ef842277cbef5e4e4555cde752f1d`, tree `61415ecb5172e140ce63bfce654b4370ace12c71`, ignored-inclusive status empty at intake. Main pin `bb3a3b03cb94eef6c06ae4b12d07cfe7bbdef43f`. Declared parent target `feat/case-workbench-integration-73` at `ead177ef9`, unchanged and not moved.
* Authenticated account `jmservera` (id 8036360). Research disposition `executed`; Planning Readiness `Ready`.

## Defect (reported by the coordinator, reproduced there; read in source here)

* Source read: `ranking_publication.verify` appends `rec["published_on"]` to `dates` after the hash, name and registry checks, with no check of the value's type or calendar validity. `max(dates)` is then returned as `latest`.
* `ranking_publication_runner.run` then calls `datetime.date.fromisoformat(latest)` for `next_window_start` when not due. For an archived `published_on` of `"2026-11-31"` this raises an unhandled `ValueError`, while `verify` reports `problems: []` and status `ok`.
* A related gap: `publish` validates `published_on` with a regex only (`_DATE`), so `publish(snap, dir, "2026-11-31")` would write an impossible date into a new immutable record. Writing is bounded to the same minimal helper, so the fix is applied at the publish boundary too, before writing.
* Non-string metadata (`null`, number, list) already raise `TypeError` or compare badly inside `verify`: `max` over mixed types can raise outside the `try`, and a number would be treated as a date. These are in scope as "metadata type guards".

## Prior art

* Runner `_date(value)`: type guard, `_DATE` regex, then `date.fromisoformat`, returning `None` on failure. This is the existing pattern; it lives in the runner, which the core publication module cannot import (the runner imports it).
* Other modules (`synthetic/climate_history.py`) use `date.fromisoformat(x).isoformat() == x` round trip. Python 3.12 `fromisoformat` also accepts non-`YYYY-MM-DD` forms, so regex plus parse is kept and no regex-only validity is relied on.

## Chosen minimal design

* Add one private helper in `ranking_publication` (`_valid_date`: `str`, `_DATE` match, `date.fromisoformat` succeeds) and use it in `publish` for `published_on` and in `verify` for the archived `published_on`.
* In `verify`, an invalid or non-string `published_on` appends a problem `"{name}: publication date is not a valid calendar date."` and is not added to `dates`, so `latest` is trusted-only. Keep the existing `try/except` and message styles.
* The runner needs no code change if `latest` is always valid: schedule, publish and verify then report the problem consistently (`publish` already refuses with `archive_unverified` when problems exist; `schedule` reports the problems; `verify` is status `problem`). The runner's `_date` can reuse the same logic but is left unchanged to keep the diff minimal.
* Unchanged: valid archive bytes, names, identities, idempotence, immutability, valid-date scheduling, stale-source warnings, future-source refusal, signed-policy boundaries, retention and deletion (none introduced). Not repaired: unrelated max-date edges and `as_of` validation.

## Tier and scope

* Existing FULL-tier ranking publication candidate; this continuation is LIGHT ONLY. #185 owns the sole heavy execution (gate `a7d4`, `/tmp/g185-full-r9-1106`); no gate, SQL, browser, Docker, `--changed` or second heavy run is started.
* Not claimed: whole #79, a live scheduler, Legal retention, named policy sign-off, independent exact-head review, hosted CI or human approval. Criteria 3 and 4 of #79 stay open.
