<!-- markdownlint-disable-file -->
# #184 stage B1 single-instance start/stop retry enforcement: research (2026-11-12)

Research disposition: executed (read-only, local). Planning Readiness: Ready.

## Scope and owner direction

* Goal (owner clarification): a running temperature and humidity simulator that can be started and stopped. It is not ticket management.
* After the owner heard the explanation of the existing five-minute stop check and the missing retry check, the owner said "that's it, go ahead, continue with the questions". Admitted scope: stage B1 of the [merged proposal](../../../docs/reference/research/iot-sensor-analytics-research-plan.md#narrow-engineering-design-proposal-2026-11-12-refs-184) (PR 1465, base `5df20e639`), single instance only.
* Not admitted: stage B2 (cross-process SQL ticket pool, deferred, not approved), run schema changes (D1 selects scenario plus exact-ID manifest but this candidate implements none), D4, scanner or model route, cadence, cohort, budget and live decisions. No push, PR or issue edit, deployment, Hub, device or model call, or spend.
* Read: [original](../../../docs/case_study_48_original.md), the addendum, the reference index and [memory](../../../docs/reference/memory.md) (context, not evidence). The addendum is 158 KB; only the #184 simulator parts are relevant and no addendum change is needed for a behavior-preserving transport fence.

## Current behavior (source at base `5df20e639`)

* `live_simulator.run` calls the optional `gate(now)` once before each five-minute slot, then `send_slot`.
* `send_slot` runs `one(home)` per home in batches. Each attempt does `await pacer.admit()` (may sleep for the rate gap) then `sink.send`. A retryable `SinkError` sleeps a jittered exponential backoff and loops. No control read happens between attempts, so a stop, expiry, or cohort removal during a slot is not seen until the next slot, after up to `attempts` sends per home (default 4).
* `main` builds `gate` from `live_control.load` and `decide`; a `StreamError` (unreadable or invalid control) returns False (fail closed). With no `--control-file` (stdout only; iothub requires a control file) the gate is always True and nothing is read.
* `live_control.decide` returns SEND only if not expired, expiry within 14 days and enabled. Cohort membership is `Control.homes`.

## Findings that shape the change

* The smallest fail-closed seam is a per-attempt permit callback evaluated after pacing (and therefore after backoff sleeps, which precede the next loop's pacing) and immediately before `sink.send`.
* The production callback must be a real module function used by `main`, so tests exercise the production decision rather than a test-only predicate.
* The earlier-recorded stage B1 text also lists a per-process attempt cap. The owner's admission for this candidate names read/revalidation, so the cap is not added (not requested, and `attempts` per home already bounds retries per slot). Recorded as an unmet part of the proposal row, not a claim.
* The store is not re-read per attempt: cohort removal means removal from the control document's `homes`. A home deleted from the store mid-slot is not detected until the next refresh. That is an existing slot-level behavior, not changed here.

## Qualifications preserved

* A send already handed to the sink or Hub cannot be recalled; an in-flight `sink.send` is not interrupted. No remote cancellation and no instantaneous termination are claimed. Only later attempts are prevented.
* Single process only: another replica or process reading a different state is not fenced (B2 deferred). Control-file read races (atomic replace, no lock for readers) mean a stop written during the read-to-send interval can still allow that one attempt.
* The 2026-11-11 bounded-plan records (original plan, additive corrected record, original adverse independent review) are historical and untouched. The stream-chronology discrepancy remains Medium and qualified. SELF process qualifications stand: author review is not independent, and this task does not renew any exhausted campaign or grant approval.
* Unknown historical balances remain unknown.

## Planning Readiness

Ready. Evidence: source reading above; baseline 65 tests in the two target test files pass when `PYTHONPATH` points at this worktree (the default editable install resolves `zava_forward.api` to a different checkout, `/home/azureuser/source/ama/src/api/...`, so every run must set `PYTHONPATH`).
