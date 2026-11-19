---
title: Per-user chat epic (#157) live criteria check, 2026-11-19
description: Per-criterion record for the open acceptance criteria of epic #157 and the one cut-over gate violation fixed in the knowledge-base index
author: AMA programme
ms.date: 2026-11-19
ms.topic: reference
---

## Scope and authority

Synthetic demo, desktop only. Owner decisions of 2026-11-18 apply: live Azure authorised in resource group `ama`, no drills, no Key Vault rotation, no production change; billing reconciliation, DPO and Legal approval and person-run assistive-technology testing are not needed for the demo. No credential was read or printed and nothing was created on Azure.

## Observations

| Check | Result |
| --- | --- |
| `az containerapp revision list` for `ca-cutover-test-demo-api` | `ca-cutover-test-demo-api--0000033` Healthy, Running (newer than 0000032 in the [2026-11-18 note](./issue-157-live-chat-epic-recheck-2026-11-18.md)) |
| Same for `ca-resident-demo` | `ca-resident-demo--0000014` Healthy, ScaledToZero |
| Signed-in chat endpoint probe | Not repeated; the 2026-11-18 probe (status, own-thread list, unknown-thread 404, break-glass 403 with audit chain) stands for the earlier revision and is not claimed for 0000033 |
| `python3 tools/check-legacy-references.py` at head | 1 violation: `docs/reference/README.md:1355` named retired `prototype/` without archive tag `v0.21.0` |
| `python3 -m unittest tools.test_check_legacy_references` before the fix | 1 of 8 failed (`test_repository_has_no_violations`) |

## Change made

The index row for the parity matrix now reads "removed in #202 step 1 (archive tag `v0.21.0`)". This clears the last residual of draft D2 in the [#440 triage note](./stabilization-checkpoint-triage-440-live-2026-11-18.md); the guard test passes after the edit (see the changes record). It is a documentation text change, FOCUSED tier.

## Per-criterion verdicts for #157

| Criterion | Verdict | Basis |
| --- | --- | --- |
| Complete the #440 stabilization checkpoint | Unproven | #440 still has two unticked criteria: filing triage drafts D1 to D4 with owner approval of any requirement change, pivot or deferral, and PR artifacts with independent review. Neither is possible in a local-only task. D3 (unreachable `ChatIsolation.turn`) stays open: it changes security-adjacent src and needs the FULL tier |
| If accepted, child features are accepted | Unproven | #162 needs a deployed break-glass setting change outside the authorisation; #164 needs owner approval of thresholds and task registration; #159 screen-reader testing is waived for the demo and not evidenced |
| Decision accepted; no memory as controlled-decision evidence; chat consumption bounded (ticked) | Not re-opened | ADR 0004 (2026-10-15); PR #1552; PRs #1547 and #1558 |

## Limits

* No model turn and no signed-in probe ran today, so no grounding or isolation claim is refreshed for revision 0000033.
* The fix removes a gate violation; it does not satisfy any #157 criterion.
