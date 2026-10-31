---
title: Employee progress dashboard 533 correction phase details
description: Exact completion and publication boundaries for successor loop
ms.date: 2026-10-31
---

Task 533 / employee-progress-dashboard-533-correction. Opening direction:
research Ready, original RV-001 is the sole implement defect. No unanswered
scope decision; validation and publication prerequisites must actually execute.

<!-- rpi:phase id=P01 -->
## P01: Correct and validate

<!-- rpi:task id=P01-T01 -->
### P01-T01

Use the existing lifecycle_case initialized-template pattern. Extend scale_data
with an optional typed list of case templates. Unit regression passes initialized
ZF-1 through ZF-4 templates; browser calls retain existing no-argument behavior.
Deep copies preserve resident/home mutations and remapped AI references without
mutating initial reader templates. Defaults therefore come from the actual store,
not a copied subset. Keep every existing exact scale assertion.

<!-- rpi:task id=P01-T02 -->
### P01-T02

From src/api, use installed distributions and
PYTHONPATH=.:src:tests:../core/src:../agents/src:../core/tests:../agents/tests.
Set PYTHONDONTWRITEBYTECODE=1; Ruff caches external.
First execute both classes' test_existing_60000_home_fixture_progress_and_filtered_page_boundaries
under flock -n. Then full python3 -m unittest discover -s tests -q;
ruff check; ruff format --check. Record skip test IDs/reasons, never count skips
as execution. Actual browser: python3 -m checks.progress_browser_check
--axe <hash-verified 4.10.3 asset> --out <new external path> --scale under
flock -n, which runs original small plus scale checker. Lock admission failure
permits later nonblocking retry, not an unlocked run or interrupted foreign owner.

Completion: P01-T01 authored and P01-T02 executed, both reconciled to changes.
Focused 2/2 backend regressions passed; requested discovery 1432 tests with
1112 executed and 320 expected skips passed; Ruff/format/types passed; actual
small/scale Chromium and all 13 axe scans passed. Individually confirm and
record skip IDs/reasons with a skip-only lightweight audit instead of duplicating
the 1112 executed tests. The audit executes zero tests and does not replace the
actual required full discovery. See correction changes for exact logs/hashes.

<!-- rpi:phase id=P02 -->
## P02: Review and publish

<!-- rpi:task id=P02-T01 -->
### P02-T01

Review exact correction diff, original rejected finding, reconciled plan/details,
changes and actual logs; write only successor review. One independent reviewer,
no repeat source Review inside this successor after findings.
Append successor pointers to originals without rewriting adverse outcomes.

<!-- rpi:task id=P02-T02 -->
### P02-T02

Resolve authenticated gh api user; local privacy-safe email for both identities,
required trailer. Commit source and dated evidence. Fetch origin main and run
python3 tools/rpi-checks.py --all --jobs 3 --lock-timeout 0 --base <main sha>
--out <new external directory>. Runner owns the shared lock; no outer flock.
Busy admission permits later new nonblocking attempt in session.
Missing prerequisite/failed full gate blocks publication. Keep receipt external.
Immediately before push fetch main and verify receipt with current base. A fresh
independent assessor receives HEAD/tree/base, source-review pointer/outcome,
receipt/verification, original findings/dispositions and clean worktree evidence;
checks identity/readiness only, not another source Review. It writes external
assessment so HEAD remains exact. Fetch/verify again directly before
git push -u origin HEAD and gh pr create --base main with Refs #533, unmet live
criterion and check/evidence details. No merge or history rewrite.
