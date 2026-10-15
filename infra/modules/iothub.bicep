param name string
param location string
param tags object
param workspaceId string
param peSubnetId string
param zoneIds object
@description('Principal ids granted read access to the built-in device-to-cloud endpoint (the API consumer identity only).')
param consumerPrincipalIds array
@description('Hub tier. B1 supports device-to-cloud and message routing only, which is all that simulated in-use monitoring needs. S1 adds cloud-to-device, twins and IoT Edge.')
@allowed(['B1', 'S1'])
param skuName string = 'B1'
@minValue(1)
@maxValue(10)
param unitCount int = 1
@description('Days the built-in endpoint retains messages for the consumer (1 to 7). Azure SQL stays the system of record.')
@minValue(1)
@maxValue(7)
param retentionDays int = 1
@minValue(2)
@maxValue(32)
param partitionCount int = 2
@description('Development only. Allows public network access in addition to the private endpoint.')
param allowPublicNetworkAccess bool = false
@description('Expected monthly cost estimate in the billing currency; creates a dedicated budget scoped to the hub.')
param monthlyCostEstimate int = 25
param alertEmail string
param budgetStartDate string

var eventHubsDataReceiver = 'a638d3c7-ab3a-418d-83e6-5f17a39d4fde'
var consumerGroupName = 'api-consumer'

resource hub 'Microsoft.Devices/IotHubs@2023-06-30' = {
  name: name
  location: location
  tags: tags
  sku: { name: skuName, capacity: unitCount }
  properties: {
    disableLocalAuth: true
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
      fallbackRoute: {
        name: '$fallback'
        source: 'DeviceMessages'
        endpointNames: ['events']
        isEnabled: true
      }
    }
  }
}

resource consumerGroup 'Microsoft.Devices/IotHubs/eventHubEndpoints/ConsumerGroups@2023-06-30' = {
  name: '${hub.name}/events/${consumerGroupName}'
  properties: { name: consumerGroupName }
}

resource receiverRoles 'Microsoft.Authorization/roleAssignments@2022-04-01' = [for principalId in consumerPrincipalIds: {
  scope: hub
  name: guid(hub.id, principalId, eventHubsDataReceiver)
  properties: {
    principalId: principalId
    principalType: 'ServicePrincipal'
    roleDefinitionId: subscriptionResourceId('Microsoft.Authorization/roleDefinitions', eventHubsDataReceiver)
  }
}]

// DeviceTelemetry is deliberately not logged: readings and device ids stay out of diagnostics.
resource diagnostics 'Microsoft.Insights/diagnosticSettings@2021-05-01-preview' = {
  scope: hub
  name: 'to-log-analytics'
  properties: {
    workspaceId: workspaceId
    logs: [
      { category: 'Connections', enabled: true }
      { category: 'DeviceIdentityOperations', enabled: true }
      { category: 'Routes', enabled: true }
      { category: 'Configurations', enabled: true }
    ]
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
        values: [hub.id]
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
output eventHubCompatibleName string = 'events'
