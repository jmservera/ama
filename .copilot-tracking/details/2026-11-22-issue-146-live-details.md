# Issue 146 details (2026-11-22)

Phase 1 sqlDtu: scope is the retrofit database resource id as in `sqlCpu`; dependsOn sql; Sev3; PT5M/PT15M.
Phase 2 receiver: scopes the job in the same resource group; dimension `state` Include `Failed`; Sev2; enabled true when action group given.
Phase 3 runbook: follow the existing entry layout (Anchor, rule, proposed owner, triage, response, recovery).
Phase 4 tests: reuse `_resource`, `_description`, `_anchors` helpers.
