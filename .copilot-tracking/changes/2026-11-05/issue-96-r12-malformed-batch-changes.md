---
title: Issue 96 r12 changes and author review
ms.date: 2026-11-05
---

Refs #96, parent #93. Executed after the r12 research and plan. Original r6 self-review is unchanged.

## Changes

* `src/core/src/zava_forward/core/form_review.py` `_proposals`: attribution now uses case id, schema id and version only. An attributable batch with no `schema_digest` key yields the existing `proposal-record-malformed` Unknown (batch id only); a present, different digest and missing or malformed attribution keys stay excluded.
* `src/core/tests/test_form_dependencies.py`: `test_attributable_batch_missing_digest_stays_visible_as_unknown` on both stores; also asserts a different digest and a different schema id stay excluded and that the read leaves the case record unchanged.

## Validation (light, local, exits captured, venv `/tmp/ama-96-venv`, imports from this worktree, external caches)

* New test failed at intake source (`0 != 1`), passed after the fix; retained as the initial failure.
* unittest form_dependencies, form_review, form_export, form_staging: 56 tests OK, 0 skips (exit 0).
* ruff check 0, ruff format --check 0, mypy 0 (267 files).
* No heavy gate, browser, SQL, Docker or cloud work. The r11b receipt is historical and does not cover this head; a fresh FULL gate is required.

## Self-review

Executed once; the fix is minimal and fail-closed, with no new abstraction, write or policy. Residual: independent exact-head review and fresh FULL run are required. C1, C5, residual C6 and #93 approval remain unproven.
