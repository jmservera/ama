# Plan: IoT Hub Bicep module (issue 140)

1. Add modules/iothub.bicep: B1 hub, disableLocalAuth, built-in endpoint retention, consumer group, Event Hubs Data Receiver for API identity, diagnostics, private endpoint, hub-scoped budget.
2. Add privatelink DNS zones to network.bicep; wire module and parameters in main.bicep.
3. Add infra/tests/test_iothub_module.py static guards.
4. Record decisions in infra/README.md, ADR 0003 open items, docs/reference/log.md.
5. Validate: az bicep build/lint, infra and mvp unit tests.

Critique (single pass, self): scope is minimal; DPS deliberately deferred; cost is an estimate, not invented fact. No conflicts with owner decisions.
