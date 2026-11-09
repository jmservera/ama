# Review: ranking archive Blob Bicep wiring (Refs #136, #1258)

* Executed once by an independent read-only reviewer (code-review agent) on exact implementation head `d4c0f42da266308a60ab0ffaeee96294bdedbce4` (tree `1a2f83cb3938958e45714fd36c5eda44119741fe`). Assessed boundary: `git diff f724f4bca..d4c0f42da`. The reviewer ran `az bicep build` and 71 infra tests (OK). Review is not repeated in this task.
* Outcome: Approve. No Blocking or Significant findings; one Minor.

## Findings

| ID | Class | Finding | Routing |
| --- | --- | --- | --- |
| F1 | Minor | `ruff check --fix` (run on the new test lines) also removed the existing `# noqa: S307` note on `evaluate()`; unrelated to this change | Applied directly in the following record commit (line restored; `git diff f724f4bca -- infra/tests/test_bicep_policy.py` no longer touches it). Not re-reviewed |

The reviewer confirmed: conditional container, policy and output are correct; flag-off leaves resources, env and roles unchanged; policy is unlocked with no invented duration; `assert_retention_controls` keeps its two-policy count; README and parameter text make no WORM or durable-release claim and state the residual account-scope delete permission and the configuration-only pilot guard.

## Own evidence (not the reviewer's)

* Commands and exits are in the changes record (build, lint, three `build-params`, 90 infra tests OK, 23 provider contract tests OK). After restoring the noqa line the two new tests were re-run: OK.
* Source and compiled template only. Not proved: provisioning, role grant, WORM enforcement or lock, approved retention duration, folder-record migration, emulator or real-account behaviour, deployment approval, demo runtime. #136 and #1258 criteria stay unticked.

## Routed follow-ups

1. Final integration after the parent #1258 freeze and review (parent C5 listing correction is moving; config interface expected unchanged), then rerun these infra tests on the integrated head.
2. Owner decision: ranking-record retention duration, locking and approval; until then the archive is not immutable or durably released.
3. Platform decision: container-scoped Blob role instead of account-scope Contributor (delete residual).
4. Owner decision: migration of existing folder records (Blob starts empty).
5. Deployment and an emulator or real-account run (owner-gated).
