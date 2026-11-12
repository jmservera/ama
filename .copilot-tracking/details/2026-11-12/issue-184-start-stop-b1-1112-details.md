<!-- markdownlint-disable-file -->
# #184 stage B1 start/stop retry enforcement: details (2026-11-12)

Per [plan](../../plans/2026-11-12/issue-184-start-stop-b1-1112-plan.md).

## Design

* `send_slot(..., attempt_gate: Callable[[str], bool] | None = None)`. In `one(home)`, after `await pacer.admit()` and immediately before `sink.send`, call `attempt_gate(home)`. A False, or an exception from the gate, counts one `RUN_CONTROL_FENCED` code and one failed home, and returns without sending or retrying. Fail closed on any gate exception.
* `run(..., attempt_gate=None)` passes it through; when a slot reports `RUN_CONTROL_FENCED` the run ends after reporting that slot instead of sleeping to the next boundary (the next slot gate would stop it anyway).
* `attempt_permitted(control_path, home, moment) -> bool`: `live_control.load`, `decide == SEND` and `home in control.homes`; a `StreamError` returns False. `main` passes `lambda home: attempt_permitted(control_path, home, datetime.now(UTC))` only when `--control-file` is set; otherwise None (no read, defaults unchanged).
* Summary gains no field; the fence appears in `codes` and `failed`, so `_report` is unchanged.

## Tests (failing first)

* send_slot: gate False before first attempt sends nothing; gate flips False after a transient failure so the retry is not sent and backoff is not repeated; gate flips during pacing delay (checked after the sleep); a raising gate fails closed; gate always True matches the no-gate result (regression).
* run: fenced slot ends the run without sleeping to the next slot.
* Production path: `attempt_permitted` for send, stopped, expired, over-window, removed home, unreadable and corrupt file; `main` with a patched sink whose first send rewrites the real control file to stop (and, separately, remove the home) and a transient failure, asserting no later sink attempts; `main` without control sends as before.

## Validation

Targeted unittest on the two files with `PYTHONPATH` set to this worktree, ruff check and format check, mypy on the changed files. No heavy SQL, cloud or browser.
