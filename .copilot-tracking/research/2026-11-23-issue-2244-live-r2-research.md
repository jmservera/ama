# Research 2244 live r2 (2026-11-23)

Disposition: executed. Planning Readiness: Ready. Owner demo scope 2026-11-18 applies (live Azure read-only, no drills, no production change).

## Evidence

* Live revision `ca-cutover-test-demo-api--0000055` (created 2026-11-23T03:25:45Z, Healthy). `az containerapp exec` md5 of the installed `mssqlstore.py` is bf6f84873dc6bb738cdfb52f73a1a30d, equal to this checkout (HEAD 6e0badf1e1); `_schema_current` appears twice in both. The #2292 fast paths are therefore live (the earlier note said not deployed).
* `/healthz` returned 200 in 0.10 s. Log Analytics workspace `log-cutover-test` is readable now (`ContainerAppSystemLogs`, `ContainerAppConsoleLogs`), which closes the earlier "not readable" gap.
* Real contention on 0000055 (console and system logs):
  * 07:08:05Z the http-scaler scaled to 2; replica `...7vs6x` started 07:08:21Z. Serving replica `...mbzml` returned 503 `sql-write-lock-busy` on `/api/briefing` at 07:09:06Z and 07:10:04Z, so another session held the `zavaforward_write` lock for minutes.
  * `7vs6x` logged `SQL write lock busy at start-up; retry 1 of 7` at 07:09:10Z (the MssqlStore retry works), then exited with code 1 at 07:09:47Z with `could not take the write lock` from `server.py _serve -> lawstore.LawStore.from_env -> MssqlDb -> RuleCardStore.__init__ -> transaction -> _Conn._begin`. Container Apps restarted it at 07:09:57Z.
  * Replica `...pg6mj` (started 07:16:06Z) did the same: three retry logs, exit 1 at 07:18:02Z, same LawStore path.
  * Replicas started 08:49:13Z and 08:50:19Z logged no lock error.
* Root cause (new defect): `MssqlDb` in `lawstore.py` opens its own `_Conn` with `startup_retries = 0` and takes the write lock for its DDL, for `RuleCardStore` init and for `rules.seed()`. The #2273 retry covers only `MssqlStore._open`. A scale-out during a long writer still crash-restarts the new replica until the lock frees. The other replica keeps serving, but it is the same class as the issue.
* StartUp probe is 1 s + 40 x 3 s (about 121 s), unchanged; worst-case retry wait is about 211 s per BEGIN. Not changed (production setting).
* Not run: a deliberate lock-hold drill (owner: no drills) and a live deploy of a fix (owner: no production changes).

## Approach

Enable the same bounded start-up retry on the law store path: `MssqlDb` sets `startup_retries` while it, `RuleCardStore` and `rules.seed()` run, and `LawStore.__init__` ends it in a `finally`. Unit tests use the existing fake driver. Out of scope: a read-only fast path for rule cards (they seed data) and probe alignment.
