param name string
param location string
param tags object
param workspaceId string
param peSubnetId string
param zoneId string
param secretsUserPrincipalIds array
param enableLock bool
@description('Development only. Allows connectivity from external networks in addition to the private endpoints.')
param allowPublicNetworkAccess bool = false
@description('Development only. False allows a 7 day soft delete and purge so disposable environments can reuse names. Once enabled on a vault, purge protection cannot be turned off.')
param purgeProtection bool = true

resource vault 'Microsoft.KeyVault/vaults@2024-11-01' = {
  name: name
  location: location
  tags: tags
  properties: {
    tenantId: tenant().tenantId
    sku: { family: 'A', name: 'standard' }
    enableRbacAuthorization: true
    enableSoftDelete: true
    softDeleteRetentionInDays: purgeProtection ? 90 : 7
    enablePurgeProtection: purgeProtection ? true : null
    publicNetworkAccess: allowPublicNetworkAccess ? 'Enabled' : 'Disabled'
    networkAcls: {
      defaultAction: allowPublicNetworkAccess ? 'Allow' : 'Deny'
      bypass: 'None'
    }
  }
}

resource secretsUser 'Microsoft.Authorization/roleAssignments@2022-04-01' = [for principalId in secretsUserPrincipalIds: {
  scope: vault
  name: guid(vault.id, principalId, 'kv-secrets-user')
  properties: {
    principalId: principalId
    principalType: 'ServicePrincipal'
    roleDefinitionId: subscriptionResourceId('Microsoft.Authorization/roleDefinitions', '4633458b-17de-408a-b874-0445c86b69e6')
  }
}]

resource diagnostics 'Microsoft.Insights/diagnosticSettings@2021-05-01-preview' = {
  scope: vault
  name: 'to-log-analytics'
  properties: {
    workspaceId: workspaceId
    logs: [{ categoryGroup: 'allLogs', enabled: true }]
    metrics: [{ category: 'AllMetrics', enabled: true }]
  }
}

resource lock 'Microsoft.Authorization/locks@2020-05-01' = if (enableLock) {
  scope: vault
  name: 'do-not-delete'
  properties: { level: 'CanNotDelete' }
}

module endpoint 'privateEndpoint.bicep' = {
  name: 'pe-${name}'
  params: {
    name: name
    location: location
    tags: tags
    subnetId: peSubnetId
    targetResourceId: vault.id
    groupId: 'vault'
    dnsZoneIds: [zoneId]
  }
}

output id string = vault.id
output name string = vault.name
