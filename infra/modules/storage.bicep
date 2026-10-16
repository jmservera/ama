param name string
param location string
param tags object
param workspaceId string
param peSubnetId string
param zoneIds object
param enableLock bool
@description('Days audit archive blobs stay immutable (time-based retention, unlocked until the owner locks the policy).')
@minValue(1)
param auditImmutabilityDays int = 365
@description('Days ledger digests stay immutable. Must be no shorter than the legal audit retention period (open owner decision). The policy is created unlocked; locking is irreversible and is done by the owner.')
@minValue(1)
param ledgerDigestImmutabilityDays int = 365
@description('Array of { principalId, roleDefinitionId, scope } where scope is blob or queue.')
param roleAssignments array
param zoneRedundant bool = false
@description('Development only. Allows connectivity from external networks in addition to the private endpoints.')
param allowPublicNetworkAccess bool = false

resource account 'Microsoft.Storage/storageAccounts@2024-01-01' = {
  name: name
  location: location
  tags: tags
  sku: { name: zoneRedundant ? 'Standard_ZRS' : 'Standard_LRS' }
  kind: 'StorageV2'
  properties: {
    allowBlobPublicAccess: false
    allowSharedKeyAccess: false
    defaultToOAuthAuthentication: true
    minimumTlsVersion: 'TLS1_2'
    supportsHttpsTrafficOnly: true
    publicNetworkAccess: allowPublicNetworkAccess ? 'Enabled' : 'Disabled'
    networkAcls: {
      defaultAction: allowPublicNetworkAccess ? 'Allow' : 'Deny'
      bypass: 'None'
    }
    encryption: {
      requireInfrastructureEncryption: true
      keySource: 'Microsoft.Storage'
      services: {
        blob: { enabled: true }
        queue: { enabled: true, keyType: 'Account' }
      }
    }
  }
}

resource blobService 'Microsoft.Storage/storageAccounts/blobServices@2024-01-01' = {
  parent: account
  name: 'default'
  properties: {
    isVersioningEnabled: true
    deleteRetentionPolicy: { enabled: true, days: 30 }
    containerDeleteRetentionPolicy: { enabled: true, days: 30 }
  }
}

var containers = ['evidence', 'imports', 'quarantine', 'exports', 'audit-archive', 'ledger-digests']

resource blobContainers 'Microsoft.Storage/storageAccounts/blobServices/containers@2024-01-01' = [for container in containers: {
  parent: blobService
  name: container
  properties: { publicAccess: 'None' }
}]

resource auditRetention 'Microsoft.Storage/storageAccounts/blobServices/containers/immutabilityPolicies@2024-01-01' = {
  parent: blobContainers[4]
  name: 'default'
  properties: {
    immutabilityPeriodSinceCreationInDays: auditImmutabilityDays
    allowProtectedAppendWrites: true
  }
}

resource digestRetention 'Microsoft.Storage/storageAccounts/blobServices/containers/immutabilityPolicies@2024-01-01' = {
  parent: blobContainers[5]
  name: 'default'
  properties: {
    immutabilityPeriodSinceCreationInDays: ledgerDigestImmutabilityDays
    allowProtectedAppendWrites: false
  }
}

resource queueService 'Microsoft.Storage/storageAccounts/queueServices@2024-01-01' = {
  parent: account
  name: 'default'
}

var queues = ['agent-tasks', 'agent-tasks-poison', 'import-jobs', 'import-jobs-poison']

resource taskQueues 'Microsoft.Storage/storageAccounts/queueServices/queues@2024-01-01' = [for queue in queues: {
  parent: queueService
  name: queue
}]

resource roles 'Microsoft.Authorization/roleAssignments@2022-04-01' = [for assignment in roleAssignments: {
  scope: account
  name: guid(account.id, assignment.principalId, assignment.roleDefinitionId)
  properties: {
    principalId: assignment.principalId
    principalType: 'ServicePrincipal'
    roleDefinitionId: subscriptionResourceId('Microsoft.Authorization/roleDefinitions', assignment.roleDefinitionId)
  }
}]

resource blobDiagnostics 'Microsoft.Insights/diagnosticSettings@2021-05-01-preview' = {
  scope: blobService
  name: 'to-log-analytics'
  properties: {
    workspaceId: workspaceId
    logs: [{ categoryGroup: 'audit', enabled: true }]
    metrics: [{ category: 'Transaction', enabled: true }]
  }
}

resource queueDiagnostics 'Microsoft.Insights/diagnosticSettings@2021-05-01-preview' = {
  scope: queueService
  name: 'to-log-analytics'
  properties: {
    workspaceId: workspaceId
    logs: [{ categoryGroup: 'audit', enabled: true }]
    metrics: [{ category: 'Transaction', enabled: true }]
  }
}

resource lock 'Microsoft.Authorization/locks@2020-05-01' = if (enableLock) {
  scope: account
  name: 'do-not-delete'
  properties: { level: 'CanNotDelete' }
}

module blobEndpoint 'privateEndpoint.bicep' = {
  name: 'pe-${name}-blob'
  params: {
    name: '${name}-blob'
    location: location
    tags: tags
    subnetId: peSubnetId
    targetResourceId: account.id
    groupId: 'blob'
    dnsZoneIds: [zoneIds.blob]
  }
}

module queueEndpoint 'privateEndpoint.bicep' = {
  name: 'pe-${name}-queue'
  params: {
    name: '${name}-queue'
    location: location
    tags: tags
    subnetId: peSubnetId
    targetResourceId: account.id
    groupId: 'queue'
    dnsZoneIds: [zoneIds.queue]
  }
}

output id string = account.id
output name string = account.name
