@minLength(3)
@maxLength(47)
param name string
param location string
param tags object
param workspaceId string
param peSubnetId string
param zoneIds object
@description('Principal id of the API managed identity. Receives only from the dedicated telemetry Event Hub.')
param consumerPrincipalId string
@description('Owner-selected exercise tier. Standard features and scale-out require a separate decision.')
@allowed(['B1'])
param skuName string = 'B1'
@minValue(1)
@maxValue(1)
param unitCount int = 1
@description('Transport retention in days (1 to 7), not SQL record retention. Azure SQL stays the system of record.')
@minValue(1)
@maxValue(7)
param retentionDays int = 1
@minValue(2)
@maxValue(32)
param partitionCount int = 2
@description('Development only. Allows public network access in addition to the private endpoint.')
param allowPublicNetworkAccess bool = false
@description('False bootstraps identity and RBAC without registering a route endpoint. Set and preserve true only after separately approved sender-role propagation verification.')
param routingReady bool = false
@description('Monthly transport allocation in the subscription billing currency (USD scenario in README). Alerts only, not a hard spend cap.')
@minValue(1)
@maxValue(700)
param monthlyCostEstimate int = 60
param alertEmail string
param budgetStartDate string

var eventHubsDataReceiver = 'a638d3c7-ab3a-418d-83e6-5f17a39d4fde'
var eventHubsDataSender = '2b629674-e913-4c01-ae53-ef4638d8f975'
var consumerGroupName = 'api-consumer'
var telemetryName = 'sensor-readings'
var routeEndpointName = 'api-telemetry'
var telemetryNamespaceFqdn = split(split(replace(telemetryNamespace.properties.serviceBusEndpoint, 'https://', ''), '/')[0], ':')[0]

module scopeGuard 'iothub-scope-guard.bicep' = {
  name: 'iot-scope-guard'
  params: {
    resourceGroupMustBeAma: resourceGroup().name == 'ama' ? 'ok' : ''
    iotLocationMustBeUKSouth: location == 'uksouth' ? 'ok' : ''
  }
}

resource telemetryNamespace 'Microsoft.EventHub/namespaces@2024-01-01' = {
  name: 'eh-${name}'
  location: location
  tags: tags
  dependsOn: [scopeGuard]
  sku: { name: 'Standard', tier: 'Standard', capacity: 1 }
  properties: {
    disableLocalAuth: true
    minimumTlsVersion: '1.2'
    publicNetworkAccess: 'Disabled'
    isAutoInflateEnabled: false
    maximumThroughputUnits: 1
  }
}

resource telemetryNetworkRules 'Microsoft.EventHub/namespaces/networkRuleSets@2024-01-01' = {
  parent: telemetryNamespace
  name: 'default'
  properties: {
    publicNetworkAccess: 'Disabled'
    defaultAction: 'Deny'
    trustedServiceAccessEnabled: true
    ipRules: []
    virtualNetworkRules: []
  }
}

resource telemetry 'Microsoft.EventHub/namespaces/eventhubs@2024-01-01' = {
  parent: telemetryNamespace
  name: telemetryName
  properties: {
    partitionCount: partitionCount
    retentionDescription: {
      cleanupPolicy: 'Delete'
      retentionTimeInHours: retentionDays * 24
    }
  }
}

resource consumerGroup 'Microsoft.EventHub/namespaces/eventhubs/consumergroups@2024-01-01' = {
  parent: telemetry
  name: consumerGroupName
  properties: {}
}

resource hub 'Microsoft.Devices/IotHubs@2023-06-30' = {
  name: name
  location: location
  tags: tags
  dependsOn: [scopeGuard, telemetryNetworkRules]
  identity: { type: 'SystemAssigned' }
  sku: { name: skuName, capacity: unitCount }
  properties: {
    disableLocalAuth: true
    disableDeviceSAS: false
    disableModuleSAS: true
    minTlsVersion: '1.2'
    publicNetworkAccess: allowPublicNetworkAccess ? 'Enabled' : 'Disabled'
    eventHubEndpoints: {
      events: {
        retentionTimeInDays: retentionDays
        partitionCount: partitionCount
      }
    }
    routing: {
      endpoints: {
        eventHubs: routingReady ? [
          {
            name: routeEndpointName
            authenticationType: 'identityBased'
            endpointUri: 'sb://${telemetryNamespaceFqdn}/'
            entityPath: telemetry.name
            resourceGroup: resourceGroup().name
            subscriptionId: subscription().subscriptionId
            identity: {}
          }
        ] : []
      }
      routes: routingReady ? [
        {
          name: 'all-device-messages'
          source: 'DeviceMessages'
          condition: 'true'
          endpointNames: [routeEndpointName]
          isEnabled: true
        }
      ] : []
      fallbackRoute: {
        name: '$fallback'
        source: 'DeviceMessages'
        endpointNames: ['events']
        isEnabled: false
      }
    }
  }
}

resource receiverRole 'Microsoft.Authorization/roleAssignments@2022-04-01' = {
  scope: telemetry
  name: guid(telemetry.id, consumerPrincipalId, eventHubsDataReceiver)
  properties: {
    principalId: consumerPrincipalId
    principalType: 'ServicePrincipal'
    roleDefinitionId: subscriptionResourceId('Microsoft.Authorization/roleDefinitions', eventHubsDataReceiver)
  }
}

// The hub must exist before its system identity can be authorized. Route activation is a separate apply.
resource senderRole 'Microsoft.Authorization/roleAssignments@2022-04-01' = {
  scope: telemetryNamespace
  name: guid(telemetryNamespace.id, hub.id, eventHubsDataSender)
  properties: {
    principalId: hub.identity.principalId
    principalType: 'ServicePrincipal'
    roleDefinitionId: subscriptionResourceId('Microsoft.Authorization/roleDefinitions', eventHubsDataSender)
  }
}

// Connections and identity-operation logs also contain device ids; disabling DeviceTelemetry alone is insufficient.
resource diagnostics 'Microsoft.Insights/diagnosticSettings@2021-05-01-preview' = {
  scope: hub
  name: 'to-log-analytics'
  properties: {
    workspaceId: workspaceId
    logs: [{ categoryGroup: 'allLogs', enabled: false }]
    metrics: [{ category: 'AllMetrics', enabled: true }]
  }
}

resource telemetryDiagnostics 'Microsoft.Insights/diagnosticSettings@2021-05-01-preview' = {
  scope: telemetryNamespace
  name: 'to-log-analytics'
  properties: {
    workspaceId: workspaceId
    logs: [{ categoryGroup: 'allLogs', enabled: false }]
    metrics: [{ category: 'AllMetrics', enabled: true }]
  }
}

module hubEndpoint 'privateEndpoint.bicep' = {
  name: 'pe-${name}'
  params: {
    name: name
    location: location
    tags: tags
    subnetId: peSubnetId
    targetResourceId: hub.id
    groupId: 'iotHub'
    dnsZoneIds: [zoneIds.iotHub, zoneIds.iotHubEndpoint]
  }
}

module telemetryEndpoint 'privateEndpoint.bicep' = {
  name: 'pe-eh-${name}'
  params: {
    name: telemetryNamespace.name
    location: location
    tags: tags
    subnetId: peSubnetId
    targetResourceId: telemetryNamespace.id
    groupId: 'namespace'
    dnsZoneIds: [zoneIds.iotHubEndpoint]
  }
}

resource budget 'Microsoft.Consumption/budgets@2023-05-01' = {
  name: 'budget-${name}'
  properties: {
    category: 'Cost'
    amount: monthlyCostEstimate
    timeGrain: 'Monthly'
    timePeriod: { startDate: budgetStartDate }
    filter: {
      dimensions: {
        name: 'ResourceId'
        operator: 'In'
        values: [
          hub.id
          telemetryNamespace.id
          resourceId('Microsoft.Network/privateEndpoints', 'pe-${name}')
          resourceId('Microsoft.Network/privateEndpoints', 'pe-${telemetryNamespace.name}')
        ]
      }
    }
    notifications: {
      actual80: {
        enabled: true
        operator: 'GreaterThan'
        threshold: 80
        thresholdType: 'Actual'
        contactEmails: [alertEmail]
      }
      forecast100: {
        enabled: true
        operator: 'GreaterThan'
        threshold: 100
        thresholdType: 'Forecasted'
        contactEmails: [alertEmail]
      }
    }
  }
}

output id string = hub.id
output name string = hub.name
output consumerGroup string = consumerGroupName
output eventHubCompatibleName string = telemetryName
output eventHubNamespaceFqdn string = telemetryNamespaceFqdn
output routingEnabled bool = routingReady
