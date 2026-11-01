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
@description('Monthly budget in the billing currency. Notifications above 80 percent actual and 100 percent forecast are not a hard cap.')
param monthlyBudget int = 300
param budgetStartDate string = utcNow('yyyy-MM-01')
@description('Enable new job/IoT alert candidates only after separate named-human signal, owner and threshold approval. Defaults disabled; see infra/monitoring-runbooks.md.')
param enableCandidateMonitoringAlerts bool = false
@description('Non-secret reference to separate monitoring activation approval. Empty or whitespace keeps candidates disabled; a string is not approval evidence by itself.')
param monitoringApprovalReference string = ''
@description('IoT Hub tier for simulated in-use monitoring (ADR 0003 decision 6, issue 140).')
@allowed(['B1'])
param iotHubSku string = 'B1'
@minValue(1)
@maxValue(1)
param iotHubUnits int = 1
@minValue(1)
@maxValue(7)
param iotHubRetentionDays int = 1
@description('Monthly IoT transport allocation in the billing currency, including the keyless Event Hub adapter and endpoints. Alerts only; verify total USD700 headroom before any provisioning.')
@minValue(1)
@maxValue(700)
param iotHubMonthlyCost int = 60
@description('Bootstrap false registers no custom endpoint or route. Set and preserve true only after separately approved IoT sender-role propagation verification.')
param iotHubRoutingReady bool = false
@description('Entra security group that administers the SQL server (no SQL logins exist).')
param sqlAdminGroupName string
param sqlAdminGroupObjectId string
@allowed(['Group', 'User', 'Application'])
param sqlAdminPrincipalType string = 'Group'
@description('Entra app registration client ID protecting the workbench API. Leave empty to deploy without app authentication (not for shared use).')
param entraClientId string = ''
@description('Key Vault and Container App secret name for browser authentication. Retain the private setup-selected name on redeploy; never put the secret value here.')
param entraClientSecretName string = 'entra-client-secret'
@description('Browser credential storage. App-local demo credentials block application redeployment; use deployApplications=false for dependency-only updates. Wrappers discover the deployed tag and refuse an unsafe full deployment.')
@allowed(['keyvault', 'app'])
param entraCredentialStore string = 'keyvault'
@description('Explicit Entra role-value mapping for an existing registration. Empty uses the application defaults. Transitional mappings do not rename tenant roles.')
param entraRoleMap object = {}
@description('Provision private token-only storage and its maintenance identity/job for delegated Microsoft profile photos.')
param enableEntraTokenStore bool = false
@description('Activate EasyAuth token storage only after the maintenance job has successfully written its first SAS secret.')
param entraTokenStoreReady bool = false
@description('Container images. The default placeholder lets infrastructure deploy before application images exist.')
param apiImage string = 'mcr.microsoft.com/k8se/quickstart:latest'
@description('Minimum API replicas. Default 0 permits scale-to-zero for cost-safe demos and cold starts; set 2 explicitly for always-on production replicas.')
@minValue(0)
@maxValue(4)
param apiMinReplicas int = 0
@description('Enable direct model calls from the existing MVP API. Leave false for the proposed separate agent-runner topology; true grants the API model invocation rights and configures AI_ENDPOINT.')
param enableApiAi bool = false
@description('False bootstraps dependencies without exposing placeholder apps. Build/push the real image, provision the auth secret and seed SQL, then redeploy with true.')
param deployApplications bool = true
@description('Omit every agent and background job when false, allowing API-only staging without competing queue or scheduled consumers. Does not stop workloads already deployed in another generation.')
param deployBackgroundWorkloads bool = true
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
@description('Development-only direct HTTPS demo in a separately named environment and subnet. Requires private backing services and browser Entra authentication when applications deploy; incompatible with Front Door.')
param demoDirectIngress bool = false
@description('Optional edge custom domain (managed TLS certificate). Empty uses the default azurefd.net host.')
param edgeCustomDomain string = ''
@allowed(['Detection', 'Prevention'])
param edgeWafMode string = 'Prevention'
@description('Enable zone redundancy where the region supports it.')
param zoneRedundant bool = false

@description('SQL tier: serverless for dev, provisioned general purpose for pilot (ADR 0002 decision 1).')
@allowed(['serverless', 'provisioned'])
param sqlTier string = 'serverless'
@description('SQL vCores: serverless maximum or provisioned count.')
param sqlVCores int = 2
@description('Serverless only. Auto-pause delay in minutes: -1 disables, otherwise 15 to 10080.')
param sqlAutoPauseDelayMinutes int = 60
@description('SQL backup storage redundancy. Empty derives Zone when zoneRedundant, otherwise Local.')
@allowed(['', 'Local', 'Zone', 'Geo', 'GeoZone'])
param sqlBackupStorageRedundancy string = ''
@description('SQL point-in-time restore window in days (1 to 35).')
@minValue(1)
@maxValue(35)
param sqlBackupRetentionDays int = 14

@description('Production (default) enforces isolation, quarantine and purge protection. Development permits individual explicit opt-outs; choosing development alone relaxes nothing. SQL is always private.')
@allowed(['production', 'development'])
param deploymentProfile string = 'production'

@description('Development only. Explicit public opt-in for services other than SQL, which is always private. Keep false for shared stacks.')
param allowPublicNetworkAccess bool = false

@description('Development only. False sets a 7 day Key Vault soft delete without purge protection so the name can be purged and reused.')
param keyVaultPurgeProtection bool = true
@description('Development only. Explicit false permits immediate image pulls without quarantine. Production requires true.')
param registryQuarantineEnabled bool = true
@description('CanNotDelete locks on stateful resources. Required for pilot deployments.')
param enableLocks bool = false
@description('Small employee chat model. Model availability and task evaluation must be checked before activation.')
param chatModelName string = 'gpt-4.1-nano'
@description('Pinned ARM model version, not the combined provider response-model identity.')
param chatModelVersion string = '2025-04-14'
@allowed(['GlobalStandard', 'Standard'])
param chatModelSku string = 'GlobalStandard'
@description('Chat model throughput capacity, not a monetary spending cap. One is the smallest requested allocation.')
@minValue(1)
param chatModelCapacity int = 1
@description('Explicit model override for existing/evaluated stacks. First entry serves standard; second serves capable, or the first serves both when only one is configured. A shared model does not establish capable-tier quality.')
@minLength(1)
param modelDeployments array = [
  {
    name: 'standard'
    model: chatModelName
    version: chatModelVersion
    skuName: chatModelSku
    capacity: chatModelCapacity
  }
]
@description('Region for the Azure SQL server when the primary region is not accepting new SQL servers. The private endpoint stays in the primary VNet.')
param sqlLocation string = location
@description('Map tile URL template for the workbench map (https). Development may use https://tile.openstreetmap.org/{z}/{x}/{y}.png within its usage policy.')
param tileUrl string = ''
param tileAttribution string = ''
@description('Owner-recorded chat privacy references (docs/reference/research/chat-demo-storage-approval-2026-11-01.md). All four refs must be set to send the settings; empty keeps chat storage refused.')
param chatDpiaRef string = ''
param chatLawfulBasisRef string = ''
param chatNoticeRef string = ''
param chatRetentionRef string = ''
@minValue(0)
param chatRetentionDays int = 0
param tags object = {}
@description('Owner tag value required by the tagging standard (infra/README.md, Governance controls).')
param ownerTag string = 'Juan Manuel Servera'

var isDev = deploymentProfile == 'development'
var publicAccess = isDev && allowPublicNetworkAccess
var purgeProtection = !isDev || keyVaultPurgeProtection

var prefix = '${workload}-${environmentName}'
var applicationPrefix = demoDirectIngress ? '${prefix}-demo' : prefix
var ledgerJobName = demoDirectIngress ? 'job-${applicationPrefix}-audit' : 'job-${applicationPrefix}-ledger-verify'
var unique = take(uniqueString(resourceGroup().id, location, 'v2'), 5)
var compact = replace(prefix, '-', '')
var allTags = union(tags, {
  workload: 'zava-forward-demonstrator'
  environment: environmentName
  'zava-forward-deployment-profile': deploymentProfile
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
    resourceGroupMustBeAma: resourceGroup().name == 'ama' ? 'ok' : ''
    primaryLocationMustBeUKSouth: location == 'uksouth' ? 'ok' : ''
    productionProfileForbidsPublicNetworkAccess: isDev || !allowPublicNetworkAccess ? 'ok' : ''
    productionProfileRequiresKeyVaultPurgeProtection: isDev || keyVaultPurgeProtection ? 'ok' : ''
    productionProfileRequiresRegistryQuarantine: isDev || registryQuarantineEnabled ? 'ok' : ''
    regionCheckMustBeRecorded: !empty(regionCheckReference) ? 'ok' : ''
    quotaCheckMustBeRecorded: !empty(quotaCheckReference) ? 'ok' : ''
    deploymentLocationsMustBeSelected: !empty(location) && !empty(sqlLocation) ? 'ok' : ''
    publicEdgeRequiresProductionProfile: !enablePublicEdge || (!isDev && !allowPublicNetworkAccess) ? 'ok' : ''
    pilotRequiresProductionProfile: environmentName != 'pilot' || (!isDev && !allowPublicNetworkAccess) ? 'ok' : ''
    pilotRequiresLocks: environmentName != 'pilot' || enableLocks ? 'ok' : ''
    publicEdgeRequiresApplications: !enablePublicEdge || deployApplications ? 'ok' : ''
    sharePointEvidenceStoreRequiresSiteId: evidenceStore != 'sharepoint' || !empty(sharePointSiteId) ? 'ok' : ''
    tokenStoreReadyRequiresTokenStore: !entraTokenStoreReady || enableEntraTokenStore ? 'ok' : ''
    entraRoleMapRequiresEntraClientId: empty(entraRoleMap) || !empty(entraClientId) ? 'ok' : ''
    bearerOnlyRequiresAudience: !entraBearerOnly || (!empty(entraClientId) && !enableEntraTokenStore && !entraTokenStoreReady) ? 'ok' : ''
    demoRequiresDevelopmentProfile: !demoDirectIngress || isDev ? 'ok' : ''
    demoForbidsPublicEdge: !demoDirectIngress || !enablePublicEdge ? 'ok' : ''
    demoRequiresPrivateBackingServices: !demoDirectIngress || !allowPublicNetworkAccess ? 'ok' : ''
    demoRequiresBrowserAuthentication: !demoDirectIngress || !deployApplications || (!empty(entraClientId) && !entraBearerOnly) ? 'ok' : ''
    appCredentialRequiresDirectDemo: entraCredentialStore != 'app' || (demoDirectIngress && !entraBearerOnly && !empty(entraClientId)) ? 'ok' : ''
    appCredentialBlocksApplicationDeployment: entraCredentialStore != 'app' || !deployApplications ? 'ok' : ''
    serverlessAutoPauseDelayMustBeSupported: sqlTier != 'serverless' || sqlAutoPauseDelayMinutes == -1 || (sqlAutoPauseDelayMinutes >= 15 && sqlAutoPauseDelayMinutes <= 10080) ? 'ok' : ''
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
  params: { prefix: prefix, location: location, tags: allTags, demoDirectIngress: demoDirectIngress }
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
    sqlTier: sqlTier
    maxVCores: sqlVCores
    autoPauseDelayMinutes: sqlAutoPauseDelayMinutes
    backupStorageRedundancy: sqlBackupStorageRedundancy
    backupRetentionDays: sqlBackupRetentionDays
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
  dependsOn: [guard]
  params: {
    allowPublicNetworkAccess: publicAccess
    name: 'iot-${prefix}-${unique}'
    location: location
    tags: allTags
    workspaceId: monitoring.outputs.workspaceId
    peSubnetId: network.outputs.peSubnetId
    zoneIds: network.outputs.zoneIds
    consumerPrincipalId: identity.outputs.principalIds.api
    skuName: iotHubSku
    unitCount: iotHubUnits
    retentionDays: iotHubRetentionDays
    monthlyCostEstimate: iotHubMonthlyCost
    routingReady: iotHubRoutingReady
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
    demoDirectIngress: demoDirectIngress
    prefix: applicationPrefix
    location: location
    tags: allTags
    workspaceId: monitoring.outputs.workspaceId
    infrastructureSubnetId: demoDirectIngress ? network.outputs.demoAcaSubnetId : network.outputs.acaSubnetId
    vnetId: network.outputs.vnetId
    identityIds: identity.outputs.ids
    identityClientIds: identity.outputs.clientIds
    registryServer: registry.outputs.loginServer
    appInsightsConnectionString: monitoring.outputs.appInsightsConnectionString
    sqlServerFqdn: sql.outputs.fqdn
    sqlDatabaseName: sql.outputs.databaseName
    storageAccountName: storage.outputs.name
    foundryEndpoint: foundry.outputs.endpoint
    openAiEndpoint: foundry.outputs.openAiEndpoint
    foundryProjectName: foundry.outputs.projectName
    modelDeploymentNames: foundry.outputs.modelDeploymentNames
    modelVersions: foundry.outputs.modelVersions
    keyVaultUri: 'https://${keyvault.outputs.name}${environment().suffixes.keyvaultDns}'
    entraClientId: entraClientId
    entraClientSecretName: entraClientSecretName
    entraCredentialStore: entraCredentialStore
    deployWorkloads: deployApplications
    apiMinReplicas: apiMinReplicas
    deployBackgroundWorkloads: deployBackgroundWorkloads
    entraBearerOnly: entraBearerOnly
    entraRoleMap: entraRoleMap
    tokenStoreReady: enableEntraTokenStore && entraTokenStoreReady
    tokenStoreAccountName: enableEntraTokenStore ? authTokenStore!.outputs.accountName : ''
    tokenMaintenanceIdentityId: enableEntraTokenStore ? authTokenStore!.outputs.identityId : ''
    tokenMaintenanceClientId: enableEntraTokenStore ? authTokenStore!.outputs.identityClientId : ''
    tileUrl: tileUrl
    tileAttribution: tileAttribution
    chatDpiaRef: chatDpiaRef
    chatLawfulBasisRef: chatLawfulBasisRef
    chatNoticeRef: chatNoticeRef
    chatRetentionRef: chatRetentionRef
    chatRetentionDays: chatRetentionDays
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
  name: 'alert-${applicationPrefix}-api-5xx'
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
  name: 'alert-${applicationPrefix}-api-restarts'
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

resource ledgerDigestMismatch 'Microsoft.Insights/scheduledQueryRules@2023-03-15-preview' = if (deployApplications && deployBackgroundWorkloads) {
  name: 'alert-${applicationPrefix}-ledger-digest-mismatch'
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
          query: 'ContainerAppConsoleLogs | where JobName startswith "${ledgerJobName}" and Log has "LEDGER_DIGEST_ALERT"'
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

resource ledgerVerifyMissing 'Microsoft.Insights/scheduledQueryRules@2023-03-15-preview' = if (deployApplications && deployBackgroundWorkloads) {
  name: 'alert-${applicationPrefix}-ledger-verify-missing'
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
    overrideQueryTimeRange: 'PT26H'
    criteria: {
      allOf: [
        {
          query: 'ContainerAppConsoleLogs | where JobName startswith "${ledgerJobName}" and Log has "LEDGER_DIGEST_OK" | where TimeGenerated > ago(26h)'
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

module operationalMonitoring 'modules/operationalMonitoring.bicep' = {
  name: 'operational-monitoring'
  dependsOn: [guard, apps]
  params: {
    prefix: prefix
    location: location
    tags: allTags
    workspaceId: monitoring.outputs.workspaceId
    appInsightsId: monitoring.outputs.appInsightsId
    actionGroupId: monitoring.outputs.actionGroupId
    iotHubId: iotHub.outputs.id
    jobNames: deployApplications && deployBackgroundWorkloads ? concat([
      demoDirectIngress ? 'job-${applicationPrefix}-orch' : 'job-${applicationPrefix}-orchestrator'
      ledgerJobName
      demoDirectIngress ? 'job-${applicationPrefix}-load' : 'job-${applicationPrefix}-import'
    ], enableEntraTokenStore ? [
      demoDirectIngress ? 'job-${applicationPrefix}-auth' : 'job-${applicationPrefix}-auth-renewal'
    ] : []) : []
    monthlyBudget: monthlyBudget
    budgetName: budget.name
    enableCandidateAlerts: enableCandidateMonitoringAlerts
    approvalReference: monitoringApprovalReference
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
output keyVaultName string = keyvault.outputs.name
output iotHubName string = iotHub.outputs.name
output iotHubConsumerGroup string = iotHub.outputs.consumerGroup
output iotHubEventHubNamespaceFqdn string = iotHub.outputs.eventHubNamespaceFqdn
output iotHubEventHubName string = iotHub.outputs.eventHubCompatibleName
output iotHubRoutingEnabled bool = iotHub.outputs.routingEnabled
output foundryEndpoint string = foundry.outputs.endpoint
output identityPrincipalIds object = identity.outputs.principalIds
output logAnalyticsWorkspace string = monitoring.outputs.workspaceName
output operationsWorkbookId string = operationalMonitoring.outputs.workbookId
output publicEdgeHostName string = enablePublicEdge ? edge!.outputs.publicHostName : ''
output entraRedirectUri string = enablePublicEdge ? edge!.outputs.entraRedirectUri : ''
