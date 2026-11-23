---
title: Issue 116 live round 8 evidence (2026-11-23)
description: Reruns the provider-boundary proof at head ac58e5c451, probes the live API read-only without credentials, and records what stays unproven
ms.date: 2026-11-23
---

Synthetic demo, desktop only. Owner decisions of 2026-11-18 apply. Issue 116 shows one unticked box: allowlists at every provider boundary. The [r7 note](./issue-116-live-r7-evidence-2026-11-22.md) holds the boundary matrix and its source reread; no `src/` file changed since, so this round reruns the suites at head `ac58e5c451` and probes the live API. No credential was read, no Azure resource was created or changed, and no source file changed.

## Method and results

Suites ran sequentially from each project directory with the worktree `src` first on `PYTHONPATH`.

| Suite | Result |
| --- | --- |
| core `test_ai_provider_payload_spy`, `test_ai_input_bounds` | 24 tests, OK |
| api `test_ai_boundary_caller_inventory`, `test_ai_call_site_inventory`, `test_resident_aoai`, `test_assistants_dispatch`, `test_resident_assistant_provider` | 45 tests, OK |
| agents `test_heldout_aoai`, `test_heldout_batch` | 56 tests, OK |

Live read-only probe of `ca-cutover-test-demo-api` (active revision `ca-cutover-test-demo-api--0000055`), unauthenticated: `/api/cases` 401, `/api/ai/status` 401, `/healthz` 200. This confirms the role gate rejects anonymous callers; it says nothing about payload contents.

## Per-criterion status

| Criterion | Status | Basis |
| --- | --- | --- |
| Allowlists at every provider boundary | Proven offline for each enumerated boundary; not observable live | Suites above and the r7 matrix; the payload sent to a model is invisible from the deployed apps, and a billable call is not needed for the demo |
| Provider-spy tests, zero canaries | Ticked; rerun green | Payload spy suite |
| Unknown task or field and excess input fail before a call | Ticked; rerun green | Input bounds and spy suites |
| Output, citation and export permission recheck | Ticked; not rerun live | Prior rounds |
| Document AI derivative or exception | Ticked; rerun green | Payload spy suite |
| Source permissions, proposal-only writes, consent | Ticked; not rerun live | Prior rounds |
| Reuse current wrappers | Ticked | One shared `approved_payload` |

Unproven for the demo: live payload contents, a credentialed role sweep this round, independent review and hosted CI. No box is ticked by this note; the owner ticks after review. Refs #116.
