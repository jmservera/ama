# Research: IoT Hub Bicep module (issue 140)

Disposition: executed. Planning Readiness: Ready.

* Sources: issue 140, ADR 0003 decision 6 and open items, infra/main.bicep, modules/storage.bicep, keyvault.bicep, privateEndpoint.bicep, network.bicep, mvp-validation.yml.
* Existing pattern: modules take workspaceId, peSubnetId, zoneIds and `allowPublicNetworkAccess`; roles are assigned to the API user-assigned identity; the only budget is a resource-group-level one in main.bicep.
* ADR 0003: devices need keys or X.509 (Entra unsupported for device APIs); API consumer uses a managed identity; no connection string or key in source or logs; DeviceTelemetry and device ids stay out of diagnostics.
* Owner decisions: uksouth, Azure only, owner Juan Manuel Servera for device credentials, retention policies unlocked.
* Unverifiable here: current IoT Hub pricing, live what-if (no resource group access). Recorded as open items.
