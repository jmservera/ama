targetScope = 'resourceGroup'

@description('Existing API name in ama. Grants reads/restart only; does not deploy a workload.')
param apiName string
@description('Existing SQL administrator user-assigned identity name, id-<prefix>-init.')
param initializerIdentityName string

module guard './modules/staff-initializer-guard.bicep' = {
  name: 'staff-initializer-scope'
  params: {
    approvedScope: resourceGroup().name == 'ama' && startsWith(initializerIdentityName, 'id-') && endsWith(initializerIdentityName, '-init') ? 'ama' : ''
  }
}

resource api 'Microsoft.App/containerApps@2025-07-01' existing = {
  name: apiName
}
resource initializer 'Microsoft.ManagedIdentity/userAssignedIdentities@2023-01-31' existing = {
  name: initializerIdentityName
}

resource relay 'Microsoft.App/jobs@2025-07-01' existing = {
  name: 'job-${substring(initializerIdentityName, 3)}'
}

resource restartRole 'Microsoft.Authorization/roleDefinitions@2022-04-01' = {
  name: guid(resourceGroup().id, 'staff-initializer-api-restart')
  properties: {
    roleName: 'Staff initializer API restart (${resourceGroup().name})'
    description: 'Read serving revisions/replicas and restart the scoped API; no settings, secrets or Graph access.'
    type: 'CustomRole'
    assignableScopes: [resourceGroup().id]
    permissions: [{
      actions: [
        'Microsoft.App/containerApps/read'
        'Microsoft.App/containerApps/revisions/read'
        'Microsoft.App/containerApps/revisions/replicas/read'
        'Microsoft.App/containerApps/revisions/restart/action'
      ]
      notActions: []
      dataActions: []
      notDataActions: []
    }]
  }
  dependsOn: [guard]
}

resource restartAssignment 'Microsoft.Authorization/roleAssignments@2022-04-01' = {
  scope: api
  name: guid(api.id, initializer.id, restartRole.id)
  properties: {
    roleDefinitionId: restartRole.id
    principalId: initializer.properties.principalId
    principalType: 'ServicePrincipal'
  }
}

resource relayRole 'Microsoft.Authorization/roleDefinitions@2022-04-01' = {
  name: guid(resourceGroup().id, 'staff-initializer-result-tags')
  properties: {
    roleName: 'Staff initializer result tags (${resourceGroup().name})'
    description: 'Read/merge encrypted result tags on the existing initializer only; no job settings, secrets or Graph access.'
    type: 'CustomRole'
    assignableScopes: [resourceGroup().id]
    permissions: [{
      actions: [
        'Microsoft.Resources/tags/read'
        'Microsoft.Resources/tags/write'
      ]
      notActions: []
      dataActions: []
      notDataActions: []
    }]
  }
  dependsOn: [guard]
}

resource relayAssignment 'Microsoft.Authorization/roleAssignments@2022-04-01' = {
  scope: relay
  name: guid(relay.id, initializer.id, relayRole.id)
  properties: {
    roleDefinitionId: relayRole.id
    principalId: initializer.properties.principalId
    principalType: 'ServicePrincipal'
  }
}
