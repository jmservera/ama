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
