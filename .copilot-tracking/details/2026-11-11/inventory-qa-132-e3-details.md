---
title: Inventory-managed staff intake and independent QA 132 extension E3 details
ms.date: 2026-11-11
---

## Phase 1 identity assertions

* `git rev-parse HEAD`, `HEAD^{tree}`, `git status --short` shows nothing except the untracked or committed E3 records under `.copilot-tracking/*/2026-11-11/inventory-qa-132-e3-*` (any other path stops the stage), and the source identity is asserted against `3c395740` (not the later E3 record commit), `git diff 7e2744cf HEAD -- src | sha256sum` equals `2472c5af...ec44f`, `sha256sum` of the test file equals `1048770a...940c`.
* Success: all equal. Failure: stop and record.

## Phase 2 commands

* Venv under `/tmp` with a new name, `pip install -e src/core[sql] -e src/agents -e src/api[dev]` only if a command fails on an actual missing dependency, otherwise the declared install is the normal setup (existing declared pins only). Assert `zava_forward.core`, `.agents`, `.api` `__path__` start with this worktree.
* Commands, from `src/api` with `PYTHONPATH=tests:../core/tests:../agents/tests`: `python -m unittest -v test_staff_intake_api` (E2 observed 96 run, 36 skipped; expect both new case names to appear for the SQLite base and the JSON subclass, so at least four runs); `python -m unittest -k inventory test_resident_api` (E2: 1 run); `python -m unittest test_role_endpoint_inventory test_dependency_rule` (E2: 26 run). From `src/core` with `PYTHONPATH=tests`: `python -m unittest -k inventory test_resident_decisions` (E2: 48 run, 17 skipped) and `python -m unittest -k test_resident_acceptance_never_clears_technical_or_hazard_gates -k test_quality_dependencies_are_scoped_and_unknown_evidence_cannot_release test_resident_decisions test_quality_procurement` (E2: 6 run, 2 skipped). A zero-test selector is a failure, not a pass. Use the documented invocation (not `tests.<module>`), avoiding the two E2 selector mistakes. Then from `src/api`: `ruff check .`, `ruff format --check .`, `mypy`; and `git diff --check`.
* Record raw log, exit code, tests run, skips with reasons (MSSQL class, SQL-store-contract tests on JSON, opt-in Core SQL). Skips are unobserved, not passes.

## Phase 3 trial merge

* `git fetch origin main` (read-only), `git worktree add --detach /tmp/<scratch> HEAD`, `git merge --no-commit --no-ff origin/main` there. Separate venv or reuse with `pip install -e` pointing at the scratch tree and the import assertion repeated, because an editable install of the topic worktree would otherwise shadow it. Remove the scratch worktree afterwards.
* Expected clean merge: main's extra files are AI-consumption only.

## Phase 4 diagnostic design

* Script `/tmp/diag132/diag.py`, not committed. Build both diagnostic classes explicitly from a mixin: `class Bypass: ...` overriding `declare_inventory`, then `class DiagSql(Bypass, StaffIntakeApi)` and `class DiagJson(Bypass, JsonStaffIntakeApi)`, so the JSON class is patched too (running the original JSON class would be unpatched). The mixin overrides `declare_inventory` to call `super().declare_inventory()` and then `mock.patch.object(Store, "require_resident_clear", lambda self, c, bindings=None: None)` started with `addCleanup(stop)`. This bypasses only the shared resident-clear call after real inventory setup; it leaves safety, evidence, independence and state checks live, and `SqlStore` still records its dependency via its override calling the (patched) base.
* The patch wrapper counts its invocations; a result with zero recorded invocations after real inventory setup is `inconclusive`, never `insensitive`. Run only the two new case names on both classes (a restricted loader, not the whole imported module, so the committed classes are not re-run). Record the exact failing assertion line per case and class.
* Outcome table: `sensitive` if each case fails at a held-accept or held-handover `assert_held` (status 200 rather than 409) or the state assertion; `inconclusive` if another guard produces a different 409 or an earlier error; `insensitive` would be a real finding to route, never fixed here. Case A's acknowledgement is outside the bypass and is expected unchanged. Because the first failing assertion stops a case, the restart assertions in case A and the later-capture assertions in case B are reported as unobserved under the diagnostic, not as sensitive; no extra control is added for them unless a separate script exercises them without changing committed tests.
* The E2 `_inventory_managed=False` control is not repeated and its adverse result is not replaced.

## Phase 6 records

* New files only: `changes`, `reviews`, state update with dated E3 names; the E2 files are never edited. The changes record must state the retrospective E2 ordering, original versus forward adoption, the divergences (if any) and raw exits. Review executed once after implementation and does not claim independence.
