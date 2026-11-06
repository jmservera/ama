---
title: Changes for exact-68 replacement (issue 1204)
ms.date: 2026-11-06
---

Plan: [plan](../../plans/2026-11-06/coordinator-exact68-replacement-prep-1204-plan.md), Phase 3. Details: [details](../../details/2026-11-06/coordinator-exact68-replacement-prep-1204-details.md).

## Changes

* Removed exactly 68 run-001 raw transcript files (288862 bytes) from the checkout under `.copilot-tracking/sandbox/2026-11-05-coordinator-behavior-001/raw/`, as listed in the pending journal and manifest SHA-256 643fb9ad.... Their bytes remain in the tracked bundle `raw-selected-68.tar.gz`, Git history at f6b2984d9, and the external archive.
* Added `exact68-actual-removal-journal.md` (actual outcome and qualifications) and this Changes record. No other file added or changed.
* Not changed: agent source (blob acefb44a), `exit-codes.json`, report 005, original and adverse records, normalized copies, bundles, `.gitattributes`, refs, `/tmp/h1204`.

## Validation

* Guarded external operation passed all pre and post assertions (see the journal). Protected 7507 blobs, refs and 262 external entries unchanged.
* `cd tools && python3 -m unittest test_backlog_sync test_rpi_checks`: exit 0, Ran 97 tests OK in 19.279 s (external log `/tmp/h1204-r8/unit.log`, SHA-256 e3a5e14e555f178943e42754c36594af0f729d63f72850b0982877fbf5f27c1f).
* Range `git diff --check origin/main..HEAD` (origin/main bb3a3b03cb94eef6c06ae4b12d07cfe7bbdef43f) before this commit exited 2 with 340 lines, all in the 68 files still present in the committed head; the working-tree `git diff --check` exited 0. The range result after this commit is recorded in the Review.

## Remaining gates

Independent exact-head assessment, hosted checks, human acceptance of report 005 and the complete local gate on the final head. Storage and focused-unit conformance is not whole-issue acceptance.
