# Research: #1288 correction 4 (C4)

Written 2026-11-08T21:33Z (real clock) before any product or test edit. Refs #1288, #107. No closing claim. Disposition: Research `executed` (native code reading of the committed C3 head); the independent report is orientation, each mechanism below was confirmed in the actual source.

## Start state

* Head `699ec528490de96c99bd70ae025378ddab3a7599`, tree `37e1775238c329330cc16da5ff85df635bd05f5c`, tracked clean, branch `feat/quality-sensor-demo-1288`. Not rebased; #184 stays unmerged and unintegrated.
* Owner authority: C4 is the second of up to three extra bounded cycles for this issue only. Consent, safety, human review, budget and live-model gates are unchanged. No heavy process: an approved disk cleanup owns `/tmp/ama-rpi-heavy.lock` (observed present, 11G free on `/`). SQL Server, Docker, browser and FULL are not started.
* Tier: FULL later (SQL consent/control schema, security-sensitive projection). It is a separately admitted coordinator action and stays PENDING.
* Independent C3 report (`review-1288-699-20261108-functional/functional-findings.json`, read entirely): request_changes, 3 High and 2 Medium. Its surviving red/green outputs agree with mine: `/tmp/c3-green-1.txt` and `-2.txt` had the three gap tests failing with `execute(first)` false after same-bucket arrivals; the final helper in `test_quality_sensors.py` moves `execute` before the arrivals, so the green test no longer covers that ordering. Confirmed.

## Confirmed mechanisms in the committed code

1. High, `sensor_view._controls` (lines 104-136). Completeness is `COUNT(index)==COUNT(control)`. Equal counts with a wrong mapping pass: control A1 (home A, granted), control A2 (home A, declined), index rows (A,A1) and (B,A2). Viewing A loads only A1, every named sensor is indexed, consent is `granted`. `Assistants.migrate` swallows a reconcile failure, and `reconcile_control_home` skips controls with an unparseable or invalid home (and raises on malformed JSON), so a bad unrelated control leaves the wrong index in force. Nothing records whether the index was ever proven exact.
2. High, `Assistants._due` (987-997). `known` is every task for (capability, case) in any release or epoch. `_task_id` includes release reference and continuity epoch but `scheduling_signature` does not, so after a release activation or an epoch change the new exact id is absent while the coarse signature is "known": `_due` returns False for good. Any historical match also hides a non-sensor A to B to A return.
3. High, same function and `claim`. A pending task is recorded with the coarse signature at enqueue. A same-bucket arrival before claim makes `claim` mark it `stale` with no provider call (attempts stays 0). The replacement capture has the same coarse signature, no exact task, so `_due` refuses it until the bucket changes: no current autonomous proposal and zero calls spent.
4. Medium, `_mark_requested` (778-787). For a `leased` task it rewrites `dispatch.trigger` to `requested`. `execute` starts the provider thread while the task stays leased, and `complete` reloads the body, so a returned proactive call is relabelled manual by a request made during the in-flight call. The `claimed` event still says proactive: stored provenance contradicts itself.
5. Medium, `sensor_view.AS_OF_RULE` and `capture_source`. Since C3 a context-only capture is `ok` and context rows may be older than 366 days (30 days around the anchor, capped at the as-of edge) but the shared rule states only a 366-day window. The same rule text feeds the UI (`ops.js` line 49 renders `as_of_rule`) and the model snapshot.

## Design decisions (evidence-based, smallest coherent)

* Index proof: add one tiny marker row (`sensor_consumer_index_state`, id 1) holding `{count, homes:{home_id: sha256(sorted sensor ids)}}`. It is written by `configure` in the same transaction from the supplied controls and by a successful reconcile from the parsed controls. A failed or inexact reconcile deletes it. Reads fail closed unless the marker exists, its count equals both table counts, and the digest of the home's indexed slice equals the marker's for that home (an absent home must have an empty slice). That is three scalar reads plus one primary-key read per request, no fleet scan and no JSON parsing of other homes. Residual risk, stated: an out-of-band edit that moves a row and restores both counts AND the home's digest is out of scope; only trusted `configure` and migration write these tables.
* Scheduling: the throttle compares the current coarse signature with the latest eligible task of the current release and epoch, not any historical task. A pending task that went stale before any dispatch (`attempts==0`) does not count, so it is replaced once. An existing exact task keeps scans idempotent. Release or epoch changes start a new scope.
* Dispatch: freeze `dispatch.trigger` at claim per fence. A request during flight only sets the durable `manual_requested`, which a later claim (retry) reads. Late-request visibility comes from the recorded invocation event.
* Wording: describe the two horizons in `AS_OF_RULE` in one place; UI and model both consume it.

## Out of scope

Web files are not edited (the UI renders the shared rule). Real SQL Server, query plans, browser/axe, release attestation, #184 semantic merge and the live walkthrough remain separate gates.

## Planning readiness

Ready.
