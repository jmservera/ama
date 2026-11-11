---
title: Issue 1360 served-transfer outcome diagnostic review
ms.date: 2026-11-10
task_id: 1360-outcome-diagnostic-1110
---

## Execution and boundary

Review executed once, by the authoring agent, after the diagnostic finished. This is a self-review of diagnostic conformance only. It is not a product APPROVE, not an independent exact-head assessment, not human approval and not hosted CI. Assessed boundary: the new RPI records on branch `test/demo-transfer-outcome-diagnostic-1360-1110` over pinned main `fe59ef56a0084dd975fd7e5c342670bb8f788fb0`, plus the external evidence folder.

## Outcome

Diagnostic conformance: conformant with the plan, with the limits below. Issue 1360 outcome: the static claim is now confirmed by a native counterexample (the generic message is printed after a durable commit). No product repair is authorised and none was made.

## Checks against plan success criteria

| Criterion | Result |
| --- | --- |
| Injection only at post-commit `_sync` from `save`, commit proven first | Met. Proof files record the call order and `committed_before_injection` true for C1 and C2; N2 shows no injection when a conflict aborts before commit. |
| Real CLI exit and stderr | Met. Subprocess exit 2 and stderr "the served store refused it (...). Nothing was recorded." for OSError and ValueError. |
| Independent reopen shows retained document, audit, independent writer commit | Met (read-only sqlite3 connection and a fresh `SqlStore`). |
| Retry idempotent, no second creation | Met. Exit 0, `added=0 already_present=1`, audit count unchanged at 1. |
| Ledger and refused file unchanged | Met (sha256 equal before and after). |
| Known branches distinct | Met for conflict rollback by N2 and for the other branches by the unchanged existing tests (40 OK before and after). Committed-reload, partial and driver branches were not re-executed natively here. |
| No source change | Met. Worktree has only new RPI records; empty diff over `src docs tools .github infra` against the base. |

## Findings

| # | Severity | Finding | Routing |
| --- | --- | --- | --- |
| 1 | Medium (message contract) | Generic `OSError`/`ValueError` branch can report "Nothing was recorded" after commit. Not data loss; retry is idempotent. | Later user-selected work, needs a dated finite grant. Not made here. |
| 2 | Limit | The failure is injected, not naturally caused; no real writer was shown to cause a natural post-commit `OSError`. | Stated in the handoff. |
| 3 | Limit | The local witness log is writable and self-asserted. | Stated in the handoff. |
| 4 | Process | Critique and Review were self-executed because nested agents were not permitted. | Independent exact-head assessment remains required before any publication. |

## Not claimed

No whole issue 1360, 73 or 135 acceptance, no live, appointment, consent or production claim, no Critical or High integration claim, no waiver of independent review, human approval or hosted checks, no reset of the 135 C5 allowance.
