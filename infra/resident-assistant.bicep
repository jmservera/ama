targetScope = 'resourceGroup'

@description('Explicit opt-in. Default off, including production use. Never deploy the resident app or alter ingress.')
param enabled bool = false
@description('Dedicated account in existing RG ama; no keys or local authentication.')
param accountName string = 'aoai-resident-469'
@allowed(['swedencentral'])
param location string = 'swedencentral'
@description('Existing resident application managed identity. No identity is created.')
param residentIdentityName string = 'id-resident-demo'
@allowed(['gpt-4.1-mini'])
param modelName string = 'gpt-4.1-mini'
@allowed(['2025-04-14'])
param modelVersion string = '2025-04-14'
@allowed([1])
param capacity int = 1

var active = enabled && resourceGroup().name == 'ama'

resource residentIdentity 'Microsoft.ManagedIdentity/userAssignedIdentities@2023-01-31' existing = {
  name: residentIdentityName
}

resource account 'Microsoft.CognitiveServices/accounts@2025-06-01' = if (active) {
  name: accountName
  location: location
  kind: 'OpenAI'
  sku: { name: 'S0' }
  tags: { workload: 'resident-assistant', issue: '469', 'zava-forward-synthetic': 'true' }
  properties: {
    customSubDomainName: accountName
    disableLocalAuth: true
    publicNetworkAccess: 'Enabled'
    dynamicThrottlingEnabled: false
  }
}

resource model 'Microsoft.CognitiveServices/accounts/deployments@2025-06-01' = if (active) {
  parent: account
  name: 'resident-mini'
  sku: { name: 'Standard', capacity: capacity }
  properties: {
    model: { format: 'OpenAI', name: modelName, version: modelVersion }
    versionUpgradeOption: 'NoAutoUpgrade'
  }
}

resource inference 'Microsoft.Authorization/roleAssignments@2022-04-01' = if (active) {
  scope: account
  name: guid(accountName, residentIdentityName, 'resident-openai-user')
  properties: {
    roleDefinitionId: subscriptionResourceId('Microsoft.Authorization/roleDefinitions', '5e0bd9bd-7b93-4f28-af87-19fc36ad61bd')
    principalId: residentIdentity.properties.principalId
    principalType: 'ServicePrincipal'
  }
}

output endpoint string = active ? account!.properties.endpoint : ''
output scopeAccepted bool = resourceGroup().name == 'ama'
