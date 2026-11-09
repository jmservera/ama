---
title: Issue 1259 C2 typing correction details
description: Phase details for the two-diagnostic test typing correction
ms.date: 2026-11-09
---

## Phase 1: Edit

In `src/core/tests/test_ranking_archive_blob.py`, change the signature of `test_conditional_create_never_lists_so_an_unreadable_listing_does_not_block_it` to `-> None` and replace `len(self.fake.requests("PUT")) == 1` with `len([c for c in self.fake.calls if c[0] == "PUT"]) == 1`.

## Phase 2: Validate (owned out-of-tree venvs, CI install profile)

* `cd src/core && mypy`; compare sorted line-stripped diagnostics with parent log (expect equal; 84).
* `cd src/api && mypy` (expect 9, all fixture).
* `ruff check .` and `ruff format --check .` in core and API, each recorded separately; parent-inherited failures are retained, not fixed.
* `python -m unittest` for `tests.test_ranking_archive_blob`, `tests.test_ranking_publication`, `tests.test_ranking_publication_runner` (core) and `tests.test_ranking_publication_wiring` (API, with `PYTHONPATH=../core/tests:../agents/tests`).
* Logs stored under the mktemp directory with sha256.

## Phase 3: Record and review

Changes record, one Review, state JSON, handoff in the session files directory, commit frozen candidate with Conventional Commit and trailer.
