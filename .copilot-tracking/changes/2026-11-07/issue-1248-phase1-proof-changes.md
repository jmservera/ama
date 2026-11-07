---
title: Issue 1248 phase 1 controlled proof record
description: Observed held-case-read mechanism proof and unchanged base run for the saved-call History readiness failure
ms.date: 2026-11-07
ms.topic: reference
---

## Status

* Phase 1 controlled proof only. Not a repair, not a publication candidate and not a Review. Phases 2 and 3 await separate admission.
* Base source: main 0f420dc9514db22081cb48fa733267d9d33a0d24, prospective head 9e0c29cd37abfab61cf78126772d6335571555a3, tree 6483fbde7219daaeef7e4b4dd34555f612d5efc8 (clean for the base run).
* Heavy lock `/tmp/ama-rpi-heavy.lock` taken non-queued (`flock -n`) for each browser run; no other holder.

## Environment

* Runner: `/mnt/ama-gates/g1248-p1-1107/run.sh` (new, owned). Isolated HOME, TMPDIR, ZF_DATA and scratch under `/mnt/ama-gates/g1248-p1-1107/`; loopback-only audit hook copied from the R4 `safety/sitecustomize.py`; axe 4.10.3 bytes copied from R4 (read-only source).
* Module origin: `PYTHONPATH` lists this worktree's `src/core/src`, `src/agents/src`, `src/api/src` and tests; the check ran from this worktree's `src/api`. Dependencies (Playwright 1.64.1, Chromium) reused read-only from the user site and `~/.cache/ms-playwright`. No install; no R4/R5 environment touched.
* Attempt 0 (`base-attempt0-envfail.log`, sha256 0ff73479...): `ModuleNotFoundError: playwright` because `env -i` hid the user site. Environment fault before any check; corrected with `PYTHONUSERBASE`. Preserved, not hidden.

## Runs

| Run | Log (sha256) | Result |
| --- | --- | --- |
| Unchanged base | `/mnt/ama-gates/g1248-p1-1107/base.log` (3f13a087...) | EXIT 0, 407 PASS. R4 did not recur: bounded "not reproduced". |
| Diagnostic held read | `/mnt/ama-gates/g1248-p1-1107/held1.log` (26b74733...) | EXIT 0, 411 PASS (407 plus 4 diagnostic checks), including the original "saved call reaches actual history". |

* Diagnostic diff (uncommitted at run time): `git diff` sha256 26c891081fb9addf5c6b61a6949df3a4aec243e8c0498633326b078f500ff20a, one file, `src/api/checks/case_journey_browser_check.py`, +49 -2. Ruff check and format clean.

## Observations (held1)

* Routing: `**/api/cases/ZF-1` held only after Save is clicked; the POST `/api/cases/ZF-1/call` does not match it. Route and request listener removed in `finally`.
* Correlated traffic: `["POST /api/cases/ZF-1/call", "GET /api/cases/ZF-1"]`, exactly one held read.
* While held: `#outcome` is empty and the original workspace element is still connected.
* Old-condition read (select History, one `inner_text()`) while held: does NOT contain "Unsaved synthetic call".
* After release: the old workspace detaches, History remains selected (`aria-selected=true`) and the replaced workspace's History panel contains the exact saved call.
* No application error; the call appeared once the read was released.

## Cause Versus Unknown

* Proven (controlled, synthetic): the empty-`#outcome` signal precedes the refreshed History data, so the check's one-shot read can see a History panel without the new call while the post-Save case read is in flight. This is an incomplete readiness signal in the checker, not an application defect: the application renders the call once the read completes (H2 not supported, H3 contradicted).
* Not proven: that this mechanism caused the original R4 failure. R4 timing was not captured and the unchanged base run passed. Attribution of R4 remains "consistent with, not shown".

## Not Done

* No readiness repair, no final Review, no completed state, no push, PR or acceptance tick.
