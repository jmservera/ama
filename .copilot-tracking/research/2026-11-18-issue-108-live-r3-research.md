---
title: Issue 108 live r3 research (opening)
ms.date: 2026-11-18
---

Task: re-verify the unticked acceptance criteria of #108 on the live synthetic demo. Refs #108.
Prior evidence: docs/reference/research/issue-108-harness-audit-live-r2-2026-11-18.md, issue-108-live-demo-evidence-2026-11-18.md, ai-heldout-batch-432-live-2026-11-18.md.
Open criteria: model/version/quota in region; held-out freeze; humans block seeded errors; effort/cost comparison; hashes/denominators; call authorisation; real AI/SQL/Azure proof; one-lever routing/caching.
Disposition: executed (new quota routes, live harness re-run, demo route check). Planning Readiness: Ready.

## Findings

* Harness: 116 tests OK (agents). Azure CLI: both deployments Succeeded, names/versions/SKU/capacity/rate limits recorded. Quota headroom routes: cognitiveservices usages empty in both regions; `az quota` and Microsoft.Quota fail with MissingRegistrationForResourceProvider (registering a provider is a subscription change, not done).
* Live app: ca-cutover-test-demo-api revision 0000032 Running, health 200. Signed-in Playwright: /api/ai/report 200 (11 scenarios passed; 16 calls, 1 unknown liability, coverage incomplete); three manager routes 403 for the Programme Manager demo account.
* Human block of seeded errors, effort/cost comparison, independent labels, attestation: need people or a validated price; not provable for the demo beyond prior notes.
* Evidence: docs/reference/research/issue-108-live-r3-2026-11-18/.
