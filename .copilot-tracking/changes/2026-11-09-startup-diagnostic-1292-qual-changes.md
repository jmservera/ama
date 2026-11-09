---
title: Issue 1292 startup diagnostic record qualification
ms.date: 2026-11-09
---

## Purpose and status

* Dated 2026-11-09 qualification of the diagnosis-only record frozen at `59accfa1ca9be77f2e98faf5ef862deba76cf941`, written after an independent Readiness review (approve_with_comments: three Medium, one Low evidence-interpretation findings). It supersedes, from this date and without backdating, the statements qualified below in the original changes and review records and in the external handoff `handoff-1292-startup-diagnostic.md`. Those originals are unchanged.
* Unchanged executable-source evidence qualification. Not a source fix, not an E5, no new run. The cause of the retained `database is locked` failure remains UNKNOWN; H1 to H4 remain unresolved. Refs #1292 only; every #1292 criterion stays unmet and unticked.
* Counters unchanged: six original diagnostic attempts used (3 isolated, 3 concurrent, plus one disclosed non-counted harness defect); E4 history immutable; E5 not spent; one additional productive source correction remains; no automatic grant or reset.

## Qualifications

* Q1 (R2 in the original review; the changes record and handoff do not state it). The six non-reproducing executions, four with timing-perturbing observers, do not establish that either the six-module API workload or I/O pressure is necessary or sufficient to reproduce the failure. Neither was varied. Replacing the original wording: a separately authorized diagnostic could investigate that workload or I/O pressure; it exceeds the original plan bounds and was not performed.
* Q2 (original changes, review R1, handoff). Reading from the retained `I2/I3/C2/C3.observer.json` traces, which record statement starts only, with no COMMIT-return event:
  * 3.05-3.25 s is an observer-derived upper bound from the holder's `BEGIN IMMEDIATE` trace to the first later waiter event. It is not a measured lock hold time.
  * 1.10-1.17 s is the interval between `_backfill_zero_ordinals` enter and exit in the holder (the backfill wrapper).
  * 1.80-2.03 s is the interval from the holder's backfill exit and COMMIT trace to the first later waiter event. It is not the COMMIT call duration and includes commit and checkpoint work, scheduling and waiter wake-up in a way these traces cannot separate.
  * In I2 the first later waiter event is, at 8.0005 s, the enter and exit of `_review_priority_order` and `_backfill_zero_ordinals` followed by COMMIT inside its `_migrate_recommendations`; the holder's own `_migrate_recommendations` exit is at 9.8697 s. In I3, C2 and C3 the first later waiter event is a COMMIT closing an earlier BEGIN IMMEDIATE trace, before the waiter's `_migrate_recommendations` entry. The waiter may therefore have been blocked in an earlier migration step, and the trace does not locate the lock wait.
  * The approximate 1.6x margin (5.0 s over about 3.1 s) is a heuristic derived from that upper bound, not a demonstrated failure threshold or cause. H1 stays a candidate only.
* Q3 (original review R1). The 5.0 s figure is SQLite's per-lock busy timeout (`PRAGMA busy_timeout=5000` at `src/core/src/zava_forward/core/sqlstore.py:224,258`, with the `connect` default). The test does not assert both openers finish within 5 s. It asserts `errors == []` and then `elapsed < 20.0` for the opener phase (`src/core/tests/test_priority_order.py:734-735`). The retained original failure (`logs-440-sqlwave/core-store-priority.log:424-441`) stopped at the `errors` assertion, before the duration assertion. No deadline defect is demonstrated.
* Q4 (original review "Core attempts under 17 s"). Unittest-reported durations are 15.161-16.097 s. Core process wallclocks (`core_end - core_start` in each `.meta`) are I1 17.679, I2 16.844, I3 17.313, C1 17.535, C2 17.628, C3 18.057 s, i.e. 16.844-18.057 s. All are below the 180 s cap.
* Q5 (observer safety). The four observer records show `ok: true` and empty `raised` arrays: no observer error was observed. This does not guarantee that every recorder failure would be harmless: in `observer_run.py` the `_open` exception-path `RAISED.append` is unguarded and a failure to install the trace callback is suppressed. Observer runs perturb timing, and none of this implicates the observer in the original failure.

## Provenance and verification (read-only, no reruns)

* Head `59accfa1ca9be77f2e98faf5ef862deba76cf941`, tree `93e1bf9f2bf563e22ed4c34c1eb84c46f2fd1085`, branch `test/demo-startup-diagnostic-1292-1109`, base `ef28d4da42d83b111d48f14df9b70e3c4932a477`. Planning commit `8aea86f8ba0ab2f7d4d503d589cb44305f3fe914` (tree `75f48688cb26b7584bd9fec1d8514227e0fcbf7b`) is an ancestor of the frozen head (`git merge-base --is-ancestor` true; the frozen head adds only the changes, review and state records).
* `git diff --stat ef28d4da4 HEAD -- src infra tools .github pyproject.toml` is empty at the frozen head; the 7-file, 250-line diff is entirely `.copilot-tracking`. `git status --short --ignored` was empty.
* Original blobs at the frozen head: changes `81493702a5ee`, details `c8bdc85a3871`, critique `4f9fc061ca5a`, plan `4c25e732d920`, research `d4b155e11fc7`, review `7448edca8b98`, state `1a3418aca5c0`. Working-tree sha256 values were captured before and are re-hashed after this task; see the review record.
* Raw packet `/home/azureuser/source/ama-demo-wt/logs-1292-startup-diagnostic/`: `sha256sum -c SHA256SUMS` matched 29 of 29 members with no mismatch, including `harness-defect/`. The manifest's own sha256 is `c4442f3f69a27a7547059b813d65c28cf05495d7bcc775bb7cde76f5ce5aec8c`. No trusted original manifest hash exists, so this shows member consistency with the manifest, not independent origin. The raw directory is outside the repository and not committed.
* Fetched `origin/main` is `1464b4d850a89aaaf835ba8a9ad98d38aeb1fdd6` (remote-tracking fetch only, informational; not merged or rebased, base preserved). `git diff --name-only ef28d4da4 origin/main -- src` is empty, so the exercised `sqlstore.py` and `test_priority_order.py` do not differ between the base and fetched main; this is source-path equivalence, not a claim about workflows, tools or docs that changed.

## Unavailable claims

* Plan FR1 promised an import-origin check for each `zava_forward.*` namespace and sha256 of `sqlstore.py`, `store.py` and `test_priority_order.py`. The original record retains only the `sqlstore.py` sha256 prefix `0b0caf62802d` and a prose summary of import origins; the full per-module import output and the other two hashes were not retained, and the owned venv was removed. They are not reconstructed or inferred here. The tracked blobs of those files are identical at base and head, but that is not an observation of what the runs imported.
* Existing transcript and executed raw provenance is evidence with limits; it is not re-established by re-running. No new execution, SQL, browser, stress, model, cloud, credential or cleanup action was taken.
* Not independent of the authors: this qualification and its review are authored. The Readiness reviewer must assess the new head before any publication. No hosted CI was read for this head.
