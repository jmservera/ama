---
title: Issue 2116 witnessed suspension drill criterion, demo classification
description: Classifies the single remaining criterion of #2116 against the 2026-11-18 owner demo rules (Refs #2116)
ms.date: 2026-11-23
ms.topic: reference
---

## Scope

Issue #2116 carries one unticked criterion, split from #122: "A witnessed
authorized drill exercises suspension, owned communication responsibility and
restart. Constructed templates do not send live notices or contact residents
automatically."

## Evidence gathered

* Protocol and blank record: `docs/reference/method/operator-suspension-drill-protocol.md`
  states that no drill has been run, no restart authority is appointed, and
  that an agent must not complete the record.
* Mechanism: `src/api/tests/test_operator_suspension.py` run on 2026-11-23 in this
  worktree: `Ran 20 tests ... OK` (54 s). These are constructed-fixture tests
  and the protocol says they do not satisfy the human parts.
* Sibling criteria of #122 (persist suspension, epoch recheck, race and restart
  tests, quarantine, restart gating, history, manual fallback) are already ticked.

## Classification

| Criterion part | Demo status | Reason |
| --- | --- | --- |
| Suspension mechanism, restart gating | Proven by constructed tests only | Mechanism, not a drill |
| Witnessed authorized drill | Not provable for the demo; owner-gated | Owner decision 2026-11-18 allows no drills; needs a named restart authority and a human witness, which an agent cannot supply |
| Owned communication responsibility | Owner-gated | Requires a named human communication owner |
| Templates send no live notices | Not exercised | No drill; constructed templates only |

No code gap that needs no owner approval was found, so no `src` change is made
and the tier is FOCUSED. No Azure resources were created or changed.

## Decision

Criterion stays unticked and owner-gated. Follow-up: when the owner appoints a
restart authority and witness, run the protocol and complete its record.
