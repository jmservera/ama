---
title: "Issue 1297 gate bytecode hygiene critique"
ms.date: 2026-11-16
---

## Execution

Critique executed once, on the final candidate plan, by the RPI worker (self-critique; independent exact-head review stays with the coordinator). Verdict: proceed with amendments applied.

## Findings and dispositions

* Alternative: change the test's env to forward the bytecode variables. Rejected: fixes one test, leaves every other scrubbed child exposed, and edits SQL-adjacent core tests unnecessarily. Applied: interpreter-level policy.
* Risk: writing a .pth to every venv could change receipt file lists. Disposition applied: only the api venv keeps the out-dir `browser-bytecode-policy.pth`; venv files live outside the receipt.
* Risk: regression test must prove it fails before the fix. Applied: run it against the unfixed tool first and record the failure in the changes artifact.
* Risk: relaxing clean checks. None: `clean_identity` and snapshot logic are untouched; no skip allowance changes.
* Residual: a scrubbed child using a non-venv interpreter is out of scope.
