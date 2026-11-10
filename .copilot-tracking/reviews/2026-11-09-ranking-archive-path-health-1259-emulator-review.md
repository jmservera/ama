---
title: Issue 1259 local Azurite emulator validation review
description: Original single author Review of the local Azurite validation of the frozen Blob ranking archive adapter
ms.date: 2026-11-09
---

## Execution and outcome

Review executed once, 2026-11-09, by the authoring agent (rpi-agent, Sonnet 5.5) after execution finished. It is an author review, not independent, not repeated for this task. Boundary assessed: the [changes record](../changes/2026-11-09-ranking-archive-path-health-1259-emulator-changes.md), the external logs `00` to `20` under `/home/azureuser/.local/share/ama/gates/g1259-emulator-1109.P6T1sb/logs/`, and the worktree state.

Outcome: Complete for the bounded local validation; Residual work for issue 1259 (not conformant to its full acceptance criteria). The check was admitted and every planned adapter and control observation was performed; nothing was blocked. Material gaps are routed, not closed.

## Assessment against the plan

| Plan item | Result |
| --- | --- |
| Source byte-identical to `7fc680d0` | Met: 285 of 285 `src/core` files match git blobs before and after; no source, test, tool or infra diff |
| Missing-tool check before install, scratch-only install | Met (log 00, 04) |
| Owned ports, key, CA; no real Azure, account, data, model, firewall change | Met |
| No production TLS/auth weakening, no adapter edit, no host-rewriting transport | Met: default urllib transport, https verified through the owned CA in `SSL_CERT_FILE`, SAS auth, production-style host |
| Admission via existing configuration | Admitted; no incompatibility found. Unproven alternative for path-style Azurite URLs: the adapter's `base` drops the URL path, so only host-style accounts work (recorded as a fact, not a defect) |
| Conditional create, idempotence, retained bytes, list, get, valid-empty | Performed on the actual adapter and runner |
| Path-free failure and manual controls | Performed: 403 (no list permission, tampered signature), 404 (absent container), refused socket; unknown state, `archive_unreadable`, no write, no leak |
| Hold service only for the check; stop its PID | Met: PID 2972196 stopped, no listener, nothing else pruned |
| Evidence-only candidate | Met: only RPI records committed; logs, keys, certificates, SAS stay external |

## Findings

| Id | Finding | Routing |
| --- | --- | --- |
| RV-1 | The emulator cannot produce malformed XML, endless pagination or 5xx; those paths and multi-page listing are covered only by the parent mocked-REST tests. | Residual: stays mocked evidence; no claim made. |
| RV-2 | The first-`NextMarker` parsing choice (PC-1 of the parent c5 task) was not probed; Azurite does not emit a duplicate marker. | Residual: owner choice unchanged. |
| RV-3 | Records published with the test-local signed registry fail verification under the shipped unsigned registry, as designed; CLI schedule/verify on a populated container therefore show registry problems that are not adapter defects. | Explained in the changes record; no action. |
| RV-4 | Managed-identity (bearer) path was not exercised. | Residual: needs a real or faithful identity setup; not claimed. |
| RV-5 | A setup SDK/emulator API-version mismatch occurred (log 08) and was fixed by pinning the setup SDK; the adapter's API version 2021-08-06 was accepted. | Recorded as deviation; no impact on adapter evidence. |
| RV-6 | Azurite is an emulator: real Azure behaviours (WORM, RBAC, network rules, throttling, SAS clock skew, real status and error codes for conditional create) are unproven. | Residual: needs an approved real-account validation, owned by the coordinator and owner. |
| RV-7 | Correction-budget wording conflicts between the brief (1 of 5 remains 1) and the parent c5 handoff (1 of 5 used, four remaining). | Routed to the coordinator; this task consumed no cycle. |

No finding blocks the local candidate. No source correction is proposed, because none of the observed behaviour contradicts the AC the emulator can test.

## Acceptance criteria support (does not tick or rewrite any criterion)

Supports, as local emulator evidence only: failing listing never reported as a healthy empty archive; unknown state and refusal shape (`archive_unreadable`, zero write); path-free diagnostics; valid first-run (empty container) distinguished from unreadable; create-only idempotence and retained bytes. Does not support: real-account behaviour, WORM, the final criterion (full receipt, independent exact-head assessment, hosted checks), or human approval. Refs #1259 only.

## Follow-ups (ranked, current)

1. Owner choice on PC-1 (first `NextMarker`) and, if desired, one more authorized parent cycle. Ease: low effort, quality leverage high; blocked on a decision.
2. Real Azure account and WORM validation under an approved, owner-controlled environment (not authorised here).
3. Independent exact-head review and hosted CI of the child stack when the coordinator authorises publication.
