# Details: demo-149-role-workbench-heading-hierarchy-0442

* Date: 2026-11-14

## Phase 1: test module

* Class `RoleWorkbenchStructure(MatrixServer)` crawls once in `setUpClass`: for each of 8 roles it signs in, reads `/api/me` navigation, then renders navigation views, `#/case/ZF-1`, `#/screens`, `#/handoff-waiting`, `#/simulator`, `#/import`, `#/coordinator`, and each discovered specialist screen with and without `&case=ZF-1`.
* Per view it collects visible headings, tables (caption/aria-label/labelledby, `th` scope) and links/buttons without accessible text (aria-label, resolved aria-labelledby, text, or image alt).
* Tests: coverage of roles and views, exactly one non-empty `h1`, no skipped or empty heading levels, `h1` first with the recorded `H1_NOT_FIRST` gap (staff `#/`, `#/all`), named and scoped tables, named controls.

## Phase 2: validation

Run from `src/api` with `PYTHONPATH` set to the worktree `src`, `../core/src`, `../core/tests`, `../agents/src`, `../agents/tests` and `tests`.
