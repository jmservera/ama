# Research: issue 1288 E4 (isolated public simulation lane for real-AI Quality sensor grounding)

Disposition: executed. Task `issue-1288-e4`, parent `issue-1288-e3`. Fourth of five additional cycles after historical C1-C8; one remains. Refs #1288 only. All E1-E3 adverse findings are preserved (E1 Medium/Low review items, E2 F1 residual and the owner decision, E3 freeze and its R1-R4). Start `7e88abb58`; fresh `origin/main` `ad679b96b` merged ordinarily as `ebb08e21d` (no conflicts, E3 and E1-E2 intent intact).

## Owner decision applied

Owner chose option (b): a dedicated simulation store with a genuinely separate connection, schema and credential, a bundled public fixture case and a sealed capability over the exact payload bytes verified at `Ai`. Not the egress proxy. Safe assumptions and go-ahead were already given; the E3 mistake of stopping to re-ask is not repeated. No reset or renewal of cycles, no live, Azure, model, financial or approval authority is inferred.

## What the current code makes possible (evidence from the E4 tree)

* The model request is `assistants.build_request(task)`: `SYSTEM` plus `canonical({capability, purpose, evidence: snapshot})`. The snapshot is `assistants.capture("quality-evidence", case, sensors=...)`: closed-allowlist case facts, quality records (free text `evidence`), checklists and `sources.sensors` from `sensor_view.capture_source`.
* `sensor_view.capture_source(db, home, reference, now, mssql)` and `view(...)` need only a DB connection that holds the sensor tables and consent control index; the employee view and the model capture already share one function, which is what makes "UI IDs equal model IDs" provable.
* `SensorConsumer` accepts only `SqlStore | SensorMssqlConnector` and writes the controls, consent index, guard triggers and `sensor_reading`. Its quality check also reads `cases(id)` to confirm the home exists. A sensor-only SQLite connector is therefore a small additive reuse, mirroring `SensorMssqlConnector`.
* `Ai._request` builds the exact provider body bytes, then applies, in order: captured-readings refusal (contextvar, no seal exists today), data-protection hold, input bound, meter reserve, token, dispatch check, socket. The AST test `test_ledger_call_is_inside_the_admission_and_completion_path` pins the reserve, dispatch, urlopen, complete ordering.
* `Assistants` holds the working-store release, continuity (suspension) and meter ledger; `Assistants.execute` is the private path and keeps its own captured-readings withholding for a real `Ai`.
* E2 `Boundary.tls_ai()` is a genuine local loopback TLS peer with a counting meter and token counter around a real `Ai`; it is the production transport composition spy to reuse (extended only to record body bytes and serve a configured reply).

## Provenance invariant that a positive design needs

1. Every byte of the model input (system text, case facts, documents, quality records, checklists, sensors, as-of state) is produced by one trusted composer from (i) a bundled public fixture case in source and (ii) persisted observations read from a dedicated simulation store. No working-store case, reading, document or free-text join is possible because the composer takes no such input.
2. The dedicated store is a separate SQLite file with its own marker, store id and schema, opened by a separate credential (an HMAC key file with owner-only permissions) that is not the working store credential, path or `ZF_DATA`.
3. The composer mints a seal: HMAC over (namespace, store id, nonce, SHA-256 of the exact serialized provider body bytes, expiry), recorded single-use in the dedicated store.
4. `Ai._request` verifies the seal over the body it actually serialized, before data hold, meter, token or socket. Absent, altered, expired, replayed, cross-store or mismatching-digest seals are refused with an explicit reason. A captured-readings request with no valid seal is refused exactly as today, so the private path stays OFF and the simulation path does not relax it.
5. Caller payload tokens, booleans, unsigned digests and a self-declared namespace cannot satisfy step 4 because only the lane holds the key.

## What remains impossible to claim

* Withdrawal or suspension between the last Python check and the real socket send is not atomic. It is mitigated (last check immediately before dispatch, completion recheck that discards output) and disclosed. The private path stays disabled for exactly this reason; the simulation lane carries only public synthetic data, so a late send discloses nothing private.
* In-process hostile code that reads the key file or replaces `ai.simulation_verifier` is out of scope (honour-system, disclosed), as with E2's `sends_no_bytes`.

## Scope kept bounded

No egress proxy, no framework or app rewrite, no new service, no private data, no `ZF_DATA`, no real dataset mapping, no deployment or Azure resource, no model call. Missing store or key reports explicit `unavailable` with the manual route, never success. Any architecture note is a CANDIDATE, not approved.

## Planning Readiness: Ready

Plan: [plan](../plans/2026-11-09-quality-sensor-demo-1288-e4-plan.md).

## Residuals after this cycle (planned honestly)

* No live call is made. A real-model demonstration needs a separate finite, verified admission (budget, window, deployment, approver) and one request; that is the exact remaining LIVE step.
* Native assistive technology and live acceptance stay OPEN; whole 1288 stays OPEN.
