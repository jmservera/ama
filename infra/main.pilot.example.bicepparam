using './main.bicep'

// NON-DEPLOYABLE EXAMPLE. Copy to a private, untracked file and replace every
// placeholder before use. Never pass this file to az deployment.
// PILOT: production profile with no relaxations. Region uksouth (owner decision 2026-10-15).
param workload = 'forward'
param environmentName = 'pilot'
param location = 'uksouth'
param sqlLocation = 'uksouth'
param alertEmail = 'platform-alerts@example.invalid' // PLACEHOLDER
param sqlAdminGroupName = 'sg-zava-forward-sql-admins' // PLACEHOLDER
param sqlAdminGroupObjectId = '00000000-0000-0000-0000-000000000000' // PLACEHOLDER
param entraClientId = '' // PLACEHOLDER: set after app registration
param zoneRedundant = false // PLACEHOLDER: decide after checking uksouth zone support
param enableLocks = true
param deploymentProfile = 'production'
