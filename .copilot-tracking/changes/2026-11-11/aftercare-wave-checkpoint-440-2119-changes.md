---
title: Aftercare numeric-order integrated-main checkpoint changes (Refs #440 #1401 #1402 #134)
description: Changes record for the bounded aftercare checkpoint
ms.date: 2026-11-11
---

## Files changed

* `docs/architecture/cutover-evidence-pack.md`: appended section "Aftercare numeric-order integrated-main checkpoint (2026-11-11, Refs #440 #1401 #1402 #134)" (71 lines). No earlier section altered.
* `docs/reference/README.md`: appended one index paragraph after the 2026-11-10 aftercare checkpoint paragraph.
* `docs/reference/log.md`: appended one entry; earlier entries unchanged. `docs/reference/memory.md` untouched.
* Original RPI artifacts under `.copilot-tracking/` (research, plan, details, critique, changes, review, state), dated 2026-11-11, written in order: research, plan and details, critique, then observation and record, then review.

## Commands (pin `077ad5ad2`, worktree HEAD equal, `src` clean before and after)

| Id | Command (from the stated folder, `env -i`, owned `HOME`, explicit worktree `PYTHONPATH`) | Exit | Result |
| --- | --- | --- | --- |
| Preflight | module origin and hash probe | 0 | all four modules import from the worktree; disk hashes equal pin blobs |
| A1 | `src/core`: `python3 -m unittest test_aftercare -v` | 0 | Ran 23, OK |
| A2 | `src/core`: `python3 -m unittest test_aftercare_store -v` | 0 | Ran 42, OK, skipped 15 (SQL Server opt-in) |
| A3 | `src/core`: `python3 -m unittest test_aftercare_intake -v` | 0 | Ran 39, OK |
| A4 | `src/api`: `python3 -m unittest tests.test_aftercare_served tests.test_aftercare_screen -v` | 0 | Ran 21, OK |
| S1a | `ruff check` on three owned files | 0 | passed |
| S1b | `ruff format --check` on the same | 0 | 3 files formatted |
| S1c | `mypy` on the same, first invocation | 1 | `ModuleNotFoundError: mypy`, caused by `env -i` hiding the user site; adverse, retained, not a product finding |
| S1d | `mypy` rerun once with user site exposed | 0 | no issues in 3 files |
| Doc | `git diff --check` | 0 | clean |

No install, no dependency change, no SQL, browser, cloud or model run, no full gate. Raw logs: `/home/azureuser/.copilot/session-state/38e61c82-3c44-4b97-af59-9eed5c151ac7/files/aftercare-checkpoint-440-2119/` (outside the repository).

## Deviations and limits

* The only rerun was mypy (invocation error, one rerun). No test was rerun.
* Critique findings C-01 and C-05 were rejected with reasons; C-02 to C-04 were applied (see the critique).
* No push, PR, issue or board write. No source, test, tool or workflow change.
