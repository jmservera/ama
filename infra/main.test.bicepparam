using './main.bicep'

// TEST: shared integration uses the production security profile, not historical development relaxations.
// PLACEHOLDER values (example.invalid, all-zero GUID) must be replaced before deployment. No secrets belong here.
param workload = 'forward'
param environmentName = 'test'
param location = 'uksouth'
param sqlLocation = 'uksouth'
param regionCheckReference = '' // PLACEHOLDER: dated capability-check reference
param quotaCheckReference = '' // PLACEHOLDER: dated quota-check reference for the selected configuration
param alertEmail = 'platform-alerts@example.invalid' // PLACEHOLDER
param sqlAdminGroupName = 'sg-zava-forward-sql-admins' // PLACEHOLDER
param sqlAdminGroupObjectId = '00000000-0000-0000-0000-000000000000' // PLACEHOLDER
param entraClientId = '' // PLACEHOLDER: set after infra/scripts/create-api-app-registration.sh
param zoneRedundant = false
param sqlTier = 'serverless' // dev: auto-pause permitted
param apiMinReplicas = 0
param enableLocks = false
param deploymentProfile = 'production'
param allowPublicNetworkAccess = false
param keyVaultPurgeProtection = true
param registryQuarantineEnabled = true
