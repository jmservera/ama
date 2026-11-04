---
title: Issue 104 round 2 details
ms.date: 2026-11-04
---

## Phase 1: read_document boundary test

* Upload `note.txt` with `Store.add_document` and `change_metadata`, snapshot `controlled()`.
* Call `read_document` with the scripted hostile model and with `mode="off"`.
* Assert the stored document differs from its upload only by `summary`, the snapshot is unchanged and the audit chain verifies.

## Phase 2: focused validation

* From `src/api`: `test_ai_boundary`, `ruff check .`, `ruff format --check .`, `mypy --cache-dir=/tmp/mypy-104` (the CI command with `.[dev]` installed).
