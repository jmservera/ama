<!-- markdownlint-disable-file -->
# Plan critique: #1402 C2 integration

Executed once (rubber-duck, observed, read-only) on the final-candidate plan. Verdict: needs changes; all applied directly.

* CK-01 Blocking: `git diff --quiet` with repo-relative paths from a subdirectory can falsely pass. Applied: run from repo root, compare blob SHAs explicitly, assert existence.
* CK-02 Blocking: no proof of replay completeness. Applied: pin main, verify four-commit range before and after, `range-diff`, whole diff inspection.
* CK-03 Non-blocking: research said all 47 main changes were tracking files. Applied: corrected (also `test_permit_sql.py`, rubric `latest.json`).
* Confirmed sound: `rebase --onto origin/main 2f7465c57` boundary, lightweight preservation tag, no tracking-file overlap at inspected commits.
