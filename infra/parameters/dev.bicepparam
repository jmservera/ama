using '../main.bicep'

// NON-DEPLOYABLE EXAMPLE. Replace every PLACEHOLDER value before deployment; no secrets belong here.
// DEV: private synthetic development profile with explicit non-production relaxations.
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
param monthlyBudget = 300
param iotHubSku = 'B1'
param iotHubUnits = 1
param iotHubRetentionDays = 1
param iotHubMonthlyCost = 60
param sqlTier = 'serverless'
param sqlVCores = 2
param sqlAutoPauseDelayMinutes = 60
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
param enableLocks = false
param deploymentProfile = 'development'
param allowPublicNetworkAccess = false
param keyVaultPurgeProtection = false
param registryQuarantineEnabled = false
