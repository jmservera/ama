---
title: Issue 107 status record research
ms.date: 2026-11-04
---

## Scope

Disposition: executed (read-only). Planning Readiness: Ready for a docs-only record.

## Merged delivery (not redone)

* PR 287 (release admission), 293, 301 (dispatch worker), 863 (model-call bounds, with tests), 915 (per-period forecast), 913 (no controlled-domain writes).
* Delivered criteria on the issue: all five base criteria; RAI 2, 4, 6, 7, 9; Tokenomics 1 and 3.
* Open PR 1095 advances Tokenomics 2 (per-assistant usage attribution); not on main, so not counted here.

## Code check of unmet items

* RAI 3: `ai.py` raises `ModelMismatch` when the returned model differs from the bound model, and `test_unexpected_serving_model_quarantines_and_suspends_release` in `src/api/tests/test_assistant_release.py` proves quarantine and suspension. What remains is authoritative provider attestation of the serving version, which needs the live Azure deployment.
* RAI 5: `test_revocation_on_independent_connection_blocks_dispatch_and_reliance` and restart tests exist for the local store. Azure SQL independent-worker race evidence needs the Azure environment.
* RAI 1: approvers and residual-risk decision are human and legal (OQ-017); fixtures are constructed only.
* RAI 8: delivered-build evidence under CON-009 and AC-057 needs real AI, actual SQL and Azure.
* Tokenomics 2: attribution is open in PR 1095; historical and resident joins remain gaps.

## Conclusion

No offline code slice remains that is not already delivered or in PR 1095. Only human, Azure or legal steps remain, so this slice is a docs-only record.
