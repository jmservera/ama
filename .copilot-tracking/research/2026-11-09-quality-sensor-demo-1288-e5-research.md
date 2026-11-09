# Research: issue 1288 E5 (final correction of the independent E4 findings: 1 High, 2 Medium)

Disposition: executed. Task `issue-1288-e5`, parent `issue-1288-e4`. Fifth and FINAL additional cycle after historical C1-C8 and E1-E4; zero remain after it. No reset, renewal or sixth cycle. Refs #1288 only. Original C1-C8, E1-E4 artifacts and the independent adverse E4 findings are retained unchanged. Start `25434bb03d51416564bb5a21ccfe6afe513d3c19` (tree clean). Source of findings: coordinator `independent-1288-e4-final/functional-findings.json` (read in full), `handoff-1288-e4.md`, `handoff-1288-e4-sql-validation.md`, `demo-rpi-common.md`.

## Findings in scope (exactly these three)

* F1 High: the simulation route uses `Assistants.dispatch_hold` (suspension and release only) as its admission gate. It omits `Assistants.disabled`: missing or invalid `ZF_ASSIST_AUTHORITY` and allowances, expired `ZF_ASSIST_EXPIRES`, exhausted `assistant_allowance`, schema error. It never reserves or debits the durable pool, owns no active-call slot and has no completion or uncertainty accounting. Each POST mints a fresh single-use seal, so seals do not bound calls.
* F2 Medium: `ops.js` says "It cited N stored readings" using `proposal.readings`, which is the full set supplied to the request (`Lane.compose`), not the set cited by `output.findings`.
* F3 Medium: `_read_key` guards only `lstat`; a mode 000 regular 32-byte key passes the unsafe-mode test and `open` raises `PermissionError`; `Lane.open` has further unguarded sqlite connect and `SqlStore` or `sim_meta` failures. `App.__init__` catches only `Unavailable`, so an optional lane aborts the whole App.

## Evidence from the E4 tree

* `Assistants.claim` is the one place that owns the durable authority contract: `disabled(db, capability)` (schema error, SQL, valid limits, suspension, release admission, expiry, AI configured, allowance), then active-call slot count (`assistant_attempts.active_until > now` against `limits.active_calls`), then pool upsert with `min()` against configuration, exhaustion check, then `used_calls+1`, `reserved_tokens+reservation` and an `assistant_attempts` row, all inside one `BEGIN IMMEDIATE` transaction (`serialized` on SQL Server). `Assistants.complete` settles it: refunds unused reservation only when valid usage is present, otherwise the reservation stays as liability (uncertainty), and releases the active slot except after timeout or provider-unavailable (slot held to lease expiry). `execute` additionally holds a process-local `call_slots` bounded semaphore for the physical call.
* The existing task path cannot be used as is: a task needs a working-store case snapshot and the private route is intentionally off. The fix therefore factors the allowance, slot, reserve and settle statements out of `claim` and `complete` into shared helpers and calls them from a new simulation admission, rather than copying them, adding a flag or substituting the global financial meter.
* `assistant_attempts` rows carry an opaque `task_id`, `fence`, pool, reserved, actual and outcome; nothing else reads them except `claim`, `renew` and `complete` (grep). A simulation attempt id built from the single-use nonce reference needs no case, document or free-text join.
* `Lane.request(ai, hold)` currently calls `hold()` before and after the call. `Ai.evidence` runs seal verification before data hold, meter, token and socket (E4); admission must therefore run before `Lane.mint`, so a declined request creates no seal row and no sealed call.
* The Lane owns `proposal.readings`: list of `[reading_id, temperature_c, humidity_pct]` captured from `sensor_view.citations(sensors)` at request time and stored with the validated output in `sim_proposals.body`. A citation key is `sensor:{sensor_id}:{reading_id}` (`sensor_view.key_of`). `assistants.validate_output` requires 1 to 12 findings with each citation present in the snapshot, so a validated output always has findings, but a stored or historic row may not, and `source:home` is a legal citation. The UI must nevertheless render zero sensor citations and an empty findings list safely.
* `SqlStore` construction runs schema and migration code on the file and may create `sim-docs` and `sim-digests` directories, so open can fail with `sqlite3.Error` or `OSError` after a connection exists; `Lane.__init__` then queries `sim_meta`, which fails with `sqlite3.OperationalError` on a missing or malformed table.

## Design decisions (E5)

* D1 One shared authority transaction. Add `Assistants._reserve(db, now, attempt)` and `Assistants._settle(db, attempt, envelope)`, called by `claim`, `complete` and new `begin_call`/`end_call`. `begin_call(capability, chars, call_id)` runs `disabled(db, capability)`, the input bound, the active-call slot and the durable reserve in ONE transaction, then takes the process-local physical `call_slots` non-blocking; refusal returns the reason and releases everything. `end_call` settles (unknown usage keeps the reservation as liability, timeout and provider-unavailable keep the slot to lease expiry) and always releases the physical slot. No read-only check, no caller flag, no new approval, no global meter substitute. The real Ai financial meter still runs afterwards and is unchanged.
* D2 `Lane.request` takes an `Admission` of `hold`, `begin`, `end` callables; it admits before minting the seal and settles in `finally`. `App` builds the admission from its real `Assistants`. A declined request returns status `held` with the reason and the manual route; nothing reaches meter, token or socket.
* D3 Derive `cited` from the stored validated output and stored supplied readings at read time (`last_proposal`), keeping `readings` as supplied. This also fixes historic rows without a new migration and preserves historic IDs and values after current readings rotate. UI wording: "Supplied with N stored readings. Cited M of them." with the cited IDs listed, an explicit "It cited no sensor readings" line, and the supplied list in a native disclosure.
* D4 Translate key open or read `OSError`, a short read, sqlite connect, `SqlStore` construction and `sim_meta` failures to explicit `Unavailable` codes (`key-unreadable`, `store-unavailable`, `store-not-simulation`) at the lane boundary only, closing any partially built store. `App.__init__` already catches `Unavailable` narrowly and is unchanged.

## Tests to write failing first

* Real HTTP POSTs against the production App with a real `Ai`, loopback TLS peer, counting meter and token: missing, invalid, expired, exhausted (calls, tokens after an unknown-usage call), schema-error and parallel POSTs under `active_calls=1` decline with zero meter, token, socket; valid bounded call works and its slot and reservation settle (including provider failure and unknown usage).
* Browser check (production `ops.js`): one cited of 12, zero sensor citations, empty findings, and unchanged supplied IDs after rotation.
* Forced `PermissionError` at the key `open` and a malformed `sim_meta` through real `App` construction; the working App still serves manual routes; partial stores are closed.

## Disclosed limits that remain (not solved here)

* No actual provider or admission activation, no live, Azure, model or financial call; the finite LIVE step stays unperformed.
* The withdrawal and suspension race before the socket is still not atomic (public synthetic data only).
* SQL for the new admission reuses the already SQL-Server-tested statements; the owned SQL concurrency run is required only for the refactored `claim` and `complete` and is subject to the single non-queued heavy admission.
* Current `main` `daf45a46` is a paper-only advance with no relevant source; the SQL 1292 fix is published PR 1308 but not on main, so no integration or copy of unmerged sibling work is made.

## Planning Readiness: Ready

Plan: [plan](../plans/2026-11-09-quality-sensor-demo-1288-e5-plan.md).
