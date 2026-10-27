using './main.bicep'

// DEV: private synthetic development. Every production-default relaxation is explicit.
// PLACEHOLDER values (example.invalid, all-zero GUID) must be replaced before deployment. No secrets belong here.
param workload = 'forward'
param environmentName = 'dev'
param location = 'uksouth'
param sqlLocation = 'uksouth'
param regionCheckReference = '' // PLACEHOLDER: dated capability-check reference; historical success is not approval
param quotaCheckReference = '' // PLACEHOLDER: dated quota-check reference for the selected configuration
param alertEmail = 'platform-alerts@example.invalid' // PLACEHOLDER
param sqlAdminGroupName = 'sg-zava-forward-sql-admins' // PLACEHOLDER
param sqlAdminGroupObjectId = '00000000-0000-0000-0000-000000000000' // PLACEHOLDER
param entraClientId = '' // PLACEHOLDER: set after infra/scripts/create-api-app-registration.sh
param zoneRedundant = false
param apiMinReplicas = 0
param enableLocks = false
// Development relaxations (production is the template default).
param deploymentProfile = 'development'
param allowPublicNetworkAccess = false // SQL is private even if other services opt in
param keyVaultPurgeProtection = false
param registryQuarantineEnabled = false
