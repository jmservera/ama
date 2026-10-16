targetScope = 'resourceGroup'

@description('Short workload prefix, lower case, 3 to 10 characters.')
@minLength(3)
@maxLength(10)
param workload string = 'forward'
@description('Environment name; drives resource naming and the environment tag. pilot requires the production profile.')
@allowed(['dev', 'test', 'pilot'])
param environmentName string = 'dev'
param location string = resourceGroup().location
@description('Reference to a dated, reviewed region/service/zone capability check for the selected locations. Empty blocks deployment; never put subscription or tenant IDs here.')
param regionCheckReference string = ''
@description('Reference to a dated, reviewed quota check for Container Apps, SQL, IoT and the exact model versions/SKUs/capacities in the selected subscription. Empty blocks deployment; no IDs or secrets.')
param quotaCheckReference string = ''
@description('Mailbox for platform alerts.')
param alertEmail string
@description('Optional Teams Workflows webhook URL for operations alerts.')
@secure()
param teamsWebhookUrl string = ''
@description('Evidence document store. blob is the default; sharepoint needs the M365 steps in the ADR and infra/scripts/grant-sharepoint-access.sh.')
@allowed(['blob', 'sharepoint'])
param evidenceStore string = 'blob'
param sharePointSiteId string = ''
@description('Monthly budget in the billing currency, with alerts at 80 and 100 percent forecast and actual.')
param monthlyBudget int = 300
param budgetStartDate string = utcNow('yyyy-MM-01')
@description('IoT Hub tier for simulated in-use monitoring (ADR 0003 decision 6, issue 140).')
@allowed(['B1', 'S1'])
param iotHubSku string = 'B1'
@minValue(1)
param iotHubUnits int = 1
@minValue(1)
@maxValue(7)
param iotHubRetentionDays int = 1
@description('Estimated monthly IoT Hub cost in the billing currency; sets the hub-scoped budget. An estimate to confirm against the Azure pricing page before provisioning.')
param iotHubMonthlyCost int = 25
@description('Entra security group that administers the SQL server (no SQL logins exist).')
param sqlAdminGroupName string
param sqlAdminGroupObjectId string
@allowed(['Group', 'User', 'Application'])
param sqlAdminPrincipalType string = 'Group'
@description('Entra app registration client ID protecting the workbench API. Leave empty to deploy without app authentication (not for shared use).')
param entraClientId string = ''
@description('Explicit Entra role-value mapping for an existing registration. Empty uses the application defaults. Transitional mappings do not rename tenant roles.')
param entraRoleMap object = {}
@description('Provision private token-only storage and its maintenance identity/job for delegated Microsoft profile photos.')
param enableEntraTokenStore bool = false
@description('Activate EasyAuth token storage only after the maintenance job has successfully written its first SAS secret.')
param entraTokenStoreReady bool = false
@description('Container images. The default placeholder lets infrastructure deploy before application images exist.')
param apiImage string = 'mcr.microsoft.com/k8se/quickstart:latest'
@description('Enable direct model calls from the existing MVP API. Leave false for the proposed separate agent-runner topology; true grants the API model invocation rights and configures AI_ENDPOINT.')
param enableApiAi bool = false
@description('False bootstraps dependencies without exposing placeholder apps. Build/push the real image, provision the auth secret and seed SQL, then redeploy with true.')
param deployApplications bool = true
@description('Create the VNet-injected environment and DNS before SQL initialization, without starting workloads.')
param deployEnvironmentOnly bool = false
@description('Opt-in service smoke mode: validate bearer tokens without interactive login or a vault client secret. Requires entraClientId; incompatible with delegated token storage.')
param entraBearerOnly bool = false
param agentImage string = 'mcr.microsoft.com/k8se/quickstart:latest'
@description('Empty means the bootstrap placeholder. Use infra/scripts/deploy.py to preserve an existing job image or resolve the newest registry tag before deploying.')
param orchestratorImage string = ''
param importImage string = 'mcr.microsoft.com/k8se/quickstart:latest'
@description('Deploy Front Door Premium, a WAF policy and a Private Link origin to the internal environment (ADR 0002 decision 6). WARNING: Private Link to the managedEnvironments group of an internal VNet-injected environment is unverified for this configuration (open item). Production profile only; the private endpoint connection needs approval (infra/README.md, Public edge).')
param enablePublicEdge bool = false
@description('Optional edge custom domain (managed TLS certificate). Empty uses the default azurefd.net host.')
param edgeCustomDomain string = ''
@allowed(['Detection', 'Prevention'])
param edgeWafMode string = 'Prevention'
@description('Enable zone redundancy where the region supports it.')
param zoneRedundant bool = false

@description('Production (default) enforces isolation, quarantine and purge protection. Development permits individual explicit opt-outs; choosing development alone relaxes nothing. SQL is always private.')
@allowed(['production', 'development'])
param deploymentProfile string = 'production'

@description('Development only. Explicit public opt-in for services other than SQL, which is always private. Keep false for shared stacks.')
param allowPublicNetworkAccess bool = false

@description('Development only. False sets a 7 day Key Vault soft delete without purge protection so the name can be purged and reused.')
param keyVaultPurgeProtection bool = true
@description('Development only. Explicit false permits immediate image pulls without quarantine. Production requires true.')
param registryQuarantineEnabled bool = true
@description('CanNotDelete locks on stateful resources.')
param enableLocks bool = false
@description('Model deployments. The standard tier is the default; the capable tier is used only where the PRD model evaluation shows the standard tier misses a task threshold.')
param modelDeployments array = [
  {
    name: 'standard'
    model: 'gpt-4.1-mini'
    version: '2025-04-14'
    skuName: 'GlobalStandard'
    capacity: 30
  }
  {
    name: 'capable'
    model: 'gpt-4.1'
    version: '2025-04-14'
    skuName: 'GlobalStandard'
    capacity: 30
  }
]
@description('Region for the Azure SQL server when the primary region is not accepting new SQL servers. The private endpoint stays in the primary VNet.')
param sqlLocation string = location
@description('Map tile URL template for the workbench map (https). Development may use https://tile.openstreetmap.org/{z}/{x}/{y}.png within its usage policy.')
param tileUrl string = ''
param tileAttribution string = ''
param tags object = {}
@description('Owner tag value required by the tagging standard (infra/README.md, Governance controls).')
param ownerTag string = 'Juan Manuel Servera'

var isDev = deploymentProfile == 'development'
var publicAccess = isDev && allowPublicNetworkAccess
var purgeProtection = !isDev || keyVaultPurgeProtection

var prefix = '${workload}-${environmentName}'
var unique = take(uniqueString(resourceGroup().id, location, 'v2'), 5)
var compact = replace(prefix, '-', '')
var allTags = union(tags, {
  workload: 'zava-forward-demonstrator'
  environment: environmentName
  dataClassification: 'constructed-non-identifying'
  purpose: 'non-production-demonstrator'
  owner: ownerTag
})

var storageBlobDataContributor = 'ba92f5b4-2d11-453d-a403-e96b0029c9fe'
var storageQueueDataContributor = '974c5e8b-45b9-4653-ba55-5f855dd0fb88'
var storageQueueDataSender = 'c6a89b2d-59bc-44d0-9896-0f6e12d7b80a'

module guard 'modules/guard.bicep' = {
  name: 'parameter-guard'
  params: {
    productionProfileForbidsPublicNetworkAccess: isDev || !allowPublicNetworkAccess ? 'ok' : ''
    productionProfileRequiresKeyVaultPurgeProtection: isDev || keyVaultPurgeProtection ? 'ok' : ''
    productionProfileRequiresRegistryQuarantine: isDev || registryQuarantineEnabled ? 'ok' : ''
    regionCheckMustBeRecorded: !empty(regionCheckReference) ? 'ok' : ''
    quotaCheckMustBeRecorded: !empty(quotaCheckReference) ? 'ok' : ''
    deploymentLocationsMustBeSelected: !empty(location) && !empty(sqlLocation) ? 'ok' : ''
    publicEdgeRequiresProductionProfile: !enablePublicEdge || (!isDev && !allowPublicNetworkAccess) ? 'ok' : ''
    pilotRequiresProductionProfile: environmentName != 'pilot' || (!isDev && !allowPublicNetworkAccess) ? 'ok' : ''
    publicEdgeRequiresApplications: !enablePublicEdge || deployApplications ? 'ok' : ''
    sharePointEvidenceStoreRequiresSiteId: evidenceStore != 'sharepoint' || !empty(sharePointSiteId) ? 'ok' : ''
    tokenStoreReadyRequiresTokenStore: !entraTokenStoreReady || enableEntraTokenStore ? 'ok' : ''
    entraRoleMapRequiresEntraClientId: empty(entraRoleMap) || !empty(entraClientId) ? 'ok' : ''
    bearerOnlyRequiresAudience: !entraBearerOnly || (!empty(entraClientId) && !enableEntraTokenStore && !entraTokenStoreReady) ? 'ok' : ''
  }
}

module identity 'modules/identity.bicep' = {
  name: 'identity'
  dependsOn: [guard]
  params: { prefix: prefix, location: location, tags: allTags }
}

module network 'modules/network.bicep' = {
  name: 'network'
  dependsOn: [guard]
  params: { prefix: prefix, location: location, tags: allTags }
}

module monitoring 'modules/monitoring.bicep' = {
  name: 'monitoring'
  dependsOn: [guard]
  params: {
    allowPublicNetworkAccess: publicAccess
    prefix: prefix
    location: location
    tags: allTags
    alertEmail: alertEmail
    teamsWebhookUrl: teamsWebhookUrl
    peSubnetId: network.outputs.peSubnetId
    zoneIds: network.outputs.zoneIds
  }
}

module keyvault 'modules/keyvault.bicep' = {
  name: 'keyvault'
  dependsOn: [guard]
  params: {
    allowPublicNetworkAccess: publicAccess
    purgeProtection: purgeProtection
    name: 'kv-${compact}-${unique}'
    location: location
    tags: allTags
    workspaceId: monitoring.outputs.workspaceId
    actionGroupId: monitoring.outputs.actionGroupId
    peSubnetId: network.outputs.peSubnetId
    zoneId: network.outputs.zoneIds.vault
    secretsUserPrincipalIds: [identity.outputs.principalIds.api]
    enableLock: enableLocks
  }
}

module storage 'modules/storage.bicep' = {
  name: 'storage'
  dependsOn: [guard]
  params: {
    allowPublicNetworkAccess: publicAccess
    name: 'st${compact}${unique}'
    location: location
    tags: allTags
    workspaceId: monitoring.outputs.workspaceId
    peSubnetId: network.outputs.peSubnetId
    zoneIds: network.outputs.zoneIds
    enableLock: enableLocks
    zoneRedundant: zoneRedundant
    roleAssignments: [
      { principalId: identity.outputs.principalIds.api, roleDefinitionId: storageBlobDataContributor, scope: 'blob' }
      { principalId: identity.outputs.principalIds.api, roleDefinitionId: storageQueueDataSender, scope: 'queue' }
      { principalId: identity.outputs.principalIds.import, roleDefinitionId: storageBlobDataContributor, scope: 'blob' }
      { principalId: identity.outputs.principalIds.import, roleDefinitionId: storageQueueDataContributor, scope: 'queue' }
      { principalId: identity.outputs.principalIds.orchestrator, roleDefinitionId: storageQueueDataSender, scope: 'queue' }
      { principalId: identity.outputs.principalIds.agents, roleDefinitionId: storageQueueDataContributor, scope: 'queue' }
    ]
  }
}

module registry 'modules/registry.bicep' = {
  name: 'registry'
  dependsOn: [guard]
  params: {
    allowPublicNetworkAccess: publicAccess
    quarantine: registryQuarantineEnabled
    name: 'cr${compact}${unique}'
    location: location
    tags: allTags
    workspaceId: monitoring.outputs.workspaceId
    peSubnetId: network.outputs.peSubnetId
    zoneId: network.outputs.zoneIds.acr
    zoneRedundant: zoneRedundant
    pullPrincipalIds: [
      identity.outputs.principalIds.api
      identity.outputs.principalIds.agents
      identity.outputs.principalIds.orchestrator
      identity.outputs.principalIds.import
    ]
  }
}

module sql 'modules/sql.bicep' = {
  name: 'sql'
  dependsOn: [guard]
  params: {
    name: 'sql-${prefix}-${unique}'
    databaseName: 'retrofit'
    location: sqlLocation
    endpointLocation: location
    tags: allTags
    workspaceId: monitoring.outputs.workspaceId
    peSubnetId: network.outputs.peSubnetId
    zoneId: network.outputs.zoneIds.sql
    entraAdminGroupName: sqlAdminGroupName
    entraAdminGroupObjectId: sqlAdminGroupObjectId
    entraAdminPrincipalType: sqlAdminPrincipalType
    enableLock: enableLocks
    zoneRedundant: zoneRedundant
  }
}

module foundry 'modules/foundry.bicep' = {
  name: 'foundry'
  dependsOn: [guard]
  params: {
    allowPublicNetworkAccess: publicAccess
    name: 'aif-${prefix}-${unique}'
    projectName: 'zava-forward-agents'
    location: location
    tags: allTags
    workspaceId: monitoring.outputs.workspaceId
    peSubnetId: network.outputs.peSubnetId
    zoneIds: network.outputs.zoneIds
    userPrincipalIds: enableApiAi
      ? [identity.outputs.principalIds.agents, identity.outputs.principalIds.api]
      : [identity.outputs.principalIds.agents]
    deployments: modelDeployments
  }
}

module iotHub 'modules/iothub.bicep' = {
  name: 'iothub'
  params: {
    allowPublicNetworkAccess: publicAccess
    name: 'iot-${prefix}-${unique}'
    location: location
    tags: allTags
    workspaceId: monitoring.outputs.workspaceId
    peSubnetId: network.outputs.peSubnetId
    zoneIds: network.outputs.zoneIds
    consumerPrincipalIds: [identity.outputs.principalIds.api]
    skuName: iotHubSku
    unitCount: iotHubUnits
    retentionDays: iotHubRetentionDays
    monthlyCostEstimate: iotHubMonthlyCost
    alertEmail: alertEmail
    budgetStartDate: budgetStartDate
  }
}

module apps 'modules/containerapps.bicep' = if (deployApplications || deployEnvironmentOnly) {
  name: 'containerapps'
  dependsOn: [guard]
  params: {
    allowPublicNetworkAccess: publicAccess
    behindPublicEdge: enablePublicEdge
    prefix: prefix
    location: location
    tags: allTags
    workspaceId: monitoring.outputs.workspaceId
    infrastructureSubnetId: network.outputs.acaSubnetId
    vnetId: network.outputs.vnetId
    identityIds: identity.outputs.ids
    identityClientIds: identity.outputs.clientIds
    registryServer: registry.outputs.loginServer
    appInsightsConnectionString: monitoring.outputs.appInsightsConnectionString
    sqlServerFqdn: sql.outputs.fqdn
    sqlDatabaseName: sql.outputs.databaseName
    storageAccountName: storage.outputs.name
    foundryEndpoint: foundry.outputs.endpoint
    foundryProjectName: foundry.outputs.projectName
    modelDeploymentNames: { standard: 'standard', capable: 'capable' }
    keyVaultUri: 'https://${keyvault.outputs.name}${environment().suffixes.keyvaultDns}'
    entraClientId: entraClientId
    deployWorkloads: deployApplications
    entraBearerOnly: entraBearerOnly
    entraRoleMap: entraRoleMap
    tokenStoreReady: enableEntraTokenStore && entraTokenStoreReady
    tokenStoreAccountName: enableEntraTokenStore ? authTokenStore!.outputs.accountName : ''
    tokenMaintenanceIdentityId: enableEntraTokenStore ? authTokenStore!.outputs.identityId : ''
    tokenMaintenanceClientId: enableEntraTokenStore ? authTokenStore!.outputs.identityClientId : ''
    tileUrl: tileUrl
    tileAttribution: tileAttribution
    zoneRedundant: zoneRedundant
    evidenceStore: evidenceStore
    sharePointSiteId: sharePointSiteId
    apiImage: apiImage
    enableApiAi: enableApiAi
    agentImage: agentImage
    orchestratorImage: empty(orchestratorImage) ? 'mcr.microsoft.com/k8se/quickstart:latest' : orchestratorImage
    importImage: importImage
  }

}

module edge 'modules/edge.bicep' = if (enablePublicEdge) {
  name: 'edge'
  dependsOn: [guard]
  params: {
    prefix: prefix
    tags: allTags
    environmentId: apps!.outputs.environmentId
    originHostName: apps!.outputs.apiFqdn
    privateLinkLocation: location
    customDomain: edgeCustomDomain
    wafMode: edgeWafMode
    workspaceId: monitoring.outputs.workspaceId
  }
}

module authTokenStore 'modules/authTokenStore.bicep' = if (enableEntraTokenStore) {
  name: 'auth-token-store'
  dependsOn: [guard]
  params: {
    name: 'st${take(compact, 13)}auth${unique}'
    prefix: prefix
    location: location
    tags: allTags
    workspaceId: monitoring.outputs.workspaceId
    peSubnetId: network.outputs.peSubnetId
    blobZoneId: network.outputs.zoneIds.blob
    keyVaultName: keyvault.outputs.name
    registryName: first(split(registry.outputs.loginServer, '.'))
    allowPublicNetworkAccess: publicAccess
    zoneRedundant: zoneRedundant
  }
}

resource agentThrottle 'Microsoft.Insights/metricAlerts@2018-03-01' = {
  name: 'alert-${prefix}-foundry-throttle'
  location: 'global'
  tags: allTags
  properties: {
    severity: 2
    enabled: true
    scopes: [foundry.outputs.id]
    evaluationFrequency: 'PT5M'
    windowSize: 'PT15M'
    criteria: {
      'odata.type': 'Microsoft.Azure.Monitor.SingleResourceMultipleMetricCriteria'
      allOf: [
        {
          name: 'throttled'
          metricName: 'ClientErrors'
          operator: 'GreaterThan'
          threshold: 20
          timeAggregation: 'Total'
          criterionType: 'StaticThresholdCriterion'
        }
      ]
    }
    actions: [{ actionGroupId: monitoring.outputs.actionGroupId }]
  }
}

resource sqlCpu 'Microsoft.Insights/metricAlerts@2018-03-01' = {
  name: 'alert-${prefix}-sql-cpu'
  location: 'global'
  tags: allTags
  properties: {
    severity: 3
    enabled: true
    scopes: [resourceId('Microsoft.Sql/servers/databases', 'sql-${prefix}-${unique}', 'retrofit')]
    evaluationFrequency: 'PT5M'
    windowSize: 'PT15M'
    criteria: {
      'odata.type': 'Microsoft.Azure.Monitor.SingleResourceMultipleMetricCriteria'
      allOf: [
        {
          name: 'cpu'
          metricName: 'cpu_percent'
          operator: 'GreaterThan'
          threshold: 85
          timeAggregation: 'Average'
          criterionType: 'StaticThresholdCriterion'
        }
      ]
    }
    actions: [{ actionGroupId: monitoring.outputs.actionGroupId }]
  }
  dependsOn: [sql]
}

resource apiErrors 'Microsoft.Insights/metricAlerts@2018-03-01' = if (deployApplications) {
  name: 'alert-${prefix}-api-5xx'
  location: 'global'
  tags: allTags
  properties: {
    severity: 2
    enabled: true
    scopes: [apps!.outputs.apiId]
    evaluationFrequency: 'PT1M'
    windowSize: 'PT5M'
    criteria: {
      'odata.type': 'Microsoft.Azure.Monitor.SingleResourceMultipleMetricCriteria'
      allOf: [
        {
          name: 'server-errors'
          metricName: 'Requests'
          dimensions: [{ name: 'statusCodeCategory', operator: 'Include', values: ['5xx'] }]
          operator: 'GreaterThan'
          threshold: 5
          timeAggregation: 'Total'
          criterionType: 'StaticThresholdCriterion'
        }
      ]
    }
    actions: [{ actionGroupId: monitoring.outputs.actionGroupId }]
  }
}

resource apiRestarts 'Microsoft.Insights/metricAlerts@2018-03-01' = if (deployApplications) {
  name: 'alert-${prefix}-api-restarts'
  location: 'global'
  tags: allTags
  properties: {
    severity: 3
    enabled: true
    scopes: [apps!.outputs.apiId]
    evaluationFrequency: 'PT5M'
    windowSize: 'PT15M'
    criteria: {
      'odata.type': 'Microsoft.Azure.Monitor.SingleResourceMultipleMetricCriteria'
      allOf: [
        {
          name: 'restarts'
          metricName: 'RestartCount'
          operator: 'GreaterThan'
          threshold: 3
          timeAggregation: 'Total'
          criterionType: 'StaticThresholdCriterion'
        }
      ]
    }
    actions: [{ actionGroupId: monitoring.outputs.actionGroupId }]
  }
}

resource ledgerDigestMismatch 'Microsoft.Insights/scheduledQueryRules@2023-03-15-preview' = if (deployApplications) {
  name: 'alert-${prefix}-ledger-digest-mismatch'
  location: location
  tags: allTags
  properties: {
    displayName: 'Ledger does not match the immutable digests'
    description: 'The scheduled ledger verification job reported LEDGER_DIGEST_ALERT, or the job run failed.'
    severity: 1
    enabled: true
    scopes: [monitoring.outputs.workspaceId]
    evaluationFrequency: 'PT1H'
    windowSize: 'PT1H'
    criteria: {
      allOf: [
        {
          query: 'ContainerAppConsoleLogs | where JobName startswith "job-${prefix}-ledger-verify" and Log has "LEDGER_DIGEST_ALERT"'
          timeAggregation: 'Count'
          operator: 'GreaterThan'
          threshold: 0
          failingPeriods: { numberOfEvaluationPeriods: 1, minFailingPeriodsToAlert: 1 }
        }
      ]
    }
    actions: { actionGroups: [monitoring.outputs.actionGroupId] }
  }
}

resource ledgerVerifyMissing 'Microsoft.Insights/scheduledQueryRules@2023-03-15-preview' = if (deployApplications) {
  name: 'alert-${prefix}-ledger-verify-missing'
  location: location
  tags: allTags
  properties: {
    displayName: 'Ledger verification did not report success'
    description: 'No LEDGER_DIGEST_OK line from the daily verification job in 26 hours: the job failed to start or run, or logs are missing. Table names are unconfirmed until checked in the deployed workspace.'
    severity: 1
    enabled: true
    scopes: [monitoring.outputs.workspaceId]
    evaluationFrequency: 'PT1H'
    windowSize: 'P1D'
    criteria: {
      allOf: [
        {
          query: 'ContainerAppConsoleLogs | where JobName startswith "job-${prefix}-ledger-verify" and Log has "LEDGER_DIGEST_OK" | where TimeGenerated > ago(26h)'
          timeAggregation: 'Count'
          operator: 'LessThan'
          threshold: 1
          failingPeriods: { numberOfEvaluationPeriods: 1, minFailingPeriodsToAlert: 1 }
        }
      ]
    }
    actions: { actionGroups: [monitoring.outputs.actionGroupId] }
  }
}

resource budget 'Microsoft.Consumption/budgets@2023-05-01' = {
  name: 'budget-${prefix}'
  dependsOn: [guard]
  properties: {
    category: 'Cost'
    amount: monthlyBudget
    timeGrain: 'Monthly'
    timePeriod: { startDate: budgetStartDate }
    notifications: {
      actual80: {
        enabled: true
        operator: 'GreaterThan'
        threshold: 80
        thresholdType: 'Actual'
        contactEmails: [alertEmail]
      }
      forecast100: {
        enabled: true
        operator: 'GreaterThan'
        threshold: 100
        thresholdType: 'Forecasted'
        contactEmails: [alertEmail]
      }
    }
  }
}

output apiInternalFqdn string = deployApplications ? apps!.outputs.apiFqdn : ''
output containerRegistry string = registry.outputs.loginServer
output sqlServer string = sql.outputs.fqdn
output iotHubName string = iotHub.outputs.name
output iotHubConsumerGroup string = iotHub.outputs.consumerGroup
output foundryEndpoint string = foundry.outputs.endpoint
output identityPrincipalIds object = identity.outputs.principalIds
output logAnalyticsWorkspace string = monitoring.outputs.workspaceName
output publicEdgeHostName string = enablePublicEdge ? edge!.outputs.publicHostName : ''
output entraRedirectUri string = enablePublicEdge ? edge!.outputs.entraRedirectUri : ''
