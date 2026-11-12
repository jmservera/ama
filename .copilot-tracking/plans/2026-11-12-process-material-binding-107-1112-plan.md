# Plan: issue 107 material-binding change then fresh-process re-admission

Date: 2026-11-12. Prospective; committed with its critique before any code.

## Scope

* `src/api/tests/assistant_process_worker.py`: optional `variation` spec, an explicit enumerated set `("rule", "purpose", "roles")` applied to one named capability in that worker process only. Unknown kinds raise. Constructed runtime-binding difference, not an old image.
* `src/api/tests/test_assistant_release.py`: in the `ProcessRaces` mixin, one shared helper and three test methods (one per variation). No production, runner, schema, workflow, provider or activation change.

## Scenario (helper `check_changed_binding_process(kind)`)

1. Test process invokes pending proposals: `p` (stock-prioritisation, ZF-1), `held` (stock-prioritisation, ZF-2, never seen by the changed worker), `c1`, `c2`, `c3` (distinct unrelated capabilities that keep matching releases).
2. Wave `control`: original-binding worker executes `[c1]` -> `[True]`; one provider call; keep pool and attempts as baseline.
3. Wave `changed`: worker with the variation on stock-prioritisation executes `[p, c2]` -> `[False, True]`. Exactly two calls overall; `p` disabled with "Release admission denied", attempts 0; `held` still pending; stock release `fx-stock-prioritisation` persisted `revoked` with an `invalidated` cause by the system; unrelated releases still `active`; pool calls/tokens/expires unchanged and `used_calls`/attempts equal 2.
4. Wave `fresh`: new original-binding worker with a larger allowance configuration executes `[held, c3]` -> `[False, True]`. `held` is denied only because the persisted revocation survives (its binding matches the original record), no refill: pool stored values unchanged, `used_calls` 3, three provider calls total, `held` attempts 0 and one disabled event, stock release still `revoked`, unrelated releases `active`.
5. Distinct child pids are asserted by `finish`; waves run sequentially, no sleeps or scheduling assumptions.

## Checks (LIGHT, no services)

* Fresh venv with `pip install -e` of this worktree's core, agents, api[dev]; origin check of `zava_forward` modules; no uv, no source `PYTHONPATH` for packages (only the existing `tests:../core/tests:../agents/tests` test-module path).
* Focused: new methods, then `test_assistant_release`, `test_assistants`, `test_assistants_dispatch` as the impacted controls; ruff check, ruff format check (file excluded; worker is checked), mypy for the api project.
* Mutation proof in a throwaway copy only: a variation that does not change the binding (or the invalidation made read-only) must fail the new test; record the result.
* MSSQL methods skip without `ZF_TEST_MSSQL=1`: disclosed as not executed. No blanket FULL gate; classification: focused tier (test-only, non-gate tooling).

## Commit

Identity from `gh api user` (repository-local noreply), Conventional Commit `test(assistants): ...`, `Refs #107` and `Refs #104`, Copilot trailer. No push, PR, merge, board or issue change.
