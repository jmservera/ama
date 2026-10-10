targetScope = 'resourceGroup'

param accountName string = 'aif-warm-dev-yu44m'
param appName string = 'ca-properwarm-mvp'
param deploymentName string = 'decision'

resource account 'Microsoft.CognitiveServices/accounts@2024-10-01' existing = {
  name: accountName
}

resource app 'Microsoft.App/containerApps@2024-03-01' existing = {
  name: appName
}

resource model 'Microsoft.CognitiveServices/accounts/deployments@2024-10-01' = {
  parent: account
  name: deploymentName
  sku: {
    name: 'GlobalStandard'
    capacity: 1
  }
  properties: {
    model: {
      format: 'Microsoft'
      name: 'Microsoft-Decision-1'
      version: '1'
    }
  }
}

resource role 'Microsoft.Authorization/roleDefinitions@2022-04-01' = {
  name: guid(resourceGroup().id, accountName, 'decision-inference')
  properties: {
    roleName: 'Proper Warm Decision Inference'
    description: 'Call the Microsoft decision provider; no key listing or model administration.'
    type: 'CustomRole'
    permissions: [
      {
        actions: ['Microsoft.CognitiveServices/accounts/read']
        dataActions: ['Microsoft.CognitiveServices/accounts/AIServices/providers/action']
        notActions: []
        notDataActions: []
      }
    ]
    assignableScopes: [resourceGroup().id]
  }
}

resource access 'Microsoft.Authorization/roleAssignments@2022-04-01' = {
  scope: account
  name: guid(account.id, app.id, role.id)
  properties: {
    roleDefinitionId: role.id
    principalId: app.identity.principalId
    principalType: 'ServicePrincipal'
  }
}

output deployment string = model.name
