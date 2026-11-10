---
title: Issue 1360 served-transfer outcome diagnostic plan critique
ms.date: 2026-11-10
task_id: 1360-outcome-diagnostic-1110
---

## Execution and verdict

Critique executed once, by the authoring agent (no nested agent was permitted), against the final candidate plan and details written 2026-11-10. This is a self-critique and is not independent review. Verdict: approve with direct applications. No finding conflicts with a confirmed decision and none needs a user decision.

## Findings and direct dispositions

| # | Finding | Disposition |
| --- | --- | --- |
| 1 | An injection keyed only on "the call came from `save`" could fire on a `_sync` that precedes the commit if `save` ever called it earlier. | Applied: the hook also requires the separate read-only connection to show the new document, audit entry and a larger `meta seq` before it raises, and writes that proof first. The proof file is the evidence, not the hook's intent. |
| 2 | The independent writer must not be audit-only because audit-only commits do not change `meta seq`, so the target would take the cheap path and never call `_sync`. | Applied: the independent writer is a real `save` of `form_schemas`; the seq before and after is recorded; Approach 2 (seed merge) is the single fallback. |
| 3 | A passing reproduction would only prove the message contract, because the I/O failure is injected, not naturally caused. | Applied: the handoff and review must state this limit and must not claim a production incident, data loss or Critical/High risk. |
| 4 | Running the existing tests proves the known branches only if they run unchanged against the same head. | Applied: run `tests.test_import_exceptions` unchanged after the diagnostic and compare with the baseline; no test file is edited. |
| 5 | A negative control with no injection and a control where a conflict aborts before commit are needed to show the hook is not firing spuriously. | Applied: N1 and N2 are in the details. |
| 6 | Witness events are local and self-asserted; they must not be presented as attestation. | Applied: the handoff states the witness limits as reported by the helper. |
| 7 | Cleanup could delete evidence. | Applied: cleanup removes only the owned env under `/tmp/zf-1360-1110` after logs are copied; the evidence folder stays. |

## Not applied

None. No plan scope change, no new approach beyond the two already bounded, and no user decision required.

## Residual risk

The independent `form_schemas` save may be rejected by validation. That is handled by Approach 2 and is not a reason to widen scope. If both approaches fail for the writer reason, the result is a precise unreproduced hypothesis.
