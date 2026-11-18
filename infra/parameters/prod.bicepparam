using '../main.bicep'

// NON-DEPLOYABLE EXAMPLE. Copy to a private, untracked file and replace every
// PLACEHOLDER before use. Never pass this template unedited to az deployment.
// PROD PROFILE: production isolation controls aligned with pilot guard rules.
param workload = 'forward'
param environmentName = 'pilot'
param location = '' // PLACEHOLDER: owner-selected production-profile region
param sqlLocation = '' // PLACEHOLDER: owner-selected SQL region
param regionCheckReference = '' // PLACEHOLDER: dated capability-check reference after region decision
param quotaCheckReference = '' // PLACEHOLDER: dated quota-check reference after subscription decision
param alertEmail = 'platform-alerts@example.invalid' // PLACEHOLDER
param sqlAdminGroupName = 'sg-zava-forward-sql-admins' // PLACEHOLDER
param sqlAdminGroupObjectId = '00000000-0000-0000-0000-000000000000' // PLACEHOLDER
param entraClientId = '' // PLACEHOLDER: set after app registration
param zoneRedundant = false // PLACEHOLDER: owner decides after selected-region service support checks
param monthlyBudget = 300 // PLACEHOLDER: confirm billing budget after subscription decision
param iotHubSku = 'B1'
param iotHubUnits = 1
param iotHubRetentionDays = 1
param iotHubMonthlyCost = 60 // PLACEHOLDER: confirm IoT allocation within verified subscription budget
param sqlTier = 'provisioned' // ADR 0002 decision 1: dedicated provisioned tier without cold starts
param sqlVCores = 2 // PLACEHOLDER: size from recorded load result
param sqlBackupStorageRedundancy = '' // PLACEHOLDER: owner decision; empty follows zoneRedundant
param sqlBackupRetentionDays = 14 // PLACEHOLDER: PITR window only; legal retention is tracked under #121
param modelDeployments = [
  {
    name: 'standard'
    model: 'gpt-4.1-nano'
    version: '2025-04-14'
    skuName: 'GlobalStandard'
    capacity: 1
  }
]
param apiMinReplicas = 0
param enableLocks = true
param deploymentProfile = 'production'
param allowPublicNetworkAccess = false
param keyVaultPurgeProtection = true
param registryQuarantineEnabled = true
