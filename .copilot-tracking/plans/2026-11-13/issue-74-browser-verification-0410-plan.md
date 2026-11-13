<!-- markdownlint-disable-file -->
# Plan: #74 home-case browser verification (issue-74-browser-verification-0410)

Date 2026-11-13. Research: [research](../../research/2026-11-13/issue-74-browser-verification-0410-research.md). Details: [details](../../details/2026-11-13/issue-74-browser-verification-0410-details.md). Critique: reused from `issue-74-building-separation-0400` (blob 75ecdcdf0fca588fd6bccaf84bd74f8fa4b34896), not repeated. The scope below was fixed by the owner brief and the pre-run source reading before the run; this file was written to disk after the run, so its timing is disclosed rather than claimed as a pre-run timestamp (the runner script hash in details shows the pre-run configuration).

## Scope (pre-execution)

* One execution of `python -m checks.home_case_browser_check` from `src/api` at head 6f2918011d55d63ffc52865073ef45bd7ea9197c with `ZF_AXE_JS` set to the pinned, hash-verified axe 4.10.3 copy.
* Own environment and outputs only under the session `files/74-browser-verification-0410/` directory (venv, HOME, scratch, axe copy, logs).
* Resource rule: non-blocking exclusive flock on `/tmp/ama-rpi-heavy.lock` (regular, non-symlink, owner and inode recorded), at least 4 GiB available, no queue or retry, held until the run and cleanup end; 15-minute budget.
* Declared dependencies may be installed into the owned venv only after the selected validation fails on missing modules.
* Excluded: unit tests, SQL, full gate, cloud, image builds, browser downloads, uv, product, test, check or config edits, new assertions, `buildingView` route coverage, GitHub writes, push, PR, merge.

## Phases

* [x] Phase 1: reuse and source-equivalence record (research).
* [x] Phase 2: preflight and execution (details, changes).
* [x] Phase 3: single Review (review artifact).

## Stop conditions

Lock busy, under 4 GiB, missing pinned axe or Chromium, or any failure: record and stop without repair or blind retry.
