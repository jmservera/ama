---
title: Issue 2202 live3 changes
---

Refs #2202. Status: complete. Tier: FULL (src change); `rpi-checks.py --all` not run, gates are the coordinator's.

## Changes

* `src/core/src/zava_forward/core/chat_panel.py`: new `_retry_lock_busy` helper; the question save and the answer save both retry up to `SAVE_LOCK_RETRIES` times on the SQL write-lock timeout.
* `src/core/tests/test_chat_panel.py`: `lock_busy_saves` takes the saved role; new test for the question save (3 calls after 2 failures, re-raise on exhaustion). It fails without the change.
* Docs: [live note](../../../docs/reference/research/issue-2202-live-2026-11-27-r3.md), raw evidence in `docs/reference/research/issue-2202-live-20261127T090220Z/`, index and log entries.

## Validation run

* `tests.test_chat_panel` 65 OK; `tests.test_chatthreads`, `tests.test_chat_memory` 57 OK; ruff check and format clean; mypy in `src/core` shows the same 3 pre-existing errors as the base (opentelemetry stubs, one unused ignore), none new.
* Not run: full local gate, API suite (no API file changed), hosted CI.
* Azure: read-only; no resource created or changed.

## Per-criterion table

| Criterion | Status | Basis |
| --- | --- | --- |
| Images rebuilt from main and rolled | Partly proven | Four workloads run; API image predates #2448; provenance unreadable (registry firewall) |
| Revisions Running and Healthy | Proven | az-state.txt |
| Hardening enforced, rollback noted, agents difference explained | Proven; rollback noted, not exercised | enforced on 3 apps and 5 jobs; agents idle by design; no drills authorised |
| Owner demo checks: sensor charts | Proven | chart probe, 30 of 30 GETs 200 |
| Map gauges | Proven | card probe |
| Consent checkbox | Proven | resident probe |
| Chat routing | Proven | six questions; one 500 retried, fixed in source, not deployed |
| Half of homes with readings | Proven (58.9%) | coverage tool |
| Live receipt and log entry | Proven | live note and log |

Unproven: provenance, rollback drill, live effect of the new retry (needs an image rebuild and roll).
