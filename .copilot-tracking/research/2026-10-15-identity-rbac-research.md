---
title: Identity and RBAC as code research (#141)
---

Research disposition: executed. Planning Readiness: Ready.

* Four identities (api, agents, orchestrator, import) plus a token-maintenance identity; roles assigned in main.bicep and modules (storage, keyvault, registry, foundry, iothub, authTokenStore). All built-in data-plane roles, none broad.
* No chat store resource exists; ADR 0004 accepted by the owner 2026-10-15.
* Entra registration is created by infra/scripts/create-api-app-registration.sh; roles match mvp DEFAULT_ROLE_MAP.
* Owner decisions: uksouth, Azure only, existing sign-in kept, Juan Manuel Servera owns tenant steps. ADR 0005 permits synthetic fixtures only; no data touched.
* Open: B2B guest decision (#116), live role comparison.
