---
title: Issue 1292 current-main priority SQL Q1 qualification research
ms.date: 2026-11-09
task_id: 1292-current-main-sql-q1-1109
---

## Scope

Evidence-only documentation addendum. Input: same-reviewer assessment `2290470d-6e47-4164-9e5b-d2172030da16` of frozen `6c05b1e12922205286400a17c73957c9c23bb35e`: approve with comments, one Medium, plus out-of-scope limits. Base for this lane: clean `2bdd749a320d1fbf6f85871e211b37ad7fbc5a0f`. No SQL rerun, source, harness or script change, no security audit, no Source E5. Research disposition: executed over the touched records and the raw receipts only. Planning Readiness: Ready.

## Facts verified in the raw 30-member receipts (read-only)

* Q1 (Medium): `verify-1292-cm.py` prints cleanup and leftovers but its exit gate covers test outcomes (exits, totals, `OK`, skips, SQL counts) only. Cleanup was observed separately: `container-id.txt` and `container-cleanup.txt` both hold `9d18437a720c4490e7646c3d14559518eebc2d984ffd49c2786f784bda34f78a`, `leftover-databases.txt` is empty (captured output only: the script piped the query without retaining its exit status, so an empty file is not proof the query succeeded), and the executing session recorded `docker ps -a` empty afterwards (changes record, not a retained receipt file).
* Original wording to qualify, preserved unedited: critique C1 ("success is decided by the external verifier ... cleanup, leftovers") and the plan acceptance paragraph.
* Q2 (limit on critique C4, deadlines; the coordinator brief called it C3): per-process epoch intervals 311, 201 and 11 s, unittest durations 309.366, 201.206 and 10.367 s, campaign 540 s (`campaign.start` 1794248073, `campaign.end` 1794248613); all under 600 s and 1200 s. No timeout-path receipt exists; `run-redacted.py` joins output threads up to 5 s each after a kill, so a universal hard bound is not proven by this pass.
* Q3 (limit on critique C5, local-only admission; the brief called it C7; C7 itself is SQL-coverage wording and stands): `image-id.txt` records local tag image id `sha256:cf8f0ab2ebe61feec2eed2629061a07d247f791c2a8ddda74a4ac9f06a291718`. The precheck tested `DOCKER_HOST`, the context name and the local tag id; the run used the tag with `--pull=never`, not the immutable id. No retained actual daemon-endpoint inspection exists. Not claimed: immutable-runtime-image proof or endpoint authentication.
* The seven "Applied" dispositions record what was changed in the plan and scripts before execution; they are not proof of universal guarantees.

## Boundaries

The 67 SQL tests passed once, truthfully; recorded versions, tag and id stay as observed. Unknown startup cause, unproven AC3 old-behavior half, no full gate, no ticks. Source tree `86bc00e19a167e517ae2955ad88d6e2f7b4eac26` unchanged; docs only, no runtime check needed.
