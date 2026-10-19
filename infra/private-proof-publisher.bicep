targetScope = 'resourceGroup'

@description('Exact existing ama resource group ID, verified by the operator before preview and apply.')
param expectedResourceGroupId string

@description('Ephemeral operator SSH public key; no inbound SSH is allowed.')
param sshPublicKey string

@description('Absolute UTC cleanup deadline, at most two hours after allocation.')
param expiresAt string

@allowed(['uksouth'])
param location string = 'uksouth'

@minLength(1)
@maxLength(30)
param adminUsername string

var stem = 'issue360-publisher-20261019'
var ownership = {
  'zava-forward-owner': stem
  'zava-forward-expires': expiresAt
  'zava-forward-purpose': 'temporary-private-proof-publisher'
}

module guard 'modules/staff-initializer-guard.bicep' = {
  name: '${stem}-guard'
  params: {
    approvedScope: resourceGroup().name == 'ama' && toLower(resourceGroup().id) == toLower(expectedResourceGroupId)
      ? resourceGroup().id
      : ''
  }
}

resource vnet 'Microsoft.Network/virtualNetworks@2024-05-01' existing = {
  name: 'vnet-cutover-test'
}

resource nsg 'Microsoft.Network/networkSecurityGroups@2024-05-01' = {
  name: '${stem}-nsg'
  location: location
  tags: ownership
  dependsOn: [guard]
  properties: {
    securityRules: [
      {
        name: 'deny-all-inbound'
        properties: {
          priority: 100
          direction: 'Inbound'
          access: 'Deny'
          protocol: '*'
          sourceAddressPrefix: '*'
          sourcePortRange: '*'
          destinationAddressPrefix: '*'
          destinationPortRange: '*'
        }
      }
      {
        name: 'allow-private-acr-https'
        properties: {
          priority: 100
          direction: 'Outbound'
          access: 'Allow'
          protocol: 'Tcp'
          sourceAddressPrefix: '10.40.8.0/28'
          sourcePortRange: '*'
          destinationAddressPrefixes: ['10.40.4.20/32', '10.40.4.21/32']
          destinationPortRange: '443'
        }
      }
      {
        name: 'allow-platform-dns-tcp'
        properties: {
          priority: 110
          direction: 'Outbound'
          access: 'Allow'
          protocol: 'Tcp'
          sourceAddressPrefix: '10.40.8.0/28'
          sourcePortRange: '*'
          destinationAddressPrefix: 'AzurePlatformDNS'
          destinationPortRange: '53'
        }
      }
      {
        name: 'allow-platform-dns-udp'
        properties: {
          priority: 120
          direction: 'Outbound'
          access: 'Allow'
          protocol: 'Udp'
          sourceAddressPrefix: '10.40.8.0/28'
          sourcePortRange: '*'
          destinationAddressPrefix: 'AzurePlatformDNS'
          destinationPortRange: '53'
        }
      }
      {
        name: 'allow-wireserver-agent'
        properties: {
          priority: 130
          direction: 'Outbound'
          access: 'Allow'
          protocol: 'Tcp'
          sourceAddressPrefix: '10.40.8.0/28'
          sourcePortRange: '*'
          destinationAddressPrefix: '168.63.129.16/32'
          destinationPortRanges: ['80', '32526']
        }
      }
      {
        name: 'allow-platform-imds-http'
        properties: {
          priority: 140
          direction: 'Outbound'
          access: 'Allow'
          protocol: 'Tcp'
          sourceAddressPrefix: '10.40.8.0/28'
          sourcePortRange: '*'
          destinationAddressPrefix: 'AzurePlatformIMDS'
          destinationPortRange: '80'
        }
      }
      {
        name: 'deny-other-platform-dns'
        properties: {
          priority: 150
          direction: 'Outbound'
          access: 'Deny'
          protocol: '*'
          sourceAddressPrefix: '*'
          sourcePortRange: '*'
          destinationAddressPrefix: 'AzurePlatformDNS'
          destinationPortRange: '*'
        }
      }
      {
        name: 'deny-other-platform-imds'
        properties: {
          priority: 160
          direction: 'Outbound'
          access: 'Deny'
          protocol: '*'
          sourceAddressPrefix: '*'
          sourcePortRange: '*'
          destinationAddressPrefix: 'AzurePlatformIMDS'
          destinationPortRange: '*'
        }
      }
      {
        name: 'deny-all-outbound'
        properties: {
          priority: 200
          direction: 'Outbound'
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

resource subnet 'Microsoft.Network/virtualNetworks/subnets@2024-05-01' = {
  parent: vnet
  name: '${stem}-subnet'
  properties: {
    addressPrefix: '10.40.8.0/28'
    defaultOutboundAccess: false
    networkSecurityGroup: {id: nsg.id}
  }
}

resource publicIp 'Microsoft.Network/publicIPAddresses@2024-05-01' = {
  name: '${stem}-ip'
  location: location
  tags: ownership
  dependsOn: [guard]
  sku: {name: 'Standard'}
  properties: {publicIPAllocationMethod: 'Static'}
}

resource nic 'Microsoft.Network/networkInterfaces@2024-05-01' = {
  name: '${stem}-nic'
  location: location
  tags: ownership
  properties: {
    enableIPForwarding: false
    ipConfigurations: [
      {
        name: 'publisher'
        properties: {
          privateIPAllocationMethod: 'Dynamic'
          subnet: {id: subnet.id}
          publicIPAddress: {id: publicIp.id}
        }
      }
    ]
  }
}

resource publisher 'Microsoft.Compute/virtualMachines@2024-07-01' = {
  name: stem
  location: location
  tags: ownership
  identity: {type: 'SystemAssigned'}
  properties: {
    hardwareProfile: {vmSize: 'Standard_D2as_v5'}
    storageProfile: {
      imageReference: {
        publisher: 'Canonical'
        offer: '0001-com-ubuntu-server-jammy'
        sku: '22_04-lts-gen2'
        version: '22.04.202610170'
      }
      osDisk: {
        name: '${stem}-os'
        createOption: 'FromImage'
        diskSizeGB: 32
        deleteOption: 'Delete'
        managedDisk: {storageAccountType: 'StandardSSD_LRS'}
      }
    }
    osProfile: {
      computerName: 'issue360pub'
      adminUsername: adminUsername
      linuxConfiguration: {
        disablePasswordAuthentication: true
        provisionVMAgent: true
        ssh: {
          publicKeys: [
            {path: '/home/${adminUsername}/.ssh/authorized_keys', keyData: sshPublicKey}
          ]
        }
      }
    }
    networkProfile: {
      networkInterfaces: [
        {id: nic.id, properties: {deleteOption: 'Detach'}}
      ]
    }
    diagnosticsProfile: {bootDiagnostics: {enabled: false}}
  }
}

output publisherId string = publisher.id
output publisherPrincipal string = publisher.identity.principalId
