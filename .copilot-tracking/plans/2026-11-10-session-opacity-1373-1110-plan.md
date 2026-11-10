---
title: Issue 1373 resident session opacity test-oracle plan
ms.date: 2026-11-10
task_id: 1373-session-opacity-1110
---

## Plan (authored 2026-11-10 before any source edit)

Objective: replace the false whole-token substring oracle in `SessionTests.test_round_trip_and_handle_is_opaque` with keyed-handle, case-binding and round-trip checks, and add one frozen genuine-signature collision regression, in `src/core/tests/test_resident_showcase.py` only.

* [ ] Phase 1: Add the frozen synthetic constants and one sid-patching helper; rewrite the opacity method; add the collision regression. Real `issue` and `verify`; only the module's sid random source is patched in the regression.
* [ ] Phase 2: Prove red-before (old assertion fails on the frozen fixture through unchanged code; done in research, re-run against the final file with the old assertion body) and green-after (the new tests pass, nine existing tests unchanged).
* [ ] Phase 3: Targeted validation: `SessionTests`, whole `test_resident_showcase`, Core discovery under the venv, `ruff check`, `ruff format --check`, configured `mypy` (project `files = ["src", "tests"]`), and a production-source-unchanged diff check.
* [ ] Phase 4: Changes record, one Review, state file, freeze commit with a clean tree, handoff.

Done means: the collision regression and rewritten method pass; the old assertion demonstrably fails on the same fixture; all selected checks ran with no skip in scope or the exact pending step is recorded.

Out of scope: production code, authentication, RNG, encoding, permissions, other flaky tests (including the `token[:-2] + "xx"` tamper case), other test files, shared helpers, project configs, full or `--changed` gate, browser, SQL, cloud, provider, private data, push, PR, issue or board edits, primary checkout changes.

Gates: no correction allowance beyond this one initial repair; independent exact-head assessment precedes publication; the child targets `feat/demo-closed-page-csv-80-1110`, uses `Refs #1373`, `#80`, `#189`, `#462` and carries no closing keyword. No authentication bypass or security acceptance is claimed.
