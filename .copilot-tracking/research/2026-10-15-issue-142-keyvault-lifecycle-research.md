# Research: Key Vault secret lifecycle (#142)

* Vault (infra/modules/keyvault.bicep) already sends allLogs to Log Analytics; no expiry alert, inventory, rotation or review existed.
* Secrets used: entra-client-secret and entra-token-store-sas (modules/containerapps.bicep).
* Microsoft Learn Key Vault monitoring: SecretNearExpiryEventGridNotification and SecretExpiredEventGridNotification are logged in AuditEvent regardless of Event Grid subscription, so a Log Analytics alert is viable.
* Versionless references refresh within 30 minutes (infra/README.md).
* Planning Readiness: Ready. Owner names, live rotation and deployed alert evaluation need the owner/Azure.
