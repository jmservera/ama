---
title: Ranking archive ancestor durability 1258 FULL continuation plan
description: Plan for freezing the clean head and running the final FULL gate for issue 1258
ms.date: 2026-11-08
---

Tier FULL. Base `f548b65f4aa31eb92a2cc9cb801130e422daed7f`. Details are inline.

* [ ] F1 Commit these continuation records (this is the last commit; none after the receipt). Freeze an ignored-inclusive clean head.
* [ ] F2 Recheck heavy ownership, df, RAM, CPU; refuse an existing output path.
* [ ] F3 Run `python3 tools/rpi-checks.py --all --jobs 2 --lock-timeout 0 --base f548b65f4aa31eb92a2cc9cb801130e422daed7f --out /home/azureuser/.local/share/ama/gates/g1258-full-r1 < /dev/null`. Record requested and actual jobs and shards. A failure is retained immutably; any retry uses a new output path and the documented resume rules.
* [ ] F4 Fetch main and run `--verify-receipt <receipt> --base <current origin/main>`; record hash and result.
* [ ] F5 Report. No push, PR, tick, close or cleanup.

Plan 4.2 of the original plan is satisfied by F3/F4 only if they pass. A defect found by the gate is a real finding and returns scoped evidence before any production change.

## Critique dispositions (see the FULL critique file)

* PC-001 applied: the coordinator path is 77 bytes and exceeds the 58-byte browser limit (`tools/rpi-checks.py:190-203`); the new external path `/home/azureuser/.local/share/ama/gates/g1258-full-r1` (52 bytes) replaces it. Reported as a deviation.
* PC-002 applied: an admission failure may leave no receipt; retry uses a new path (`-r2`), never reuse.
* PC-003 applied: fetch immediately before F3; if main moved, stop and report before gating; a move after the run means FULL must be rerun.
* PC-004 applied: results are recorded externally and in the response only; no tracked or untracked repository edit after the receipt.
