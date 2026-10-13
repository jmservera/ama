param name string
param prefix string
param location string
param tags object
param workspaceId string
param peSubnetId string
param blobZoneId string
param keyVaultName string
param registryName string
param allowPublicNetworkAccess bool = false
param zoneRedundant bool = false

var authTags = union(tags, { dataClassification: 'authentication-secrets', workload: 'entra-token-store' })

resource maintenance 'Microsoft.ManagedIdentity/userAssignedIdentities@2024-11-30' = {
  name: 'id-${prefix}-auth-maintenance'
  location: location
  tags: authTags
}

resource account 'Microsoft.Storage/storageAccounts@2024-01-01' = {
  name: name
  location: location
  tags: authTags
  kind: 'StorageV2'
  sku: { name: zoneRedundant ? 'Standard_ZRS' : 'Standard_LRS' }
  properties: {
    allowBlobPublicAccess: false
    allowSharedKeyAccess: false
    defaultToOAuthAuthentication: true
    minimumTlsVersion: 'TLS1_2'
    supportsHttpsTrafficOnly: true
    publicNetworkAccess: allowPublicNetworkAccess ? 'Enabled' : 'Disabled'
    networkAcls: { defaultAction: allowPublicNetworkAccess ? 'Allow' : 'Deny', bypass: 'None' }
    encryption: {
      requireInfrastructureEncryption: true
      keySource: 'Microsoft.Storage'
      services: { blob: { enabled: true } }
    }
  }
}

resource blobs 'Microsoft.Storage/storageAccounts/blobServices@2024-01-01' = {
  parent: account
  name: 'default'
  properties: {
    isVersioningEnabled: false
    deleteRetentionPolicy: { enabled: false }
  }
}

resource tokens 'Microsoft.Storage/storageAccounts/blobServices/containers@2024-01-01' = {
  parent: blobs
  name: 'auth-tokens'
  properties: { publicAccess: 'None' }
}

resource delegator 'Microsoft.Authorization/roleAssignments@2022-04-01' = {
  scope: account
  name: guid(account.id, maintenance.id, 'delegator')
  properties: {
    principalId: maintenance.properties.principalId
    principalType: 'ServicePrincipal'
    roleDefinitionId: subscriptionResourceId('Microsoft.Authorization/roleDefinitions', 'db58b8e5-c6ad-4a2a-8342-4190687cbf4a')
  }
}

resource tokenContributor 'Microsoft.Authorization/roleAssignments@2022-04-01' = {
  scope: tokens
  name: guid(tokens.id, maintenance.id, 'contributor')
  properties: {
    principalId: maintenance.properties.principalId
    principalType: 'ServicePrincipal'
    roleDefinitionId: subscriptionResourceId('Microsoft.Authorization/roleDefinitions', 'ba92f5b4-2d11-453d-a403-e96b0029c9fe')
  }
}

resource vault 'Microsoft.KeyVault/vaults@2024-11-01' existing = { name: keyVaultName }
resource secret 'Microsoft.KeyVault/vaults/secrets@2024-11-01' existing = { parent: vault, name: 'entra-token-store-sas' }
resource secretWriter 'Microsoft.Authorization/roleAssignments@2022-04-01' = {
  scope: secret
  name: guid(secret.id, maintenance.id, 'secrets-officer')
  properties: {
    principalId: maintenance.properties.principalId
    principalType: 'ServicePrincipal'
    roleDefinitionId: subscriptionResourceId('Microsoft.Authorization/roleDefinitions', 'b86a8fe4-44ce-4948-aee5-eccb2c155cd7')
  }
}

resource registry 'Microsoft.ContainerRegistry/registries@2025-04-01' existing = { name: registryName }
resource pull 'Microsoft.Authorization/roleAssignments@2022-04-01' = {
  scope: registry
  name: guid(registry.id, maintenance.id, 'acr-pull')
  properties: {
    principalId: maintenance.properties.principalId
    principalType: 'ServicePrincipal'
    roleDefinitionId: subscriptionResourceId('Microsoft.Authorization/roleDefinitions', '7f951dda-4ed3-4680-a7ca-43fe172d538d')
  }
}

resource diagnostics 'Microsoft.Insights/diagnosticSettings@2021-05-01-preview' = {
  scope: blobs
  name: 'to-log-analytics'
  properties: {
    workspaceId: workspaceId
    logs: [{ categoryGroup: 'audit', enabled: true }]
    metrics: [{ category: 'Transaction', enabled: true }]
  }
}

module endpoint 'privateEndpoint.bicep' = {
  name: 'pe-${name}-blob'
  params: {
    name: '${name}-blob'
    location: location
    tags: authTags
    subnetId: peSubnetId
    targetResourceId: account.id
    groupId: 'blob'
    dnsZoneIds: [blobZoneId]
  }
}

output accountName string = account.name
output identityId string = maintenance.id
output identityClientId string = maintenance.properties.clientId
