# Changes: issue 107 changed-binding process then fresh-process admission

Date: 2026-11-12. Local frozen candidate; nothing pushed, no PR, no merge, no issue or board change.

## Commits (local, privacy-safe noreply identity from `gh api user`)

* Parent and base: `43b2187b918206666c63cb25d8b338be09791118`, tree `67cbe8ede92d4f9f02ac3a3f71d0de06872f6b55` (identical to `feat/demo-ai-integration-1112`). Fetched `origin/main` `4f40e7ea8237e18f13ff962857a4c4f3bdfa974c`, tree `e7360069216dc0a8bc6edee077c9454c691cde04`; the parent is its ancestor.
* `c3f3a49fb` docs(rpi): research, plan and critique records.
* `cfab498810aa58dd5e6d04842a4de6d7967b2215` (tree `e9dc25fca3933633346afb78b48675a8c9521bd3`) test change. This hash was amended once to remove one stray blank line found by the independent review (finding 1); the amended commit is the validated one. The records commit that follows it carries this file, the review and the state record; its own hash is reported in the handoff.

## Files changed (test-only)

* `src/api/tests/assistant_process_worker.py`: enumerated `VARIATIONS = ("rule", "purpose", "roles")`, `vary(kind, capability)` applied inside the worker process before the service is built when the spec carries `variation`; unknown kinds raise.
* `src/api/tests/test_assistant_release.py`: `ProcessRaces.spawn(variation=...)`, `stored_release`, `check_changed_binding_process` and three methods (policy, prompt, permission). The SQLite and MSSQL process classes inherit them.

No production, provider, activation, runner, schema, workflow or dependency change.

## Deviations and adverse results (preserved)

* The records were written before code, but the code existed in the working tree before the records were committed; the commit order is records then test, and this is disclosed rather than presented as strict commit-before-code.
* The test file was edited once through a scripted write instead of the edit tool; content is the reviewed diff.
* The first assertion required the invalidation `triggers` to equal exactly the expected single trigger (an accepted critique correction). It failed for prompt (`['intended_use','prompt','evidence']`) and permission (`['evidence','permissions']`) because the task contract digest also moves with registry text. Raw output is in `evidence/.../01-first-run-exact-trigger-assertion.log`. The assertion was relaxed to assert the expected trigger and bound field are present; the policy variation does produce only `policy`. A second run (`02-focused-three.log`, exit 1) failed because the fresh-process denial text names bound fields (`permission_version`), not trigger names; fixed to assert the field name.
* The critic's finding that unrelated releases are unaffected is asserted (`active`, no `invalidated`).

## Validation (all local, venv `~/.venvs/issue107-binding-1112`, editable installs of this worktree's core, agents, api[dev]; module origin checked inside the worktree; no uv; test-module path only, `PYTHONPATH=tests:../core/tests:../agents/tests`)

| Check | Result | Evidence file |
| --- | --- | --- |
| Three new methods, 3 repeats | each exit 0, 3 tests OK | `03-focused-rep1..3.log` |
| `test_assistant_release test_assistants test_assistants_dispatch` | exit 0, 182 tests, 65 skipped (includes all MSSQL classes and JSON-only/SQL-gated skips) | `13`, `14` |
| `ruff check .` | exit 0 (first run found E501 in a new comment, fixed; raw `05`) | `05`, `10` |
| `ruff format --check .` | exit 0 (the release test file is excluded by project configuration) | `06`, `11` |
| `mypy` | exit 0, 236 source files | `07`, `12` |
| Mutation: variation made a no-op | new policy test fails (`[True, True] != [False, True]`) | `08` |
| Mutation: invalidation forced read-only in the changed worker | fails (`'active' != 'revoked'`) | `09` |

## Not run, not claimed

No disposable SQL, so the inherited `MssqlUnleasedRevocation` methods were skipped and are not SQL evidence; if later wanted they need the maintained selector `test_assistant_release.MssqlUnleasedRevocation` with an explicit nonqueued `--lock-timeout 0` local run. No blanket FULL gate (focused tier: test-only, non-gate tooling; classification recorded in the plan), no hosted CI, no provider call, activation, deployment, secrets or cleanup of shared resources.
