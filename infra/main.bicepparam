using './main.bicep'

// DEV: throwaway, reachable stack. Every relaxation of the production default is explicit below.
// PLACEHOLDER values (example.invalid, all-zero GUID) must be replaced before deployment. No secrets belong here.
param workload = 'forward'
param environmentName = 'dev'
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
