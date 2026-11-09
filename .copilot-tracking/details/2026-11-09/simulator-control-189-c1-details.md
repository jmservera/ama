<!-- markdownlint-disable-file -->
# Issue 189 C1 details (2026-11-09)

Plan: [plan](../../plans/2026-11-09/simulator-control-189-c1-plan.md).

## P1 source

* `simulator_admin.py`: `MESSAGES["VIEW_ONLY"] = "Administrator access shows every option but changes nothing; a staff role is needed to act."` (same text as the server gate), `STATUS_FOR["VIEW_ONLY"] = 403`. In `handle`, after the admin check and before any file access: if `method != "GET"` (any non-GET under PREFIX) and `user.get("view_only")` is truthy, return `_reply("VIEW_ONLY")`. Mirrors the server gate semantics. `_status(path, now, read_only=False)` adds `read_only` and sets `writable` false when read-only; `GET` passes `bool(user.get("view_only"))`.
* `server.py`: POST hook moves to immediately after the `view_only` refusal, so the existing denial and message apply first; GET hook unchanged.
* `workbench.py`: `access` is "available" unless `user.get("view_only")`, then "needs a role with this authority".

## P2 tests

* `test_entra_authoritative.py`: restore original assertion (git restore of the edited lines).
* `test_simulator_admin.py`: module `self.admin` becomes administrator with a staff assignment (`view_only=False`); new `self.read_only` (`view_only=True`). New tests: module start/stop denied for `read_only` with valid revision (file and `.lock` absent or byte-identical, no audit), GET works with `read_only: true`, `writable: false`; HTTP start/stop denied for administrator alone with a valid revision and CSRF, file bytes and audit entries unchanged; HTTP success uses `(ADMIN, STAFF)`; navigation entry "needs a role" for administrator alone and "available" with staff; existing non-admin matrices unchanged.

## P3 screen

`simulator-control.js`: `readOnly = status.read_only`; if read-only, status text "Start and Stop are switched off because administrator access without a staff role shows every option but changes nothing." Else if not writable, existing message. Else: Start form when `status.state !== "send"`; Stop form whenever `status.state` is non-null (parsed control), copy adapted ("Stop the run" with an extra sentence for expired, invalid-window and already stopped: "Stopping saves the disabled state; it is safe to repeat."). No Start precondition for Stop. Loaded `status.revision` used for both.

## P4 browser check

Run as `(ADMIN, STAFF)`; additional scripted states via a synthetic control file written directly: expired enabled (Stop present, click with confirm, file `enabled=false`, cohort and expiry unchanged), invalid window (Stop present), already stopped (Stop present, "Nothing needed changing"), stale (file changed under the loaded page, stop refused with alert, file untouched), rejected (no confirmation, file untouched), error (read-only directory is not reliable as root, so a configured-but-missing parent directory is shown as manual state), view-only administrator context (no forms, manual route text). Axe on each state.

## Critique amendments (see critique artifact)

* `test_entra_authoritative.py` assertion is rewritten (not restored from HEAD): every navigation destination is "needs a role with this authority" for administrator alone.
* Lookalike-path test: administrator plus staff for 404 and administrator alone for 403.
* New HTTP test patches `simulator_admin.handle` and asserts it is not called for an administrator-only POST, proving the server gate.
* Browser check: Stop submitted in send, expired and invalid-window states, verifying loaded revision and result; failed Stop uses a patched `live_control.write` raising `OSError` in the in-process server and asserts the alert and an unchanged control.

## P6 docs

`README.md` sentence that start and stop need an administrator with a staff role; view-only administrators can read status only.
