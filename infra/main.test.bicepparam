using './main.bicep'

// TEST: shared integration uses the production security profile, not historical development relaxations.
// PLACEHOLDER values (example.invalid, all-zero GUID) must be replaced before deployment. No secrets belong here.
param workload = 'forward'
param environmentName = 'test'
param location = 'uksouth'
param sqlLocation = 'uksouth'
param aiModelLocation = 'uksouth'
param aiModelFallbackLocation = '' // PLACEHOLDER: optional fallback; set only with a dated region and quota check
param modelCapacityBudget = 30 // approved model capacity units; must cover modelDeployments and match the quota record
param regionCheckReference = '' // PLACEHOLDER: dated capability-check reference
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
param sqlTier = 'serverless' // dev: auto-pause permitted
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
param deploymentProfile = 'production'
param allowPublicNetworkAccess = false
param keyVaultPurgeProtection = true
param registryQuarantineEnabled = true
// Synthetic-data demo only; owner decision 2026-11-01. Not a production approval.
param chatDpiaRef = 'docs/reference/research/chat-memory-dpia.md'
param chatLawfulBasisRef = 'docs/reference/research/chat-demo-storage-approval-2026-11-01.md#lawful-basis'
param chatNoticeRef = 'docs/reference/research/chat-demo-storage-approval-2026-11-01.md#notice'
param chatRetentionRef = 'docs/reference/research/chat-demo-storage-approval-2026-11-01.md#retention'
param chatRetentionDays = 30
// Ranking archive Blob container (Refs #136, #1258): source definition, not provisioning or a deploy approval.
// Set enableRankingArchiveBlob = true in the private copy to wire the demo. 0 days creates no immutability
// policy; the retention duration and its approval are a manual prerequisite, so no immutable release is claimed.
param enableRankingArchiveBlob = false
param rankingArchiveImmutabilityDays = 0
// Synthetic demo only; owner decision 2026-11-18 (demo needs no further activation approval). Not a production approval.
param enableCandidateMonitoringAlerts = true
param monitoringApprovalReference = 'docs/reference/research/issue-146-live9-monitoring-2026-11-26.md'
param enablePoisonQueueAlertCandidate = true
param enableAiLimitAlertCandidate = true
