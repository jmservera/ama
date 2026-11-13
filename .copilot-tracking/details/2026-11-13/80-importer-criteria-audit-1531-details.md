<!-- markdownlint-disable-file -->
# Details: Issue #80 importer and export criteria audit

## Phase 3 specification

Changes file holds: pinned source and test commands with results; a table with one row per literal criterion and per compound clause (columns: clause, verdict, evidence `file:line`, missing gates); the twelve-entry style control inventory refreshed at the pin; limitations; list of artifacts. Verdict vocabulary is exactly `PROVEN` or `NOT FULLY PROVEN`.

## Clause decomposition

* C1: (a) mapping shown, (b) conflicts shown, (c) row-level preview shown, (d) source never changed, each assessed at module level (workbook importer) and user-reachable level (web/API).
* C2: (a) every list has an export control, (b) Excel or CSV format, (c) Excel one-way read-only.
* C3: (a) version, source, approval, supersession retained in export, (b) independent of AI provider, (c) reachable by a user export.
* C4: owner-set thresholds exist as approved record.

## Validation

Re-run cited line numbers with `grep -n` against the pinned tree before finalising; `git diff --check`; independent `code-review` of the changes file.

## Critique dispositions applied (single critique)

* Blocking, accepted: C2 requires a list-to-control matrix of displayed lists (not only located controls); uncovered or scope-uncertain lists keep C2 NOT FULLY PROVEN.
* Non-blocking, accepted: assess the importer CLI preview (`__main__.py:209-223`) separately from web/API; do not infer a workbook UI from it.
* Non-blocking, accepted: carry forward owner interpretation of "list" scope, live-data access, retention and suppression approvals as unresolved gates without implying they block synthetic-demo evidence.
