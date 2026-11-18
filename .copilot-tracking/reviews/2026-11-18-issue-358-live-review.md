---
title: Issue 358 live review
ms.date: 2026-11-18
---

One review pass. Outcome: Conformant for the scoped evidence claims; residual work routed.

* No source diff; expiry mutation fails 8 tests; round-trip PASS after a retained early-readback FAIL.
* No secret values appear in evidence (outputs print names, booleans, vault URL only; the KV URL is a synthetic demo vault).
* Residual: full `setup-entra.py` run on the deployed app (Graph authority, #349/#360) and #352 re-verification remain unproven; issue 358 stays open.
* Witness refusals for implement-start/done (changes pointer missing from state) are retained and were corrected by updating the state.
