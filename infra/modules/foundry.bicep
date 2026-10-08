param name string
param projectName string
param location string
param tags object
param workspaceId string
param peSubnetId string
param zoneIds object
@description('Principals that may invoke models and agents (the agent runner identity only).')
param userPrincipalIds array
@description('Model deployments. Two tiers support the PRD rule to select the smallest model that meets task thresholds.')
param deployments array

resource account 'Microsoft.CognitiveServices/accounts@2025-06-01' = {
  name: name
  location: location
  tags: tags
  kind: 'AIServices'
  sku: { name: 'S0' }
  identity: { type: 'SystemAssigned' }
  properties: {
    customSubDomainName: name
    allowProjectManagement: true
    disableLocalAuth: true
    publicNetworkAccess: 'Disabled'
    networkAcls: {
      defaultAction: 'Deny'
      bypass: 'None'
    }
  }
}

resource project 'Microsoft.CognitiveServices/accounts/projects@2025-06-01' = {
  parent: account
  name: projectName
  location: location
  tags: tags
  identity: { type: 'SystemAssigned' }
  properties: {
    displayName: projectName
    description: 'Proper Warm retrofit demonstrator bounded agents'
  }
}

@batchSize(1)
resource models 'Microsoft.CognitiveServices/accounts/deployments@2025-06-01' = [for model in deployments: {
  parent: account
  dependsOn: [project]
  name: model.name
  sku: {
    name: model.skuName
    capacity: model.capacity
  }
  properties: {
    model: {
      format: 'OpenAI'
      name: model.model
      version: model.version
    }
    versionUpgradeOption: 'NoAutoUpgrade'
    raiPolicyName: 'Microsoft.DefaultV2'
  }
}]

resource openAiUser 'Microsoft.Authorization/roleAssignments@2022-04-01' = [for principalId in userPrincipalIds: {
  scope: account
  name: guid(account.id, principalId, 'openai-user')
  properties: {
    principalId: principalId
    principalType: 'ServicePrincipal'
    roleDefinitionId: subscriptionResourceId('Microsoft.Authorization/roleDefinitions', '5e0bd9bd-7b93-4f28-af87-19fc36ad61bd')
  }
}]

resource aiUser 'Microsoft.Authorization/roleAssignments@2022-04-01' = [for principalId in userPrincipalIds: {
  scope: account
  name: guid(account.id, principalId, 'azure-ai-user')
  properties: {
    principalId: principalId
    principalType: 'ServicePrincipal'
    roleDefinitionId: subscriptionResourceId('Microsoft.Authorization/roleDefinitions', '53ca6127-db72-4b80-b1b0-d745d6d5456d')
  }
}]

resource diagnostics 'Microsoft.Insights/diagnosticSettings@2021-05-01-preview' = {
  scope: account
  name: 'to-log-analytics'
  properties: {
    workspaceId: workspaceId
    logs: [{ categoryGroup: 'allLogs', enabled: true }]
    metrics: [{ category: 'AllMetrics', enabled: true }]
  }
}

module endpoint 'privateEndpoint.bicep' = {
  name: 'pe-${name}'
  params: {
    name: name
    location: location
    tags: tags
    subnetId: peSubnetId
    targetResourceId: account.id
    groupId: 'account'
    dnsZoneIds: [zoneIds.cognitive, zoneIds.openai, zoneIds.aiServices]
  }
  dependsOn: [models]
}

output id string = account.id
output endpoint string = account.properties.endpoint
output projectName string = project.name
