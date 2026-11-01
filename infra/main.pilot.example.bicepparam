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
param sqlTier = 'provisioned' // ADR 0002 decision 1: no serverless auto-pause cold starts in pilot
param sqlVCores = 2 // PLACEHOLDER: size from the pilot load result (not yet recorded)
param sqlBackupStorageRedundancy = '' // PLACEHOLDER: owner decision; empty follows zoneRedundant
param sqlBackupRetentionDays = 14 // PLACEHOLDER: PITR window only; legal retention is #121, undecided
param apiMinReplicas = 0
param enableLocks = true
param deploymentProfile = 'production'
param allowPublicNetworkAccess = false
param keyVaultPurgeProtection = true
param registryQuarantineEnabled = true
