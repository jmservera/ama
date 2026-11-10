---
title: Issue 79 research, continuation r10 (four independent exact-head runner findings)
ms.date: 2026-11-06
---

## Chronology statement (prospective)

This research, the plan and the details are committed before any r10 test or source edit. No r4 to r9 record, source, test, log, receipt or state file is edited, repaired or regraded. The original r4 post-hoc chronology failure, the r7 intermediate adverse events and the r8 review-timing limits all stand. The r9 FULL result applies to head `fe414bb71e24` only and becomes historical once this head changes.

## Identity and pins (intake, read before this record)

* Task `issue-79-r10-runner-assessment-findings`, parent `issue-79-r8-final-review`. Same original session `e4869dea-7260-432e-a2dd-1c7a3e01e32c`.
* Branch `feat/ranking-publication-runner-79`, head `fe414bb71e244446ea5a5a11d06f32550626972e`, tree `06cffff0b513815facbbd5f7e493d4d17ca98d70`, empty ignored-inclusive status. Freshly fetched main `bb3a3b03cb94eef6c06ae4b12d07cfe7bbdef43f`; declared parent `feat/case-workbench-integration-73` at `ead177ef90d24666557708ea344848a1be43bdf8`, unchanged. No rebase, merge or retarget.
* Research disposition `executed`; Planning Readiness `Ready`.

## Evidence read

* New independent exact-head functional assessment (approve_with_comments, four Medium, no High or Critical): `functional-findings.json` and `short-report.txt` under `/home/azureuser/.copilot/session-state/77149bdf-2f9a-4b04-b1dc-af3109946991/files/review-79-fe414-prepublication/functional/`. Read, not edited. It is a static assessment; it ran no tests.
* Actual current `ranking_publication_runner.py` (328 lines), its test module, `ranking_publication.publish` and `verify`, and the README runner paragraph.

## The four findings and the code that causes each

* F1 `load_cases` filters with `not c["closed"]`: a string, null or number is read by truthiness, so `"false"` silently drops a case and an all-malformed file becomes an empty source that ranks and could publish `total=0`. Persisted Store data writes `closed` as a real boolean, so a strict check keeps valid data working. A raised `TypeError` already reaches the CLI as an unreadable source and then as a `source_missing` refusal.
* F2 `schedule` sets status `blocked`, `due` or `current` from refusals and due only. Archive problems are listed but do not change status, and `main` maps only `problem` to exit 1. An archive with one good current record and one damaged record reports `current` and exit 0.
* F3 `run` checks free bytes before `publish`, though `publish` returns the existing record without writing when the target already exists. An identical retry on a full or read-only archive is refused with `capacity_missing`. Archive verification already runs earlier and refuses any damaged archive.
* F4 `_date` accepts `9999-12-31`, so `today + 1 day` raises `OverflowError`. Independently an archived `latest` of `9999-12-31` (a valid calendar date) overflows the next-window calculation in `schedule` and `publish`.

## Decisions for the fixes (smallest, using existing mechanisms)

* F1: require every case to be a mapping with a boolean `closed`; raise `TypeError` on the first malformed record. No coercion.
* F2: `schedule` returns status `problem` whenever the archive has problems, keeps `due`, `latest` and any approval refusal in the result. `main` already maps `problem` to exit 1.
* F3: skip the capacity check only when the exact target file already exists, so a genuinely new record still needs capacity and the helper still never overwrites.
* F4: refuse `today == datetime.date.max` with the existing `bad_date` refusal before any arithmetic. For an archived latest with no next day, report `next_window_start` as `None` and add one problem line to the result, so schedule is `problem` and publish refuses with `archive_unverified`. No future-date freshness or retention policy is invented.

## Limits

* Light checks only: the combined publication and runner test selector, Ruff, format and mypy with existing tools and external caches. No gate, SQL, browser, Docker, install or lock. The unrelated inherited helper race (shared `.tmp`, exists-then-replace), the loose `as_of` check and archive schema hardening are not touched.
* Not proven and not claimed: named policy-owner signoff, Legal retention decision, scheduler activation or retained scheduled operation. The corrected head needs a fresh FULL gate and a fresh independent reassessment; the r9 receipt does not cover it.
