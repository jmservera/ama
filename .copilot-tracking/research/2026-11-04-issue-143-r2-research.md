# Research: issue 143 remaining criteria (2026-11-04)

Research disposition: executed. Planning Readiness: Ready.

## Evidence

* Merged PRs #278 (edge module, per-service private-endpoint and DNS test, production-only guard), #352 (public src edge on existing infrastructure) and #675 (callback path and host single-source test) are on main. Issue comments record criteria 1, 2 and 4 as ticked and criteria 3 and 5 as unmet (closure audit 2026-10-31).
* Criterion 3: static guards exist for callback path, host expression, managed certificate and HTTPS-only route in `infra/modules/edge.bicep` and `infra/tests/test_edge_module.py`. What remains is the owner decision on the pilot domain and edge go/no-go, plus live Entra reconciliation.
* Criterion 5: needs a production-profile deployment with Private Link approval to the internal Container Apps environment. No deployment is authorised here.
* A further static test would sit in `infra/`, which this slice's rules exclude (new code in `src/` only), and would not move a criterion.

## Conclusion

Only human and Azure steps remain. Deliver a docs-only record PR with `Refs #143`.
