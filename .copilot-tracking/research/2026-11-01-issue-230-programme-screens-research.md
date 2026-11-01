# Research: issue 230 programme manager and coordinator screens

Research disposition: executed (repository inspection). Planning Readiness: Ready.

## Evidence

* Pattern from #226 (merged, 5aea8ced): `src/api/src/zava_forward/api/web/role-screens.js` holds a `registerRoleScreen` registry, a home chooser, `screenTable`, `screenFields`, `screenUnknown` helpers and a read-only `asset-board` screen. Tests drive the JS through node (`src/api/tests/test_asset_board_screen.py`).
* Queue data: `/api/cases?view=all` rows carry `work` from `core/taskqueues.py::context` (owner, reason, handoff with proposed/confirmed receiver, chase owner, resident-update owner, queues). The latest return event (`case.returns[-1]`, with `actor` as sender, `reason`, `from_stage`, `to_stage`) feeds `work.reason` but is not exposed as a distinct field, so returned work cannot be told apart in the shared queue. Handoff sender (`from_name`) is also not exposed.
* Lifecycle and funnel: `/api/coordinator` returns `funnel` rows (stage, entries, exits, returns, reopens, denominator, conversion=None) and `data_limits`.
* Same-home gates: case detail has `work.blockers` (steps for safety, stock, funding, resident, technical), `quality` records, `finance.budget`, `appointments`, `technical`.
* Roles: managers `Retrofit Programme Manager`, `Programme Support Officer`; `Retrofit Coordinator` is a staff role. No separate planner role exists in the codebase.

## Constraints

* Source in `src/`, tests outside the package, no new code in `mvp/` or `prototype/`.
* Missing evidence stays Unknown; screens are read-only (no records changed, no role simulator); research is desk-based hypothesis, validation remains #155.

## Unmet by design

* WCAG 2.2 conformance is not proven by node tests; browser keyboard and axe validation is follow-up (#151/#155).
* Correction cycle 2: see merge-main changes; finance evidence-missing rules.
