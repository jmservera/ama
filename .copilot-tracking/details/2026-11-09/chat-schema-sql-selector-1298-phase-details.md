<!-- markdownlint-disable-file -->
# RPI Phase Details: select MSSQL for the chat schema dependency of the sensor store (#1298)

## Metadata

* Task ID: issue-1298-fresh-demo
* Task slug: chat-schema-sql-selector-1298
* Related plan: .copilot-tracking/plans/2026-11-09/chat-schema-sql-selector-1298-plan.md
* Evidence sources: .copilot-tracking/research/2026-11-09/chat-schema-sql-selector-1298-research.md

## Phase Index

| Phase ID | Name                                    | Status | Detail sections |
|----------|-----------------------------------------|--------|-----------------|
| P01      | Reproduce and add the failing regression | ready  | P01, P01-T01    |
| P02      | Make the selector change                | ready  | P02, P02-T01    |
| P03      | Targeted validation and evidence        | ready  | P03, P03-T01    |

Test ownership lock (fixed before critique): removals none; additions at most one new test method and one new entry in an existing path loop; one edit to the existing exact-set expectation (expected set gains the `mssqlstore.py`-derived `chatthreads.py` path); no change to receipt mutation tests; semantic coverage (AST evidence of the dependency) plus regression coverage (selection, negative control, flagged command).

<!-- rpi:phase id=P01 -->
## P01: Reproduce and add the failing regression

### Context

Main `9f9aacc8b` selects `project-core` and image groups but not `mssql` for the `chatthreads.py` path (research C1). The sensor fixture constructs `MssqlStore` (C5), which imports and executes the chat definitions (C6, C7).

### Intent

Pin the omission before changing selector source.

### Boundaries

* Included: `tools/test_rpi_checks.py`.
* Excluded: source edits.

### Likely Targets

* tools/test_rpi_checks.py: new regression near the existing sensor selector tests (lines 513 to 640).

### Dependencies

* none

### Validation Expectations

* The new test fails on unchanged `tools/rpi-checks.py` with an assertion about `mssql` not selected.

### Completion Evidence

* Recorded failing run output (command, exit, assertion) in the changes record.

### Unresolved Items

* none

<!-- rpi:task id=P01-T01 -->
### P01-T01: Record the reproduction and add the regression

#### Context

Existing tests resolve suite imports by AST and pin the set exactly (C9) and check the flagged command per path (C10). Receipt mutation tests already reject missing, altered or skipped sensor evidence (C11), so the regression does not duplicate them.

#### Intent

One new test `test_sensor_store_chat_schema_dependency_selects_mssql` that: parses `mssqlstore.py` and asserts it imports `MEMORY_ADDED`, `MSSQL_DDL` and `MSSQL_INDEX` from `.chatthreads` and references the aliases in `MssqlStore`-side code; asserts the fixture imports `MssqlStore`; asserts `chatthreads.py` selects `mssql` while `chat_panel.py`, `chat_privacy.py` do not through the dependency rule. AST usage sites: the `from .chatthreads import` aliases `CHAT_DDL`, `CHAT_INDEX`, `CHAT_MEMORY_ADDED` are referenced in the schema table map, `_migrate_chat_memory` and `_create_indexes`. The `chatthreads.py` path is derived from that import, asserted to be a member of the explicit set and to match no path keyword. Assertions that fail before the fix: the selection assertion, set membership and the added loop subtest; the AST and negative-control assertions pass before and after. Add the `chatthreads.py` path to the loop in `test_changed_core_sensor_paths_select_mssql_and_the_flagged_command` so the flagged command, flag and pinned count are asserted for it.

#### Boundaries

* Included: the one test, one loop entry.
* Excluded: new receipt fixtures, SQL execution.

#### Likely Targets

* tools/test_rpi_checks.py

#### Dependencies

* none

#### Validation Expectations

* `python3 -m unittest discover -s tools -p test_rpi_checks.py -k chat_schema` fails before P02, as does the extended loop test.

#### Completion Evidence

* Failing output captured before the source edit.

#### Unresolved Items

* none

<!-- rpi:phase id=P02 -->
## P02: Make the selector change

### Context

The dependency set is explicit with a comment stating it is not transitive (C2).

### Intent

Add one path and keep every other control as is.

### Boundaries

* Included: `tools/rpi-checks.py` set member and comment; the exact-set expectation edit in tests.
* Excluded: selection logic, SQL command, skip tuples, receipt verification.

### Likely Targets

* tools/rpi-checks.py:205-212
* tools/test_rpi_checks.py:604-609

### Dependencies

* P01

### Validation Expectations

* New regression and the whole module pass.

### Completion Evidence

* Diff limited to the above; passing output recorded.

### Unresolved Items

* none

<!-- rpi:task id=P02-T01 -->
### P02-T01: Add `chatthreads.py` to the explicit sensor MSSQL dependency set

#### Context

The set currently pins `dataset.py`, `synthetic/__init__.py` and `indoor_projection.py`. The existing exact-set test derives the keyword-unmatched direct imports and adds `indoor_projection.py`; `chatthreads.py` is a store-initialization dependency, imported by `mssqlstore.py`, not a suite import, so the expectation gains it explicitly.

#### Intent

Set member `src/core/src/zava_forward/core/chatthreads.py`; comment reworded to say the entries are direct suite imports or exercised store-initialization definitions, explicit and not exhaustive or transitive.

#### Boundaries

* Included: one member, one comment.
* Excluded: renaming the constant (kept for the README and tests that reference it).

#### Likely Targets

* tools/rpi-checks.py, tools/test_rpi_checks.py

#### Dependencies

* P01-T01

#### Validation Expectations

* Full `test_rpi_checks.py` module passes.

#### Completion Evidence

* Command output with counts and exit.

#### Unresolved Items

* none

<!-- rpi:phase id=P03 -->
## P03: Targeted validation and evidence

### Context

Owner-selected demo tier: tool selector and receipt regressions and directly impacted tests; no `--all`, no waiver. The changed invariant is path selection; no SQL behavior or command changes, so an actual SQL run would not exercise the changed code.

### Intent

Record exact commands, counts, exits, skips and the SQL decision.

### Boundaries

* Included: unittest module for the tool, pinned formatter and strict typing for the two files if available, `git diff --check`.
* Excluded: `rpi-checks --all` or `--changed`, SQL containers, Docker, private data.

### Likely Targets

* .copilot-tracking/changes/2026-11-09/chat-schema-sql-selector-1298-changes.md

### Dependencies

* P02

### Validation Expectations

* Unique owned log directory from `mktemp -d`; each producer exit recorded; failures preserved.

### Completion Evidence

* Command, count and exit table in the changes record.

### Unresolved Items

* Residual: `sqlstore.py` function-local and top-level sibling imports stay unselected. The SQL run is judged not needed for a selection-only change; the review records that the real sensor SQL execution at this head is unproven by this attempt.

<!-- rpi:task id=P03-T01 -->
### P03-T01: Run the targeted tool checks and record the tier

#### Context

Pinned tooling versions are in repository configuration; availability in this environment is unverified.

#### Intent

Run: `python3 -m unittest discover -s tools -p test_rpi_checks.py -v`; Ruff lint, Ruff format check and strict mypy for the two tool files (environment ruff 0.17.3 and mypy 2.4.1 differ from the gate pins 0.17.1 and 2.4.0, so results are unpinned and not gate-equivalent); `git diff --check`; the reproduction snippet.

#### Boundaries

* Included: the commands above.
* Excluded: global installs; missing prerequisites are recorded as such.

#### Likely Targets

* none (evidence only)

#### Dependencies

* P02-T01

#### Validation Expectations

* All executed checks exit 0; skipped checks stated with the reason.

#### Completion Evidence

* Table in the changes record and review.

#### Unresolved Items

* none
