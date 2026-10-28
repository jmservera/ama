param name string
param projectName string
param location string
param tags object
param workspaceId string
param peSubnetId string
param zoneIds object
@description('Principals that may invoke models and agents. Agent runner by default; the MVP API is included only when enableApiAi is explicitly set.')
param userPrincipalIds array
@description('Nonempty model deployments. One model can back both logical tiers; two or more use the first two in order. Task quality and activation remain separately gated.')
@minLength(1)
param deployments array
@description('Development only. Allows connectivity from external networks in addition to the private endpoints.')
param allowPublicNetworkAccess bool = false

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
    publicNetworkAccess: allowPublicNetworkAccess ? 'Enabled' : 'Disabled'
    networkAcls: {
      defaultAction: allowPublicNetworkAccess ? 'Allow' : 'Deny'
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
    description: 'Zava Forward retrofit demonstrator bounded agents'
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
output openAiEndpoint string = account.properties.endpoints['OpenAI Language Model Instance API']
output modelDeploymentNames object = {
  standard: deployments[0].name
  capable: deployments[length(deployments) > 1 ? 1 : 0].name
}
output modelVersions object = {
  standard: '${deployments[0].model}-${deployments[0].version}'
  capable: '${deployments[length(deployments) > 1 ? 1 : 0].model}-${deployments[length(deployments) > 1 ? 1 : 0].version}'
}
output projectName string = project.name
