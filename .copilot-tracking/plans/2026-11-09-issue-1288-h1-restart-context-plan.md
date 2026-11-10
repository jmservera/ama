<!-- markdownlint-disable-file -->
# Plan: issue 1288 H1 restart-context diagnostic

Readback `date -u` 2026-11-09T23:37Z. Research: `.copilot-tracking/research/2026-11-09-issue-1288-h1-restart-context-research.md`. Details: `.copilot-tracking/details/2026-11-09-issue-1288-h1-restart-context-details.md`. Verification only; no correction cycle; one critique, one observation, one review.

## Steps

* [ ] 1. Record research, plan, details; run ONE critique before any observation.
* [ ] 2. Write an external disposable harness (not shipped, not a test edit) with one test: variants A and B as in research.
* [ ] 3. Make ONE non-queued `flock -n /tmp/ama-rpi-heavy.lock` admission; inspect the holder first; if busy record the block and stop with the exact unexecuted step (no queue, spin, kill, container reuse, waiver).
* [ ] 4. Owned fresh venv from the hash-locked requirements only if the earlier venv is gone (it was deleted), loopback SQL container, scratch under `mktemp`; no secret logging.
* [ ] 5. Record changes and review; classify H0 as failed-inconclusive (unchanged) and H1 separately; commit records only; write the handoff.

## Amendment after the one critique (readback 2026-11-09T23:38Z)

* Variant B does NOT call `release_support.install` and does not write to the database. It builds `store2 = open_store()`, an independent `CapturingProvider()` (as `ready()` does with no overrides), sets `model_version` and `model_version_strong` to `test-model` and `ai.release = store2.release_context`, in memory only. The existing `fx-*` rows are reused unchanged.
* Record per service: `runtime_binding` digest, stored task release reference, current `release_reference`, `release_denial`, suspension (`held`), `epoch_current`, `actionable`. Snapshot all `assistant_releases` (id, SHA-256 of body, revision) and the task row through a fresh raw connection before the first service read, after A, after B; they must be identical.
* Confirmation requires: first flag `review-suggested`, A `not-current`, non-empty cited IDs, durable rows unchanged, A guard explained by a recorded field (release denial or reference mismatch), B equal to the first service.

## Pass and fail definitions

* Hypothesis confirmed: see the amendment above; B is equal to the first service on IDs, role projection and flag status.
* Alternate reason: A and B differ in some other recorded field; report it, run no further case.
* Still failing: B differs from the first service; preserve the smallest repro and owner; no E12 and no defect classification beyond the observed fields.
* Harness error is inconclusive, never a pass.
