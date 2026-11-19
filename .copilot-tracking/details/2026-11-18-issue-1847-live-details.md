---
title: Issue 1847 live details
---
# Details

* Phase 1: three layouts (source, noneditable --target copy, editable venv) times two import orders, plus temporary restore of the original bootstrap from 7de4a8110^ to record adverse output; restore verified by `git status`.
* Phase 2: one index row and one append-only log entry.
* Phase 3: run `test_nomination_bootstrap test_bulk_edits test_nomination_route` once more, review diff, commit with Refs #1847.
