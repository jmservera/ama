targetScope = 'resourceGroup'

param location string = resourceGroup().location
param accountName string
param deploymentName string = 'case-review'
param modelName string = 'gpt-4.1-mini'
param modelVersion string = '2025-04-14'
@minValue(1)
param capacity int = 10
param principalId string
@allowed(['User', 'ServicePrincipal'])
param principalType string = 'ServicePrincipal'
param allowFirewallAccess bool = false
param allowedIps array = []

resource account 'Microsoft.CognitiveServices/accounts@2025-06-01' = {
  name: accountName
  location: location
  kind: 'OpenAI'
  sku: {
    name: 'S0'
  }
  properties: {
    customSubDomainName: accountName
    disableLocalAuth: true
    publicNetworkAccess: allowFirewallAccess ? 'Enabled' : 'Disabled'
    networkAcls: {
      defaultAction: 'Deny'
      bypass: 'None'
      ipRules: [for ip in allowedIps: {
        value: ip
      }]
    }
  }
  tags: {
    purpose: 'proper-warm-synthetic-demo'
    environment: 'non-production'
  }
}

resource model 'Microsoft.CognitiveServices/accounts/deployments@2025-06-01' = {
  parent: account
  name: deploymentName
  sku: {
    name: 'GlobalStandard'
    capacity: capacity
  }
  properties: {
    model: {
      format: 'OpenAI'
      name: modelName
      version: modelVersion
    }
    versionUpgradeOption: 'NoAutoUpgrade'
  }
}

var openAiUserRole = subscriptionResourceId('Microsoft.Authorization/roleDefinitions', '5e0bd9bd-7b93-4f28-af87-19fc36ad61bd')
resource inferenceRole 'Microsoft.Authorization/roleAssignments@2022-04-01' = {
  name: guid(account.id, principalId, openAiUserRole)
  scope: account
  properties: {
    roleDefinitionId: openAiUserRole
    principalId: principalId
    principalType: principalType
  }
}

output accountId string = account.id
output endpoint string = account.properties.endpoint
output deploymentName string = model.name
output modelVersion string = modelVersion
