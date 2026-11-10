---
title: Details for issue-136-binding-c3r1-doc-1110
description: Exact wording change for infra/README.md
ms.date: 2026-11-10
---

## Phase 1 edit

In the Accounting bullet of the public simulation lane section, replace the final sentence

`A seal minted before a restart cannot be verified after it.`

with

`Losing or replacing the simulation store or key (replica replacement or scale to zero) invalidates prior seals; a restart that retains the valid pair does not itself revoke them, and expiry and single-use checks still apply.`

The Accounting bullet keeps the preceding sentences unchanged. Line wrapping follows the surrounding 100-column text.

## Evidence

* `simulation_lane.py` `Lane.verify`: key, store id, digest, expiry and persisted single-use nonce.
* `test_public_simulation_startup.py`: second valid start retains `store_id`. No new cross-restart seal test exists.

## Validation

`git diff`, `git diff --check`, rendered-wording read, hash comparison of `src/`, `infra/tests`, `infra/modules`, `infra/main.bicep` against the frozen tree.
