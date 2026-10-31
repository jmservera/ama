targetScope = 'resourceGroup'

@description('Existing API name in ama. Grants reads/restart only; does not deploy a workload.')
param apiName string
@description('Existing SQL administrator user-assigned identity name, id-<prefix>-init.')
param initializerIdentityName string

@description('Existing private storage account that holds the staff-results container.')
param storageAccountName string = ''
@description('Include the container-scoped result-write grant only with separate explicit approval. False (default) deploys API read/restart grants only.')
param includeResultBlob bool = false

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

resource storage 'Microsoft.Storage/storageAccounts@2024-01-01' existing = if (includeResultBlob) {
  name: storageAccountName
}
resource blobService 'Microsoft.Storage/storageAccounts/blobServices@2024-01-01' existing = if (includeResultBlob) {
  parent: storage
  name: 'default'
}
resource resultContainer 'Microsoft.Storage/storageAccounts/blobServices/containers@2024-01-01' existing = if (includeResultBlob) {
  parent: blobService
  name: 'staff-results'
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

resource resultRole 'Microsoft.Authorization/roleDefinitions@2022-04-01' = if (includeResultBlob) {
  name: guid(resourceGroup().id, 'staff-initializer-result-blob-write')
  properties: {
    roleName: 'Staff initializer result write (${resourceGroup().name})'
    description: 'Create result blobs in one private container; no read, list, delete, overwrite of other scopes, keys, SAS or Graph access.'
    type: 'CustomRole'
    assignableScopes: [resourceGroup().id]
    permissions: [{
      actions: []
      notActions: []
      dataActions: [
        'Microsoft.Storage/storageAccounts/blobServices/containers/blobs/write'
        'Microsoft.Storage/storageAccounts/blobServices/containers/blobs/add/action'
      ]
      notDataActions: []
    }]
  }
  dependsOn: [guard]
}

resource resultAssignment 'Microsoft.Authorization/roleAssignments@2022-04-01' = if (includeResultBlob) {
  scope: resultContainer
  name: guid(resultContainer.id, initializer.id, resultRole.id)
  properties: {
    roleDefinitionId: resultRole.id
    principalId: initializer.properties.principalId
    principalType: 'ServicePrincipal'
  }
}
