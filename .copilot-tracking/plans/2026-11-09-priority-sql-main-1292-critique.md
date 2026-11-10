---
title: Issue 1292 current-main priority SQL regression validation critique
ms.date: 2026-11-09
task_id: 1292-current-main-sql-1109
---

## Execution

* One independent critique pass by a separate read-only `rubber-duck` agent, run once on the final-candidate research, plan, details and first runner draft (`sql-1292-current-main.sh`, never executed). Verdict: Revise. No second critique pass is run for this task.
* Confirmed by the critic: selectors and the 108, 34 and 6 counts are correct, the resident method names exist on all three classes, and no selected test has an identified skip when the opt-in environment is set.

## Findings and dispositions (all compatible; applied before implementation)

* C1 High, false success: the runner wrote `DONE` after failures. Applied: success is decided by the external verifier `verify-1292-cm.py` (exits, counts, `OK`, skip lines, exactly 67 SQL test lines, cleanup, leftovers) plus a separate `docker ps -a` check; `DONE` is not a verdict.
* C2 High, cleanup could target another container: Applied: trap installed only after a container id is captured; cleanup verifies label and exact name before removing that id; name-collision pre-check; failed verification removes nothing and is reported.
* C3 High, redaction after the fact: Applied: `run-redacted.py` redacts while writing stdout and stderr (tested with a secret spanning a chunk boundary: zero occurrences, markers present); other captured output is piped through the same filter; no post-hoc scan is relied on.
* C4 High, deadlines did not include grace or cleanup: Applied: per-process total 600 s including kill grace (TERM 570, KILL by 595), campaign budget 1140 s, outer `timeout -k 10 1190`, cleanup inside the reserved 60 s and independently verified.
* C5 High, local-only admission not enforced: Applied: pre-checks for no `DOCKER_HOST`, default context, pinned local image id, `--pull=never`.
* C6 Medium, commit order versus pinned HEAD: Applied: the runner requires `src` tree identity with the pinned base and only `.copilot-tracking/` differences; execution HEAD and the pinned base are both recorded.
* C7 Medium, overclaim of SQL coverage: Applied: wording distinguishes 67 SQL Server tests (31, 34, 2) from 81 SQLite, in-memory, fake-driver and guard tests.

## Rejected advice

* None. No advice conflicted with a confirmed owner decision.
