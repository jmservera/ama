# Research: issue 143 private networking and public edge (2026-11-01)

Research disposition: executed. Planning Readiness: Ready.

## Question

Which acceptance criteria of #143 remain unmet on `origin/main` (efebfc6d)?

## Evidence

* Criteria 1, 2 and 4 are checked in the issue and delivered by merged work (#278, #352): `infra/modules/edge.bicep` (Front Door Premium, WAF, Private Link origin, optional managed-certificate custom domain), `infra/tests/test_edge_module.py` (PE/DNS coverage per service, edge production-only guard).
* Criterion 3: `edge.bicep` outputs `entraRedirectUri` from the custom domain or default host; `infra/entra/app-registration.json` holds `callbackPath`; `setup-entra.py` registers `origin + callbackPath` only for approved domains. The only test (`test_entra_callback_follows_edge_host`) checks substrings, so the three definitions of the callback path can drift apart without a failing test.
* Criterion 5: requires a production-profile deployment. No deployment is authorised in this focused tier; CI/what-if is the evidence.

## Conclusion

Smallest in-scope change: a static consistency test tying the callback path, the host used in the edge output and the Entra manifest together. Criterion 5 stays unmet, so the PR uses `Refs`.
