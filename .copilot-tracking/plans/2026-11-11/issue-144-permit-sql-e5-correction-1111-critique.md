---
title: Issue 144 permit SQL E5 correction authored critique
description: One authored critique of the final E5 plan candidate
ms.date: 2026-11-11
task_id: issue-144-permit-sql-e5-correction-1111
---

## Label

AUTHORED, not independent; no gate cleared. One critique only.

## Findings and dispositions

* Chaining `InvalidWitness from primary` changes the exception type when cleanup fails: intended, so a cleanup problem can never read as an accepted expected failure. The primary also gets a note. Applied.
* A fake-driven harness probe cannot prove SQL behaviour: stated as HARNESS-ONLY. Applied.
* The manifest proves launcher intent, not a mount boundary: stated limit; the check is exact-path, ownership and permission binding. Applied.
* `_markers` is a private-named existing reader: accepted, no new API.

## Verdict

Proceed to Implement within E5. Not a clearance.
