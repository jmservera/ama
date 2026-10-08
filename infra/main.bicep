targetScope = 'resourceGroup'

@description('Short workload prefix, lower case, 3 to 10 characters.')
@minLength(3)
@maxLength(10)
param workload string = 'warm'
@allowed(['dev', 'test'])
param environmentName string = 'dev'
param location string = resourceGroup().location
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
@description('Entra security group that administers the SQL server (no SQL logins exist).')
param sqlAdminGroupName string
param sqlAdminGroupObjectId string
@allowed(['Group', 'User', 'Application'])
param sqlAdminPrincipalType string = 'Group'
@description('Entra app registration client ID protecting the workbench API. Leave empty to deploy without app authentication (not for shared use).')
param entraClientId string = ''
@description('Container images. The default placeholder lets infrastructure deploy before application images exist.')
param apiImage string = 'mcr.microsoft.com/k8se/quickstart:latest'
param agentImage string = 'mcr.microsoft.com/k8se/quickstart:latest'
param orchestratorImage string = 'mcr.microsoft.com/k8se/quickstart:latest'
param importImage string = 'mcr.microsoft.com/k8se/quickstart:latest'
@description('Enable zone redundancy where the region supports it.')
param zoneRedundant bool = false

@description('Deployment profile. production (default) enforces network isolation, registry image quarantine and Key Vault purge protection. development relaxes all three so a throwaway stack is reachable and iterable.')
@allowed(['production', 'development'])
param deploymentProfile string = 'production'

@description('Development only. When true, resources also accept connections from external networks (public endpoints, wide-open SQL firewall, external Container Apps environment). Keep false for anything but a throwaway dev stack.')
param allowPublicNetworkAccess bool = false

@description('Development only. False sets a 7 day Key Vault soft delete without purge protection so the name can be purged and reused.')
param keyVaultPurgeProtection bool = true
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
param tags object = {}

var isDev = deploymentProfile == 'development'
var publicAccess = isDev || allowPublicNetworkAccess
var purgeProtection = !isDev && keyVaultPurgeProtection

var prefix = '${workload}-${environmentName}'
var unique = take(uniqueString(resourceGroup().id, location, 'v2'), 5)
var compact = replace(prefix, '-', '')
var allTags = union(tags, {
  workload: 'proper-warm-demonstrator'
  environment: environmentName
  dataClassification: 'constructed-non-identifying'
  purpose: 'non-production-demonstrator'
})

var storageBlobDataContributor = 'ba92f5b4-2d11-453d-a403-e96b0029c9fe'
var storageQueueDataContributor = '974c5e8b-45b9-4653-ba55-5f855dd0fb88'
var storageQueueDataSender = 'c6a89b2d-59bc-44d0-9896-0f6e12d7b80a'

module identity 'modules/identity.bicep' = {
  name: 'identity'
  params: { prefix: prefix, location: location, tags: allTags }
}

module network 'modules/network.bicep' = {
  name: 'network'
  params: { prefix: prefix, location: location, tags: allTags }
}

module monitoring 'modules/monitoring.bicep' = {
  name: 'monitoring'
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
  params: {
    allowPublicNetworkAccess: publicAccess
    purgeProtection: purgeProtection
    name: 'kv-${compact}-${unique}'
    location: location
    tags: allTags
    workspaceId: monitoring.outputs.workspaceId
    peSubnetId: network.outputs.peSubnetId
    zoneId: network.outputs.zoneIds.vault
    secretsUserPrincipalIds: [identity.outputs.principalIds.api]
    enableLock: enableLocks
  }
}

module storage 'modules/storage.bicep' = {
  name: 'storage'
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
  params: {
    allowPublicNetworkAccess: publicAccess
    quarantine: !isDev
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
  params: {
    allowPublicNetworkAccess: publicAccess
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
  params: {
    allowPublicNetworkAccess: publicAccess
    name: 'aif-${prefix}-${unique}'
    projectName: 'proper-warm-agents'
    location: location
    tags: allTags
    workspaceId: monitoring.outputs.workspaceId
    peSubnetId: network.outputs.peSubnetId
    zoneIds: network.outputs.zoneIds
    userPrincipalIds: [identity.outputs.principalIds.agents]
    deployments: modelDeployments
  }
}

module apps 'modules/containerapps.bicep' = {
  name: 'containerapps'
  params: {
    allowPublicNetworkAccess: publicAccess
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
    zoneRedundant: zoneRedundant
    evidenceStore: evidenceStore
    sharePointSiteId: sharePointSiteId
    apiImage: apiImage
    agentImage: agentImage
    orchestratorImage: orchestratorImage
    importImage: importImage
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

resource apiErrors 'Microsoft.Insights/metricAlerts@2018-03-01' = {
  name: 'alert-${prefix}-api-5xx'
  location: 'global'
  tags: allTags
  properties: {
    severity: 2
    enabled: true
    scopes: [apps.outputs.apiId]
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

resource apiRestarts 'Microsoft.Insights/metricAlerts@2018-03-01' = {
  name: 'alert-${prefix}-api-restarts'
  location: 'global'
  tags: allTags
  properties: {
    severity: 3
    enabled: true
    scopes: [apps.outputs.apiId]
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

resource budget 'Microsoft.Consumption/budgets@2023-05-01' = {
  name: 'budget-${prefix}'
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

output apiInternalFqdn string = apps.outputs.apiFqdn
output containerRegistry string = registry.outputs.loginServer
output sqlServer string = sql.outputs.fqdn
output foundryEndpoint string = foundry.outputs.endpoint
output identityPrincipalIds object = identity.outputs.principalIds
output logAnalyticsWorkspace string = monitoring.outputs.workspaceName
