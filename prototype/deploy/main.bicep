targetScope = 'resourceGroup'

@description('Azure region for the demo resources.')
param location string = resourceGroup().location

@description('Name for the Azure Container Apps managed environment.')
param environmentName string

@description('Name for the local-synthetic demo container app.')
param containerAppName string

@description('Container image reference already available to the Container Apps environment.')
param containerImage string

@description('Infrastructure subnet resource ID in a virtual network configured for Azure Container Apps.')
param infrastructureSubnetId string

@description('Separate private-endpoint subnet, not the Container Apps infrastructure subnet.')
param modelPrivateEndpointSubnetId string
@description('Virtual network resource ID used for the private DNS link.')
param virtualNetworkId string
param modelAccountName string
param modelDeploymentName string = 'case-review'
param modelName string = 'gpt-4.1-mini'
param modelVersion string = '2025-04-14'

resource agentIdentity 'Microsoft.ManagedIdentity/userAssignedIdentities@2023-01-31' = {
  name: '${containerAppName}-agent'
  location: location
}

module model './model.bicep' = {
  name: 'properwarm-private-model'
  params: {
    location: location
    accountName: modelAccountName
    deploymentName: modelDeploymentName
    modelName: modelName
    modelVersion: modelVersion
    principalId: agentIdentity.properties.principalId
  }
}

resource modelDns 'Microsoft.Network/privateDnsZones@2024-06-01' = {
  name: 'privatelink.openai.azure.com'
  location: 'global'
}
resource modelDnsLink 'Microsoft.Network/privateDnsZones/virtualNetworkLinks@2024-06-01' = {
  parent: modelDns
  name: '${containerAppName}-model'
  location: 'global'
  properties: {
    registrationEnabled: false
    virtualNetwork: {
      id: virtualNetworkId
    }
  }
}
resource modelEndpoint 'Microsoft.Network/privateEndpoints@2024-05-01' = {
  name: '${modelAccountName}-private'
  location: location
  properties: {
    subnet: {
      id: modelPrivateEndpointSubnetId
    }
    privateLinkServiceConnections: [{
      name: 'model'
      properties: {
        privateLinkServiceId: model.outputs.accountId
        groupIds: ['account']
      }
    }]
  }
}
resource modelDnsGroup 'Microsoft.Network/privateEndpoints/privateDnsZoneGroups@2024-05-01' = {
  parent: modelEndpoint
  name: 'default'
  properties: {
    privateDnsZoneConfigs: [{
      name: 'openai'
      properties: {
        privateDnsZoneId: modelDns.id
      }
    }]
  }
}

@description('Tags to apply to demo resources.')
param tags object = {
  purpose: 'proper-warm-synthetic-demo'
  environment: 'non-production'
}

resource logWorkspace 'Microsoft.OperationalInsights/workspaces@2023-09-01' = {
  name: '${environmentName}-logs'
  location: location
  tags: tags
  properties: {
    retentionInDays: 30
    sku: {
      name: 'PerGB2018'
    }
  }
}

resource environment 'Microsoft.App/managedEnvironments@2026-01-01' = {
  name: environmentName
  location: location
  tags: tags
  properties: {
    appLogsConfiguration: {
      destination: 'log-analytics'
      logAnalyticsConfiguration: {
        customerId: logWorkspace.properties.customerId
        sharedKey: logWorkspace.listKeys().primarySharedKey
      }
    }
    vnetConfiguration: {
      infrastructureSubnetId: infrastructureSubnetId
      internal: true
    }
  }
}

resource app 'Microsoft.App/containerApps@2026-01-01' = {
  name: containerAppName
  location: location
  tags: tags
  identity: {
    type: 'UserAssigned'
    userAssignedIdentities: {
      '${agentIdentity.id}': {}
    }
  }
  properties: {
    environmentId: environment.id
    configuration: {
      activeRevisionsMode: 'Single'
      ingress: {
        external: false
        targetPort: 8080
        transport: 'http'
        allowInsecure: false
      }
    }
    template: {
      containers: [
        {
          name: 'proper-warm'
          image: containerImage
          env: [
            {
              name: 'AZURE_CLIENT_ID'
              value: agentIdentity.properties.clientId
            }
            {
              name: 'AZURE_OPENAI_ENDPOINT'
              value: model.outputs.endpoint
            }
            {
              name: 'AZURE_OPENAI_DEPLOYMENT'
              value: model.outputs.deploymentName
            }
            {
              name: 'APP_PORT'
              value: '8080'
            }
            {
              name: 'APP_INTERNAL_INGRESS'
              value: 'true'
            }
            {
              name: 'DATA_DIR'
              value: '/var/lib/properwarm'
            }
            {
              name: 'SOURCE_DIR'
              value: '/app/source-data'
            }
          ]
          resources: {
            cpu: 1
            memory: '2Gi'
          }
        }
      ]
      scale: {
        minReplicas: 1
        maxReplicas: 1
      }
    }
  }
}
