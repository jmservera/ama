<!-- markdownlint-disable-file -->
# Release Changes: SAME1288 E7

Plan: [plan](../plans/2026-11-09-quality-sensor-demo-1288-e7-plan.md). Details: [details](../details/2026-11-09-quality-sensor-demo-1288-e7-details.md). Critique: [critique](../challenges/2026-11-09-issue-1288-e7-plan-critique.md) (rework, 4 blocking findings applied before source). Records committed in 3801d2dc4 before any source edit. Refs #1288 only.

## Source commits (parent 3801d2dc4)

* 39b4a70a2 transport: `Window` owns a captured socket and `done`/`expired`/`adopted` state; `OwnedResponse` (per-connection subclass) ends the window only when the body completes or the response closes; `Connection.close` finishes the window only if no response adopted it; `ai.py` closes an `HTTPError`. New `src/api/tests/test_ai_transport_deadline.py` (7 real loopback TLS tests).
* cf3f84692 route: `Ai.send_fence_supported = False`; `Ai._request` refuses a sealed simulation with `real-provider-route-unavailable` before verifier, hold, meter, token or socket; `Lane.request` refuses with the same reason before admission. Scripted lane/worker plumbing sets the capability on a labelled local counted peer. New production-App real-Ai, subclass/delegate and source-assertion tests replace the old unfenced-client test.
* 2c2fc7298 `sensor_consumer.py`: two E501 lines wrapped; ruff format applied (format-only).

## Evidence (logs external, session files/logs-1288-e7/)

* Failing-first: `failing-first-deadline.log` exit 1 (3 FAIL, 3 ERROR of 7); `failing-first-route.log` exit 1 (2 FAIL, 1 ERROR of 3), on unchanged source.
* Green: deadline 7 OK; lane 30 OK; role inventory 23 OK; call-site inventory 6 OK; consumption API 17 OK; assistants 120 OK (58 skipped, SQL/SQLite-only gates); dispatch 2 OK; release 54 OK (4 skipped); c7 45 OK (7 skipped); e2 62 OK (31 skipped); ai_tasks 69 OK; core consumption 42, input bounds 6, sensor consumer 47 all OK.
* Complete profiles, pinned ruff 0.17.1 / mypy 2.4.0: Core SDK-free owned venv (`-e src/core[dev]` only) ruff check 0, format 0 (226 files), mypy 0 (279 files); API (`.venv-1288`, core[sql,blob]) ruff check 0, format 0 (134 files), mypy 0 (211 files). No casts, ignores, stubs or config change.

## SQL qualification

No SQL, assistants or admission source was edited in E7. SQL605/1skip and Core53 at 5827ebede remain HISTORICAL; `assistants.py` differs from that SHA only by the E6 5f44dc4e1 refused-event commit-then-raise change, covered on SQLite and the lane suites but NOT on a SQL Server run at final head. No SQL admission was taken. `impacted-green.log` from E6 contains an earlier inventory failure that was fixed and rerun; it is not uniformly green.

## Limits

* The real-provider simulation route is code-disabled. This is a safety fallback, not demo acceptance; the real-model chain is unproven and whole 1288 stays open.
* Disabling does not prove a transport-side atomic guarantee. The ordinary assistants execute path keeps its post-fence suspension race.
* Socket shutdown ends the local read only; it does not stop remote provider computation.
* `readinto`/`read1` paths are not owned by the window (unused by the client).
* UI Request button remains and renders the refusal via the existing not-sent path.
