param prefix string
param location string
param tags object
param retentionInDays int = 90
param alertEmail string
@description('Optional Teams Workflows webhook URL for operations alerts.')
@secure()
param teamsWebhookUrl string = ''
param peSubnetId string
param zoneIds object

resource workspace 'Microsoft.OperationalInsights/workspaces@2023-09-01' = {
  name: 'log-${prefix}'
  location: location
  tags: tags
  properties: {
    sku: { name: 'PerGB2018' }
    retentionInDays: retentionInDays
    features: {
      disableLocalAuth: true
      enableLogAccessUsingOnlyResourcePermissions: true
    }
    publicNetworkAccessForIngestion: 'Disabled'
    publicNetworkAccessForQuery: 'Disabled'
  }
}

resource appInsights 'Microsoft.Insights/components@2020-02-02' = {
  name: 'appi-${prefix}'
  location: location
  tags: tags
  kind: 'web'
  properties: {
    Application_Type: 'web'
    WorkspaceResourceId: workspace.id
    DisableLocalAuth: true
    publicNetworkAccessForIngestion: 'Disabled'
    publicNetworkAccessForQuery: 'Disabled'
  }
}

resource scope 'microsoft.insights/privateLinkScopes@2021-07-01-preview' = {
  name: 'ampls-${prefix}'
  location: 'global'
  tags: tags
  properties: {
    accessModeSettings: {
      ingestionAccessMode: 'PrivateOnly'
      queryAccessMode: 'PrivateOnly'
    }
  }
}

resource scopedWorkspace 'microsoft.insights/privateLinkScopes/scopedResources@2021-07-01-preview' = {
  parent: scope
  name: 'scoped-law'
  properties: { linkedResourceId: workspace.id }
}

resource scopedInsights 'microsoft.insights/privateLinkScopes/scopedResources@2021-07-01-preview' = {
  parent: scope
  name: 'scoped-appi'
  properties: { linkedResourceId: appInsights.id }
  dependsOn: [scopedWorkspace]
}

module endpoint 'privateEndpoint.bicep' = {
  name: 'pe-ampls'
  params: {
    name: 'ampls-${prefix}'
    location: location
    tags: tags
    subnetId: peSubnetId
    targetResourceId: scope.id
    groupId: 'azuremonitor'
    dnsZoneIds: [zoneIds.monitor, zoneIds.oms, zoneIds.ods, zoneIds.agentsvc, zoneIds.blob]
  }
  dependsOn: [scopedInsights]
}

resource actionGroup 'Microsoft.Insights/actionGroups@2023-01-01' = {
  name: 'ag-${prefix}-ops'
  location: 'global'
  tags: tags
  properties: {
    groupShortName: 'ama-ops'
    enabled: true
    emailReceivers: [
      {
        name: 'operations'
        emailAddress: alertEmail
        useCommonAlertSchema: true
      }
    ]
    webhookReceivers: empty(teamsWebhookUrl) ? [] : [
      {
        name: 'teams-operations'
        serviceUri: teamsWebhookUrl
        useCommonAlertSchema: true
      }
    ]
  }
}

output workspaceId string = workspace.id
output workspaceName string = workspace.name
output appInsightsId string = appInsights.id
output appInsightsConnectionString string = appInsights.properties.ConnectionString
output actionGroupId string = actionGroup.id
