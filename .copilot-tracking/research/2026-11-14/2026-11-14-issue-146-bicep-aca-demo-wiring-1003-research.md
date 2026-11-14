# Research: Bicep Container Apps demo wiring contract (Refs #146, #165)

Date: 2026-11-14. Branch: test/demo-146-bicep-aca-demo-wiring-1003 (parent 985b19bcb, PR #1625). Research disposition: executed. Planning Readiness: Ready.

## Evidence

* infra/modules/containerapps.bicep declares api, tokenRenewal, agents, orchestrator, ledgerVerify, rankingPublish and importJob; each uses a single user-assigned identity, registry pull by that identity and AZURE_CLIENT_ID from identityClientIds (tokenRenewal from tokenMaintenance params).
* Secrets: only two Key Vault references (Entra client secret, token-store SAS) with identity identityIds.api; env uses one secretRef (AUTH_TOKEN_STORE_ROTATION). No literal keys or listKeys.
* AI env (AI_ENDPOINT, deployments, versions) only on the api, gated by enableApiAi (default false in main and module); no API key.
* Chat demo: ZF_CHAT_DEMO_ACTIVATION and ZF_DEPLOYMENT_PROFILE=demo only when demoDirectIngress and exact value approved-2026-11-03; chat governance refs require all four refs and retention days > 0.
* Telemetry: commonEnv (APPLICATIONINSIGHTS_CONNECTION_STRING from monitoring output, OTEL_SERVICE_NAMESPACE) is spread into every workload except tokenRenewal.
* IoT: live-receiver-job.bicep and live-simulator-job.bicep use existing user-assigned identities, msi SQL auth, no secrets.
* No template defect found; the gap is the absence of a single contract test. Existing tests (test_container_hosting_completeness, test_identity_rbac) do not assert these env and identity pairings.
