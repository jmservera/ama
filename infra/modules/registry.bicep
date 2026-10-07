param name string
param location string
param tags object
param workspaceId string
param peSubnetId string
param zoneId string
@description('Principals that pull images (workload identities).')
param pullPrincipalIds array
param zoneRedundant bool = false

resource registry 'Microsoft.ContainerRegistry/registries@2025-04-01' = {
  name: name
  location: location
  tags: tags
  sku: { name: 'Premium' }
  properties: {
    adminUserEnabled: false
    anonymousPullEnabled: false
    publicNetworkAccess: 'Disabled'
    networkRuleBypassOptions: 'None'
    zoneRedundancy: zoneRedundant ? 'Enabled' : 'Disabled'
    dataEndpointEnabled: true
    policies: {
      quarantinePolicy: { status: 'enabled' }
      retentionPolicy: { status: 'enabled', days: 30 }
      exportPolicy: { status: 'disabled' }
      azureADAuthenticationAsArmPolicy: { status: 'enabled' }
    }
  }
}

resource pull 'Microsoft.Authorization/roleAssignments@2022-04-01' = [for principalId in pullPrincipalIds: {
  scope: registry
  name: guid(registry.id, principalId, 'acrpull')
  properties: {
    principalId: principalId
    principalType: 'ServicePrincipal'
    roleDefinitionId: subscriptionResourceId('Microsoft.Authorization/roleDefinitions', '7f951dda-4ed3-4680-a7ca-43fe172d538d')
  }
}]

resource diagnostics 'Microsoft.Insights/diagnosticSettings@2021-05-01-preview' = {
  scope: registry
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
    targetResourceId: registry.id
    groupId: 'registry'
    dnsZoneIds: [zoneId]
  }
}

output id string = registry.id
output loginServer string = registry.properties.loginServer
