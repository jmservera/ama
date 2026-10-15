using './main.bicep'

// TEST: shared integration stack on the development profile (as the 2026-10-08 and 2026-10-11 test deployments).
// PLACEHOLDER values (example.invalid, all-zero GUID) must be replaced before deployment. No secrets belong here.
param workload = 'forward'
param environmentName = 'test'
param location = 'uksouth'
param sqlLocation = 'uksouth'
param alertEmail = 'platform-alerts@example.invalid' // PLACEHOLDER
param sqlAdminGroupName = 'sg-zava-forward-sql-admins' // PLACEHOLDER
param sqlAdminGroupObjectId = '00000000-0000-0000-0000-000000000000' // PLACEHOLDER
param entraClientId = '' // set after infra/scripts/create-api-app-registration.sh
param zoneRedundant = false
param enableLocks = false
// Development relaxations (production is the template default).
param deploymentProfile = 'development'
param allowPublicNetworkAccess = true
param keyVaultPurgeProtection = false
