---
title: Issue 80 capacity C4 instrumented validation, changes
description: Prospective and actual record for the single observed whole capacity browser execution
ms.date: 2026-11-10
---

## Prospective (written before implement-start)

* No repository source file changes. The only artifacts are tracking records and external evidence (`observer.py` and its raw outputs under `phase80-capacity-c4-validation-evidence-1110/`).
* Work: one whole `capacity_browser_check --axe` via the passive observer on HEAD `2cc34027`, source hashes recorded before and after. Result, first failure and limits to be appended after execution.
* Not planned and not admitted: any checker or application fix, a second run, extra probes, C5.

## Actual: attempt 1 interrupted (recorded on resume, 2026-11-10T23:09Z)

* The single admitted execution STARTED at 2026-11-10T20:47:11Z (after the `implement-start` marker and pre-run integrity: clean tree, HEAD `2cc34027`, tree `b41c022b`, source hashes in `pre-hashes.txt`). The partial event log reached the first seeded capacity axe scan (about 7 s, milestones: GET/render 1 package and 20 work orders, seeded axe zero violations), then stopped. `run.log` carries a Node `TimeoutNegativeWarning` (clock jump), consistent with a VM suspend or reboot (reboot observed by Root at about 23:08Z). No `run.exit` was written. It is NOT a pass and NOT a checker result; the checker produced no failure.
* Preserved byte for byte: `attempt1-interrupted-events.jsonl`, `attempt1-interrupted-run.log`, `attempt1-host-load-start.txt`, `attempt1.sha256`, `attempt1-INTERRUPTED.txt` under `phase80-capacity-c4-validation-evidence-1110/`.
* Reboot wiped `/tmp`: the owned venv, the axe asset and helper scripts were missing (actual missing dependency). Restored in owned locations only: new venv `/tmp/ama-80-audit-venv-1110` with `pip install playwright==1.64.0` and editable installs of the five worktree `src/` distributions (no source-PYTHONPATH workaround for src), axe-core 4.10.3 re-fetched with sha256 `880970c0...a68bb` matching the checker pin, state validator and wrapper recreated. Chromium cache survived.
* One replacement execution (attempt 2) is admitted by Root as the single execution total, because attempt 1 was interrupted before any checker verdict. No second replacement after attempt 2.

## Actual: attempt 2 result (the single replacement execution)

* Command: owned venv python running `observer.py` (sha256 in `observer.py.sha256`) over the unchanged checker, `--axe /tmp/axepk/package/axe.min.js`, from `src/api`, `PYTHONPATH` limited to the allowed test-helper paths (`core/tests`, `agents/tests`, `api/tests`); the five `src/` distributions came from editable installs. Direct python exit written to `run.exit`: `0` (no pipe). Duration about 84 s; host load 3.49 at start, 4.10 at end.
* Result: the whole checker PASSED on unchanged HEAD `2cc34027` (tree `b41c022b`). Source hashes (checker and all `web/` files) identical before and after (`attempt2-pre-hashes.txt`, `post-hashes.txt`) and identical to attempt 1's pre-run hashes. Served assets match the owned files byte for byte except the `/app` HTML shell and `vendor/leaflet.*` (no owned equivalent by name; not defects).
* Milestones in original order, all observed in `run.log` and `events.jsonl`: seeded axe 0 violations; both CSV downloads (packages 1 row, workorders 601 rows); 14 manager routes including `#/aftercare` (with the asserted `/api/aftercare/form` 403, one occurrence) and `#/screens`; initial packages and workorders 503/retry; draft-safe packages and workorders retries; delayed sibling 401 after packages refresh failure (PASS, settled) and after workorders refresh failure (PASS, settled), both iterations executed; mutation-refresh cancel and 401; empty-capacity stage: heading, "No packages yet." and "No work orders yet." visible, `a[download$='.csv']` count 0 (source line 902, executed because the later empty-capacity axe milestone and final PASS line printed), empty axe 0 violations, 401 reload, then `assert not errors / failures / console_errors` and the final PASS line. No skips.
* Observer data: 782 requests, 745 responses, 38 requestfailed (checker's own abort of external tile requests), 73 console error events (all resource-load events for the expected 503, 401, 403 and aborted external requests), no pageerror, no observer_error, ZF_DATA absent, store paths under a temp directory. Non-2xx API: packages and workorders 503 x16 each, 401 x2 each, `/api/me` 401 x1, `/api/aftercare/form` 403 x1, `/api/workorders` 403 x1. A checker-side server log line `http-error GET /api/workorders client-disconnect BrokenPipeError` was printed (existing behaviour, not a failure).
* Not answered: C4-R2 cause of the earlier C3 line-571 failure stays UNKNOWN. This pass shows the stage passes in an observed whole run on this source; it does not explain the C3 failure (host load, timing or a flake remain unexcluded). One sample proves neither stability nor absence of a race.
* Observer limitations as researched apply: not zero perturbation, handler matching inferred, one sample.
* Carried, not re-run: Ruff check and format, Node syntax, API11 and static60 from the C4 commit on the same source hashes.
* Environment: `/tmp` wiped by the reboot; restored in owned locations only after actual missing-dependency evidence.
