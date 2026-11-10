<!-- markdownlint-disable-file -->
# Issue 189 C2 browser check research (2026-11-09)

Task `browser-check-189-c2`; parent `validation-recapture-189`. Refs #189 only. Research disposition: executed (read-only inspection plus bounded real Chromium observation; no repository edit). Base HEAD `bd7a3fb8e28a1c61dae0aac5f0bcfa320b9d4c8c`, tree `eb95eaf45148b4abe68292d3aa163647031261df`, source trees equal `d985f1495`; fetched `origin/main` `ef28d4da42d83b111d48f14df9b70e3c4932a477`, unchanged for `src`, `infra`, `tools` since `8d6f029ca`.

## Failing evidence retained

* Recapture (`capture-189-validation-recapture`, outside the repository): browser/axe exit 1 and diagnostic reruns 0, 0, 1, so 2 of 4 failed at `src/api/checks/simulator_control_browser_check.py:156` (`assert json.loads(control.read_text())["enabled"] is False`) after the first Stop, with only 3 of 11 states completed. The server logged `http-error POST /api/admin/simulator-control/stop client-disconnect exc=BrokenPipeError phase=response-write`.
* C2 baseline, unmodified source, six fresh runs in `capture-189-c2-browser` (outside the repository): exits 0, 0, 0, 0, 1, 0. Run 5 failed at line 156 with the same assertion and the same server log line; it completed 3 states (unavailable, rejected start, permitted). Cumulative adverse: 3 of 10 observed runs failed at line 156. None is waived.

## Localisation (real Chromium, probe `probe_stopped_wait.py`, exit 0)

With the control file `enabled: true` and the screen loaded, before any Stop click:

* `page.get_by_text("Stopped", exact=False)` already matches 1 element: the always-visible Stop form paragraph "A stop takes effect ... Stopping again is safe if the control is already stopped or expired." (`simulator-control.js:116`). The match is case-insensitive substring, so "stopped" in "already stopped" counts.
* `page.get_by_text("Stopped", exact=True)` matches 0 before the Stop.
* The non-exact `wait_for()` resolves immediately while the control file is still `enabled: true`.

Cause (confirmed, not a hypothesis): the check at line 155 is satisfied by static help text, so line 156 reads the file before the Stop POST has been handled. The assertion races the server write. The `BrokenPipeError` on the stop response is the consequence of the check ending the run and closing the browser while the request was in flight, not a product fault.

## Product judgement

The product behaves correctly. After a Stop the UI re-renders and sets the notice `Stop saved and read back.` only after the server write and read back (`simulator-control.js:57-64`); this is the completed stop response. The Stop form tests that follow already synchronise on that notice (`stop_state`, line 95). No product defect is evidenced; no product change is needed. The same non-exact pattern appears at line 149 (`Permitted`); in the observed states no always-visible text contains it before the Start, and the Start response is awaited by the file assertion after rendering, so it is not part of this confirmed defect and stays unchanged.

## Scope and cycle

C1 one of five productive cycles spent; C2 is explicitly authorised within the standing five total; three remain after C2. No grant or reset. Only the check synchronisation at line 155 is in scope.

## Planning Readiness

Ready.
