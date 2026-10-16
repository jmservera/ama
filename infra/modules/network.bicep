param prefix string
param location string
param tags object
param vnetAddressPrefix string = '10.40.0.0/16'
param acaSubnetPrefix string = '10.40.0.0/23'
param privateEndpointSubnetPrefix string = '10.40.4.0/24'
param demoDirectIngress bool = false
param demoAcaSubnetPrefix string = '10.40.6.0/23'

var dnsZones = [
  'privatelink${environment().suffixes.sqlServerHostname}'
  'privatelink.blob.${environment().suffixes.storage}'
  'privatelink.queue.${environment().suffixes.storage}'
  'privatelink.vaultcore.azure.net'
  'privatelink${environment().suffixes.acrLoginServer}'
  'privatelink.cognitiveservices.azure.com'
  'privatelink.openai.azure.com'
  'privatelink.services.ai.azure.com'
  'privatelink.monitor.azure.com'
  'privatelink.oms.opinsights.azure.com'
  'privatelink.ods.opinsights.azure.com'
  'privatelink.agentsvc.azure-automation.net'
  'privatelink.azure-devices.net'
  'privatelink.servicebus.windows.net'
]

resource peNsg 'Microsoft.Network/networkSecurityGroups@2024-05-01' = {
  name: 'nsg-${prefix}-pe'
  location: location
  tags: tags
  properties: {
    securityRules: [
      {
        name: 'allow-vnet-https-in'
        properties: {
          priority: 100
          direction: 'Inbound'
          access: 'Allow'
          protocol: 'Tcp'
          sourceAddressPrefix: 'VirtualNetwork'
          sourcePortRange: '*'
          destinationAddressPrefix: '*'
          destinationPortRanges: ['443', '1433']
        }
      }
      {
        name: 'deny-all-in'
        properties: {
          priority: 4000
          direction: 'Inbound'
          access: 'Deny'
          protocol: '*'
          sourceAddressPrefix: '*'
          sourcePortRange: '*'
          destinationAddressPrefix: '*'
          destinationPortRange: '*'
        }
      }
    ]
  }
}

resource acaNsg 'Microsoft.Network/networkSecurityGroups@2024-05-01' = {
  name: 'nsg-${prefix}-aca'
  location: location
  tags: tags
  properties: {
    securityRules: [
      {
        name: 'allow-afd-backend-in'
        properties: {
          priority: 100
          direction: 'Inbound'
          access: 'Allow'
          protocol: 'Tcp'
          sourceAddressPrefix: 'AzureFrontDoor.Backend'
          sourcePortRange: '*'
          destinationAddressPrefix: '*'
          destinationPortRange: '443'
        }
      }
      {
        name: 'allow-vnet-in'
        properties: {
          priority: 200
          direction: 'Inbound'
          access: 'Allow'
          protocol: '*'
          sourceAddressPrefix: 'VirtualNetwork'
          sourcePortRange: '*'
          destinationAddressPrefix: '*'
          destinationPortRange: '*'
        }
      }
    ]
  }
}

resource demoAcaNsg 'Microsoft.Network/networkSecurityGroups@2024-05-01' = if (demoDirectIngress) {
  name: 'nsg-${prefix}-aca-demo'
  location: location
  tags: tags
  properties: {
    securityRules: [
      {
        name: 'allow-internet-https-in'
        properties: {
          priority: 100
          direction: 'Inbound'
          access: 'Allow'
          protocol: 'Tcp'
          sourceAddressPrefix: 'Internet'
          sourcePortRange: '*'
          destinationAddressPrefix: '*'
          destinationPortRange: '443'
        }
      }
      {
        name: 'allow-vnet-in'
        properties: {
          priority: 200
          direction: 'Inbound'
          access: 'Allow'
          protocol: '*'
          sourceAddressPrefix: 'VirtualNetwork'
          sourcePortRange: '*'
          destinationAddressPrefix: '*'
          destinationPortRange: '*'
        }
      }
    ]
  }
}

resource vnet 'Microsoft.Network/virtualNetworks@2024-05-01' = {
  name: 'vnet-${prefix}'
  location: location
  tags: tags
  properties: {
    addressSpace: { addressPrefixes: [vnetAddressPrefix] }
    subnets: concat([
      {
        name: 'snet-aca'
        properties: {
          addressPrefix: acaSubnetPrefix
          networkSecurityGroup: { id: acaNsg.id }
          delegations: [
            {
              name: 'aca'
              properties: { serviceName: 'Microsoft.App/environments' }
            }
          ]
        }
      }
      {
        name: 'snet-pe'
        properties: {
          addressPrefix: privateEndpointSubnetPrefix
          networkSecurityGroup: { id: peNsg.id }
          privateEndpointNetworkPolicies: 'Enabled'
        }
      }
    ], demoDirectIngress ? [
      {
        name: 'snet-aca-demo'
        properties: {
          addressPrefix: demoAcaSubnetPrefix
          networkSecurityGroup: { id: demoAcaNsg!.id }
          delegations: [
            {
              name: 'aca-demo'
              properties: { serviceName: 'Microsoft.App/environments' }
            }
          ]
        }
      }
    ] : [])
  }
}

resource zones 'Microsoft.Network/privateDnsZones@2020-06-01' = [for zone in dnsZones: {
  name: zone
  location: 'global'
  tags: tags
}]

resource links 'Microsoft.Network/privateDnsZones/virtualNetworkLinks@2020-06-01' = [for (zone, i) in dnsZones: {
  parent: zones[i]
  name: 'link-${prefix}'
  location: 'global'
  properties: {
    virtualNetwork: { id: vnet.id }
    registrationEnabled: false
  }
}]

output vnetId string = vnet.id
output vnetName string = vnet.name
output acaSubnetId string = vnet.properties.subnets[0].id
output peSubnetId string = vnet.properties.subnets[1].id
output demoAcaSubnetId string = demoDirectIngress ? resourceId('Microsoft.Network/virtualNetworks/subnets', vnet.name, 'snet-aca-demo') : ''
output zoneIds object = {
  sql: zones[0].id
  blob: zones[1].id
  queue: zones[2].id
  vault: zones[3].id
  acr: zones[4].id
  cognitive: zones[5].id
  openai: zones[6].id
  aiServices: zones[7].id
  monitor: zones[8].id
  oms: zones[9].id
  ods: zones[10].id
  agentsvc: zones[11].id
  iotHub: zones[12].id
  iotHubEndpoint: zones[13].id
}
