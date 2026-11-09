# Changes: issue 144 current-main integration (2026-11-09, Refs #144)

Plan: [plan](../../plans/2026-11-09/issue-144-current-main-plan.md). Research: [research](../../research/2026-11-09-issue-144-current-main-research.md).

## Identity

* Start d2d9560694622441fc8b2ad146cccd9c765535c4; plan commit cae235e12f04d5aa95e99a08c10887c449851379; ordinary merge 1046ef8c4ef9188568687c49a0eaed453657ec12 (tree 981ea4b13c409ab28fa2530a7e80463fd4412301) of origin/main df8e858b2150198e5e22c73d224a0d3592c73daa. Final frozen head and tree are reported in the handoff after the closing commit.
* The merge applied with no conflict. The predicted tree 464ce964 differs from the result only because the plan commit added three records first (expected).

## Verified invariants

* `docs/reference/log.md`: HEAD to merge adds 8 lines (main's) and deletes 0; merge versus main adds 17 and deletes 0; headers of both histories retained. This lane then appended one entry.
* No `.copilot-tracking` record modified or deleted versus d2d95606.
* `src/agents` empty diff versus approved 63d7f8c1 and versus the pre-merge head; `queue_azure.py:124` still sends `x-ms-date`.
* Versus main, source, infra, tools and workflow differences are only the queue adapter, its test and `infra/README.md` (one table row). No dependency manifest or workflow change.

## Executed checks (owner demo-targeted tier; venv /tmp/c1venv, Python 3.12.3, ruff 0.17.1, mypy 2.4.0)

Each producer ran with output redirected to its own file and exit read directly; logs are under `/tmp/rpi144-cm/` (not committed) and none was rerun or overwritten.

| ID | Command scope | Exit | Result |
| --- | --- | --- | --- |
| A1 | `src/agents` unittest test_queue_azure test_worker test_dispatch test_dependency_rule | 0 | Ran 49 OK, 0 skips |
| A2 | `test_queue_azure.RequestDateTests` (positive Date contract) | 0 | Ran 3 OK |
| A3 | Same class against a mutated copy outside the repo with the `x-ms-date` line removed (module path confirmed as the copy) | 1 | Ran 3, errors=1: `test_every_operation_carries_a_current_utc_request_date` raised `QueueError` status 403; the two contract-transport tests passed. Expected negative result, not a product failure |
| A4 | `ruff check agents` | 0 | All checks passed |
| A5 | `ruff format --check agents` | 0 | 43 files formatted |
| A6 | `mypy src` in `src/agents` | 0 | Success, 20 source files (narrower scope than the earlier 48-file invocation; stated, not equated) |
| C1 | `src/core` unittest test_live_readings test_device_provision test_sensor_analysis_store test_sensor_consumer_live test_paired_equity | 0 | Ran 72 OK, 0 skips |

* Not run: `rpi-checks --all`, API live or SQL tests, browser, cloud, model, deployment. Main's own API and SQL checks are not selected: this branch's source is the queue adapter only and merges byte-equal to main elsewhere.
* Whitespace: `git diff --check` on authored tracking and log additions reports 0 findings; inherited main content untouched.

## Evidence limits

Local results do not show hosted mergeability or CI. Date negative proof is a mutation simulation of the request contract with a scripted transport, not the live service. All five live acceptance criteria remain unproven.
