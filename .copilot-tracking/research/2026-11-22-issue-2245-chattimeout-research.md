# Research: issue 2245 chat ask with no response within 120 s (live demo)

Date 2026-11-22. Disposition: executed. Planning Readiness: Ready. Parent task: issue-2245-live (honest hold reporting, merged as PR 2249).

## Evidence

* Probes (`docs/reference/research/issue-2245-chattimeout-2026-11-22/`): `probe_ask_latency.py` (timed API asks after a desktop Playwright sign-in), `probe_ui_first_ask.py` (UI ask right after the workbench loads), `healthz_poll.py`. Credentials were read at run time and asserted absent from every output file.
* Revision 0000051, five runs, about 45 asks: typical 3.0 to 4.3 s per ask with no model call; first ask after idle 56 s, 26 s and 6 s in three runs; no ask reached 120 s.
* Control: asks refused before admission (no `chat_admission`, no meter) take 3.07 s; asks on the hold path take about 4.1 s. The hold path therefore costs about 1 s more than a refusal.
* Azure OpenAI latency is excluded for the current state: every non-refused ask returns `AI answers are on hold because an open suspension covers AI work, so no model was called` (open suspension SUS-1, parent research). The caller principal cannot call the model data plane (HTTP 401 PermissionDenied), so a direct model latency timing is unavailable.
* Worker hang excluded: no restart (`restartCount` 0), the replica kept answering; `/healthz` polled every 0.5 s during asks stalled once up to 14.8 s (3 of 122 polls slow), then recovered.
* Failure observed on revision 0000052 after 7 min idle: one `POST /api/chat/threads/<id>/ask` returned HTTP 500 after 19.4 s; container log `http-error ... exc=ProgrammingError`. The earlier thread-creation 500s of 17:51 and 18:01 carry the same `ProgrammingError`, and `/healthz` client disconnects fall in the same windows.
* App Insights and Log Analytics queries are denied for this principal; the container console log is the only server evidence.

## Cause (supported by code, not by server telemetry)

* Azure SQL writers serialise on one exclusive application lock: `BEGIN IMMEDIATE` runs `sp_getapplock ... @LockTimeout = 15000` and `THROW 50002 'could not take the write lock'` (`mssqlstore.py` `BEGIN`). The THROW surfaces as `ProgrammingError`, matching the 500s. 19.4 s equals the 15 s lock wait plus the 4 s ask.
* The API holds `store.dblock` while it waits for that lock; `/healthz` (`ready()`) needs the same lock, which explains the stalled probes. One ask performs several lock acquisitions in sequence, so contention compounds toward the reported 120 s.
* On the model path `chat_admission` runs `chat_demo_meter.ensure` before and after every model call. Each `ensure` runs `ledger.price` and `ledger.authorize`, each opening a new SQL connection, taking the same exclusive lock in a SERIALIZABLE transaction and rereading the whole ledger, although the records already exist after the first call of the day. That is avoidable lock traffic and latency in the demo's most important path.
* Contenders for the lock in the live demo are other writers on the shared demo database (the other replica during the 0000051 to 0000052 overlap, and concurrent test sessions). Which writer held the lock during the original 120 s ask cannot be read without telemetry.

## Decision

Smallest in-code cause: seed the demo chat meter once per day and configuration per ledger instead of on every admission check. Do not change `LockTimeout`, the suspension hold, or the deployed revision (no production change authorised). The 120 s incident itself is not reproduced; the residual stalls are recorded as an unproven follow-up needing telemetry access.
