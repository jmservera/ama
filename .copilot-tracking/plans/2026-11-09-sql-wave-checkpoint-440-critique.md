---
title: SQL feature-recovery wave checkpoint 440 plan critique
ms.date: 2026-11-09
---

## Verdict

Revise. One critique pass by an independent read-only reviewer (`rubber-duck`), executed once on the final candidate plan; no second critique runs. Findings were returned inline and recorded here. No finding conflicts with a confirmed decision and none needed a user decision. No SQL admission was found necessary.

## Findings and dispositions

* PC-001 Blocking. The import-origin check as written could not pass: the `zava_forward` packages are namespace packages (`__file__` is `None`) and the SQL driver lives in the venv. Disposition: applied. Details phase 1 now checks namespace `__path__` and concrete module origins separately and records the driver origin as venv.
* PC-002 Blocking. Raw retention of historical failures was asserted without a verified location. Disposition: applied. The raw artifacts were located and read: coordinator session files `e1-sql-admission2-132322-2818937/`, `e2-sql-admission-134433-2845787/`, `e2-sql-admission2-140248-2867281/`; exits, counts, sha256 prefixes and import provenance are in the research. They remain outside the repository and the record says so. The imported `sqlstore.py` and `mssqlstore.py` sha256 equal today's `8d6f029ca` blobs.
* PC-003 Non-blocking. The nineteenth rollup entry is the successful `rubric/score` commit status. Verified with `gh api repos/jmservera/ama/commits/<head>/status`. Applied in research and plan FR1.
* PC-004 Non-blocking. Heading carried `Refs #440 #1292 #81`; the brief says `Refs #440` only. Applied: heading uses `Refs #440`, other issue numbers are traceability text.
