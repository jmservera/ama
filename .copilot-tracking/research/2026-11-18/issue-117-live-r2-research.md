---
title: Issue 117 live audit r2 research
description: Second live audit of #117 acceptance criteria on the synthetic demo
ms.date: 2026-11-18
---

Research disposition: executed (builds on the earlier note
`docs/reference/research/issue-117-live-scan-evidence-2026-11-18.md`; that evidence is reused, then re-run).
Planning Readiness: Ready.

## Scope

* Issue #117, one unticked criterion: "Uploads are scanned before availability". The ticked retention and legal hold criterion is spot-checked only.
* Synthetic demo, desktop only; live Azure authorised (rg ama, cap USD 700, no drills, no Key Vault rotation, no production changes).
* Apps: ca-cutover-test-demo-api, ca-resident-demo. Production-only items (real malware engine licence, approved retention periods, immutability lock) are separated.

## Questions

1. Does source order guarantee scan before availability?
2. Does the live demo refuse unsafe uploads and keep them out of the record?
3. What is the live scanner and storage protection state now?
4. Can a clean upload be shown available and then removed without a production change?

## Findings

Recorded in `docs/reference/research/issue-117-live-r2-audit-2026-11-18.md` as evidence is gathered.

Summary: source order proven; live refusal proven again; Defender malware scanning is enabled on the demo account
(correcting the earlier `false`), but the app scanner is local; real-engine path unproven; throwaway test blocked by
permissions and deleted. Planning Readiness: Ready.
