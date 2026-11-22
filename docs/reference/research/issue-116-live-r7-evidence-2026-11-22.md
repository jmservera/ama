---
title: Issue 116 live round 7 evidence (2026-11-22)
description: Reruns the provider-boundary proof at head 6fd6e3f838, probes the live API read-only without credentials, and records what stays unproven
ms.date: 2026-11-22
---

Synthetic demo, desktop only. Owner decisions of 2026-11-18 apply. Issue 116 shows one unticked box: allowlists at every provider boundary. The r5 matrix ([r5 note](./issue-116-live-r5-evidence-2026-11-20.md)) classified each boundary and the [r6 note](./issue-116-live-r6-evidence-2026-11-21.md) reran it. This round reruns it at head `6fd6e3f838`, rereads the four direct-egress modules and probes the live API. No credential was read, no Azure resource was created or changed, and no source file changed.

## Method and results

Suites ran sequentially from each project directory with the worktree `src` first on `PYTHONPATH`.

| Suite | Result |
| --- | --- |
| core `test_ai_provider_payload_spy`, `test_ai_input_bounds` | 24 tests, OK |
| api `test_ai_boundary_caller_inventory`, `test_ai_call_site_inventory`, `test_resident_aoai` | 26 tests, OK |
| api `test_assistants_dispatch` (reactive assistants and proactive scans) | 4 tests, OK |
| api `test_resident_assistant_provider` | 13 tests, OK |
| agents `test_heldout_aoai`, `test_heldout_batch` | 56 tests, OK |

Source reread: `core/ai.py` calls `approved_payload` in `_request` before any transport, which covers `run`, `_chat`, `evidence` and `look_at` (images are bounded by type and 4 MiB, text by 128 KiB, and `look_at` truncates text to 6000 characters). `ai_boundary_caller_inventory` pins every `Ai.run`, `look_at`, `evidence` and `_chat` call site. `ai_call_site_inventory` pins the three other direct chat-completions modules (resident demo `aoai.py`, `assistant.py`, `heldout_aoai.py`); the resident modules send closed, bounded payloads (question 1 to 500 characters, 4096-byte request, fixed topic enum) and the held-out runner stops on `prompt-too-large` before a call.

Live read-only probe of `ca-cutover-test-demo-api` (revision `0000053`), unauthenticated: `/api/cases` 401, `/api/ai/status` 401, `/healthz` 200. This confirms the role gate rejects anonymous callers; it says nothing about payload contents.

## Per-criterion status

| Criterion | Status | Basis |
| --- | --- | --- |
| Allowlists at every provider boundary | Proven offline for each enumerated boundary; not observable live | Suites above; the payload sent to a model is invisible from the deployed apps and a billable call is not needed for the demo |
| Provider-spy tests, zero canaries | Ticked; rerun green | Payload spy suite |
| Unknown task or field and excess input fail before a call | Ticked; rerun green | Input bounds and spy suites |
| Output, citation and export permission recheck | Ticked; not rerun live | Prior rounds |
| Document AI derivative or exception | Ticked; rerun green | Payload spy suite |
| Source permissions, proposal-only writes, consent | Ticked; not rerun live | Prior rounds |
| Reuse current wrappers | Ticked | One shared `approved_payload` |

Unproven for the demo: live payload contents, a credentialed role sweep this round, independent review and hosted CI. No box is ticked by this note; the owner ticks after review. Refs #116.
