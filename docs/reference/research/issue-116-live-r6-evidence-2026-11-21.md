---
title: Entra roles and field-level visibility, round 6 recheck (#116)
description: Reruns the provider-boundary proof at current head, closes the unrun assistants dispatch test gap, probes the live API role gate read-only, and records what stays unproven
ms.date: 2026-11-21
---

## Scope

Synthetic demo, desktop only. Owner decisions of 2026-11-18 apply. Issue 116 shows one unticked box, allowlists at every provider boundary. Round 5 ([r5 note](./issue-116-live-r5-evidence-2026-11-20.md)) proved each enumerated boundary offline and listed one residue: `test_assistants_dispatch` could not be imported because `opentelemetry` was missing. No credential was read, no Azure resource was created or changed, and no source file changed. Head is 08fbe37ef.

## Evidence

* Pinned `opentelemetry-sdk`, `opentelemetry-api` and `opentelemetry-exporter-otlp-proto-http` 1.45.2 (the versions in `src/core/pyproject.toml`) were installed into a throwaway directory outside the repository.
* api: `test_assistants_dispatch`, `test_chat_panel`, `test_resident_aoai` and `test_ai_call_site_inventory` ran 104 tests, OK, 1 skipped (opt-in Chromium). The dispatch test, reactive and proactive assistants, now runs.
* core: `test_ai_provider_payload_spy` and `test_ai_input_bounds` ran 24 tests, OK.
* Live read-only probe of `ca-cutover-test-demo-api` without credentials: `/api/cases`, `/api/ai/assistants`, `/api/export` and `/api/audit` returned 401; `/healthz` returned 200.

## Finding

No defect. The r5 residue about the unrunnable dispatch test is closed; the boundary matrix in the r5 note stands.

## Acceptance criteria

| Criterion | Status | Basis |
| --- | --- | --- |
| Allowlists and size limits at every provider boundary | Proven offline for every enumerated boundary; not observable live | r5 matrix; the suites above pass at head. The payload sent to a model is not visible from the deployed apps, and a billable call is not needed for the demo |
| Ticked boxes (role-by-endpoint, contractor view, redaction decision, reason roles) | Ticked before this round | Unauthenticated live gate re-probed (401); credentialed evidence stays in rounds 3 to 5 |

Unproven: live payload contents, a repeated credentialed second-role run, independent review and hosted CI. No box is ticked by this note; the owner ticks after review.
