using './main.bicep'

// NON-DEPLOYABLE EXAMPLE. Copy to a private, untracked file and replace every
// placeholder before use. Never pass this file to az deployment.
// PILOT: production profile with no relaxations.
// PLACEHOLDER: pilot region and subscription ownership remain open owner decisions.
param workload = 'forward'
param environmentName = 'pilot'
param location = '' // PLACEHOLDER: owner-selected pilot region
param sqlLocation = '' // PLACEHOLDER: owner-selected SQL region
param regionCheckReference = '' // PLACEHOLDER: dated capability-check reference after region decision
param quotaCheckReference = '' // PLACEHOLDER: dated quota-check reference after subscription decision
param alertEmail = 'platform-alerts@example.invalid' // PLACEHOLDER
param sqlAdminGroupName = 'sg-zava-forward-sql-admins' // PLACEHOLDER
param sqlAdminGroupObjectId = '00000000-0000-0000-0000-000000000000' // PLACEHOLDER
param entraClientId = '' // PLACEHOLDER: set after app registration
param zoneRedundant = false // PLACEHOLDER: owner decides after selected-region service support checks
param enableLocks = true
param deploymentProfile = 'production'
param allowPublicNetworkAccess = false
param keyVaultPurgeProtection = true
param registryQuarantineEnabled = true
