---
title: Issue 145 live review (2026-11-24)
description: Single post-implementation review for the release-change register.
ms.date: 2026-11-24
---

Refs #145. Review executed once on the final diff (recovery.py, assistants.py, tests, docs). Outcome: conformant with routed follow-ups; no material finding open.

## Checks

* Order: the register entry is written before the SQL change; a failed write raises and changes nothing (test `test_unwritable_release_register_blocks_the_change`).
* Content: entries hold release id, status and time only; no reason text (asserted in the reapply test).
* Idempotence and precedence: a second reapply changes nothing; revoked outranks suspended with one change per release.
* Authority: reapply uses `system=True` and only tightens status; it never activates or approves anything.
* Fail-closed residual: if the surrounding SQL transaction rolls back after an entry is written, a later restore reapply makes that release stricter than the live row. Accepted; a new release can be recorded by a named human.
* Static: ruff clean; mypy shows only three pre-existing environment errors outside the diff.

## Routed follow-ups (not done in this task)

* Spent allowance has no outside-database record (R3 remainder); needs an owner-approved design.
* Wire `reapply_release_changes` and `reapply_deletions` into an automated restore step once one exists; the runbook calls them by hand.
* Run a live restore drill only if the owner authorises drills; R1 blob state and R5 independent witness stay open.
* Complete validation tier: coordinator full gate, hosted CI and independent exact-head review are still required.
