param name string
param location string
param tags object
param subnetId string
param targetResourceId string
@description('Private link sub-resource, for example sqlServer, blob, queue, vault, registry, account, azuremonitor.')
param groupId string
param dnsZoneIds array

resource endpoint 'Microsoft.Network/privateEndpoints@2024-05-01' = {
  name: 'pe-${name}'
  location: location
  tags: tags
  properties: {
    subnet: { id: subnetId }
    privateLinkServiceConnections: [
      {
        name: name
        properties: {
          privateLinkServiceId: targetResourceId
          groupIds: [groupId]
        }
      }
    ]
  }
}

resource dns 'Microsoft.Network/privateEndpoints/privateDnsZoneGroups@2024-05-01' = {
  parent: endpoint
  name: 'default'
  properties: {
    privateDnsZoneConfigs: [for (zoneId, i) in dnsZoneIds: {
      name: 'zone${i}'
      properties: { privateDnsZoneId: zoneId }
    }]
  }
}
