<!-- markdownlint-disable-file -->
# #184 stage B1 start/stop retry enforcement: changes (2026-11-12)

Per [plan](../../plans/2026-11-12/issue-184-start-stop-b1-1112-plan.md) and [details](../../details/2026-11-12/issue-184-start-stop-b1-1112-details.md). Refs #184 only.

## Source

* `src/api/src/zava_forward/api/live_simulator.py`: `attempt_permitted(control_path, home, moment)` (fresh `live_control.load`, `decide == SEND`, home in `control.homes`, `StreamError` is False); `send_slot(..., attempt_gate=None)` asks it after `pacer.admit()` and right before every `sink.send`, so retries and post-pacing or post-backoff attempts are covered; a False or an error counts `RUN_CONTROL_FENCED` and one failed home; `run(..., attempt_gate=None)` ends after reporting a fenced slot; `main` wires it only when `--control-file` is set.
* `src/api/src/zava_forward/api/live_control.py`: docstring only (states the per-attempt recheck and the no-recall qualification).

## Tests

* `test_live_simulator.py` `AttemptGateTests` (6): closed before first attempt, stop between a failed attempt and its retry (after backoff), stop during a pacing delay, raising gate fails closed, open gate identical to no gate (messages, attempts, sleeps, summary), run ends on a fenced slot.
* `test_live_control.py`: `AttemptPermitTests` (2) on the production `attempt_permitted` (send, other home, expired, stopped, over-window, missing and corrupt file) and `MainAttemptFenceTests` (6) through `main` with the real control file rewritten by the sink mid-slot (unchanged, stop, stop before retry, cohort removal, expiry, corrupt file).
* Failing-first: 14 errors before the change (missing `attempt_gate` and `attempt_permitted`), then 79 pass.

## Amendments and divergences

* One shell Python snippet was used to insert the new test classes (the file-change rule prefers the edit tool); all later edits used the edit tool and `ruff format` normalized layout.
* The proposal row's per-process attempt cap was not implemented (not admitted by the owner's clarification); recorded as unmet.
* Default editable install resolves `zava_forward.api` to another checkout, so all runs set `PYTHONPATH` to this worktree; identities are in the coordinator evidence folder.

## Not changed

No schema, run manifest, SQL, Bicep, permission, real model guard, worker, UI, cadence, identity, service or dependency file. No push, PR or issue edit, deployment, Hub, device or model call, or spend. B2, D1 to D6 untouched.

## Validation

Targeted only: `tests.test_live_simulator` plus `tests.test_live_control` (79 OK), `tests.test_simulator_admin` (30 OK, adds `api/tests` to the path), `ruff check`, `ruff format --check`, `mypy` on the three changed Python files (all clean). Raw commands, output and exits are in the coordinator folder `files/184-start-stop-b1-1112/`. Not run: complete gate, SQL, cloud, browser, hosted CI.
