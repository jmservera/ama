---
title: "Changes: #79 tie-break, policy-version and read-only archive regression"
ms.date: 2026-11-14
task_id: 79-tiebreak-version-audit-0016
---

## Added

* `src/core/tests/test_ranking_tiebreak_audit.py`: 10 tests. Case-id tie-break across all input permutations (shared address), `deciding_rule` of `case_id`, `sql_key` agreement, input immutability, version and hash stamping per policy, v1 bytes unchanged by a newer policy, `verify` leaves archive bytes and mtimes unchanged (clean, wrong-registry, wrong-hash) and does not create an absent folder.
* `src/api/tests/test_ranking_tiebreak_read.py`: 4 tests. Snapshot endpoint stamping and byte stability, unknown version refused without writes, repeated publication-status reads leave archive, cases and audit unchanged, archived record keeps the stamped version.

## Modified

* `src/core/pyproject.toml` and `src/api/pyproject.toml`: one mypy `disallow_untyped_calls = false` override each for the new test modules, matching existing sibling overrides. No production code changed.

## Divergences

* UPRN is not a field anywhere in the model; tie-break is asserted on case id with a shared home address. Recorded in research.

## Validation (Focused tier, `/tmp/venv-79-0016`)

* `ruff check` and `ruff format --check`: pass in `src/core` and `src/api`.
* `mypy`: `src/core` clean. `src/api` reports 66 errors, all pre-existing (missing `playwright` stubs); identical count with the change stashed, none in the new files.
* Tests pass: new core and API files, `test_priority_order` (146, 67 skipped for no MSSQL), `test_ranking_publication`, `test_ranking_archive_blob`, `test_scenario_manifest`, API `test_ranking_policy`, `test_ranking_publication_wiring`, `test_ranking_scale`.
* Not run: full local gate, hosted CI, browser harness (not touched). Classification: Focused; pyproject edits are typing-config only, no dependency, permission, or gate semantics change.
