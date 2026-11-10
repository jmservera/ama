---
title: Issue 80 capacity line-754 diagnosis, details
description: Phase details and evidence pointers for the proposed stage correction and the diagnostic observations
ms.date: 2026-11-10
---

## Diagnostic evidence (done)

* Observation 1: `driver-obs1.py`, `obs1-events.jsonl`, `obs1.log`, exit 1 at `capacity-load` (driver readiness defect, target stage not reached).
* Observation 2: `driver-obs2.py` (sha256 `94694a73...4406`), `obs2-events.jsonl` (68 events), `obs2.log`, exit 0. Key events: held two at t=5.292; 503 at 5.293; retry request at 5.795 held by the same handler; phase A no error in 12 s; after releasing three retries the error text at t=22.097.
* Location: `ROOT/phase80-capacity-c3-evidence-1110/`. Exit codes were recorded from the Python process directly (output redirected to files, no pipeline).

## Proposed correction detail (not admitted)

* File: `src/api/checks/capacity_browser_check.py`, stage loop near `hold_capacity_read` (about lines 716-760).
* Mechanism: a mutable flag (for example a one-element list or `nonlocal` bool) read by `hold_capacity_read`:

  * set: if `urlsplit(route.request.url).path == "/api/" + endpoint`, call `route.fulfill(status=503, body="Unavailable")` without appending to `held`; otherwise hold as now;
  * the flag is set just before `failed.fulfill(503...)` and cleared after `expect(status).to_contain_text(...)` passes.
* `capacityHeldReads` is incremented only for held reads so `== 2` waits remain valid; the retry-click phase after the flag is cleared again holds exactly two reads.
* Expected timing: about 5 s of retries (500, 1500, 3000 ms) before the text appears, within the 60 s expect timeout.
* Failure semantics to preserve: a real unanswered retry must still time out visibly; no `try/except`, no timeout increase.

## Validation commands at the exact head (for a future admitted chain)

* `~/.local/bin/ruff check` and `ruff format --check` on the checker.
* `node --check src/api/src/zava_forward/api/web/ops.js`.
* `python -m unittest tests.test_list_export_api` (11) and the five related static modules (60) from `src/api` with the PYTHONPATH used in the C2 chain.
* One whole `python checks/capacity_browser_check.py --axe /tmp/axepk/package/axe.min.js` (the check takes the nonblocking heavy lock itself); record the actual exit and preserve the log.
