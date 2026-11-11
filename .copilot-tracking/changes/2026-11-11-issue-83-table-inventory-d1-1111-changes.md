---
title: Issue 83 table inventory D1 changes
ms.date: 2026-11-11
task_id: issue-83-table-inventory-d1-1111
---

## Scope

P01 to P04 implemented (P05 Review and P06 commit follow). Base head dd3c32910c3c5205a2cbedbe74608411c6f9f341. Local only.

## Changes

* `src/api/tests/test_accessibility_baseline.py`: count literal 12 to 13 and a one-line comment naming the handoff waiting table. Regex, caption check, bare-`th` ban and fail-on-new-table mechanism untouched. No new test (existing mechanism already guards caption-first and bare `th` for this table; a scope test would add policy beyond the failure).
* `docs/reference/research/ux/wcag-conformance-baseline.md`: Tables row gains the 2026-11-11 thirteen-table source-audit entry with limits; the 11 and 12 observations kept; frontmatter `ms.date` 2026-11-11; G-4 unchanged.
* `docs/reference/README.md`: baseline index entry summary and date.
* `docs/reference/log.md`: one appended entry.
* Product files (`src/api/src`, core, agents, CSS, API, store, permissions): not touched.

## Evidence

* Pre-change: `.copilot-tracking/reviews/logs/2026-11-11/issue-83-table-inventory-d1-1111-pre-change.txt` (13 != 12 at dd3c32910, worktree PYTHONPATH).
* Post-change: `.copilot-tracking/reviews/logs/2026-11-11/issue-83-table-inventory-d1-1111-post-change.txt`.
* Audit: research C3 to C5; the only app.js table added since main is the waiting table.

## Validation (cwd `src/api`, PYTHONPATH on the worktree sources, no install)

| Command | Result |
| --- | --- |
| failing test alone, before change | FAIL 13 != 12 |
| same test after change | OK |
| `python3 -m unittest test_accessibility_baseline` | 12 tests OK |
| `ZF_BROWSER_TESTS=1 python3 -m unittest test_handoff_waiting_view test_unaccepted_handoff_download_ui test_handoff_read_guidance test_handoff_api test_role_endpoint_inventory test_workbench test_role_screens` | 69 tests OK, no skips reported |
| `node --check` app.js | exit 0 |
| `ruff check tests/test_accessibility_baseline.py` | pass |
| `mypy tests/test_accessibility_baseline.py` | no issues |
| `ruff format --check tests/test_accessibility_baseline.py` | would reformat: pre-existing, same result on dd3c without my edit (stashed check); not changed in this D1 |

Not run: full gate, SQL, image build, deployment, cloud, assistive technology, hosted CI. A local pass is not a hosted pass; the hosted job for the new head is unobserved.

## Follow-up items

* Screen-reader, reflow and manual acceptance of the waiting table; OD-09 times and operational acceptance (human); #83 criterion 3 unmet.
* Out of scope and unchanged: original critique's three Low relative links, unbounded-row performance qualification, `ops.js` line 28 aria-label table form, pre-existing ruff format drift in the baseline test.
