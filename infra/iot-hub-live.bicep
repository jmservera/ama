@description('Reconcile children of the existing exercise hub only. No hub PUT or private endpoint change.')
@allowed(['iot-cutover-test-rzsrg'])
param name string = 'iot-cutover-test-rzsrg'
param location string = 'uksouth'
@allowed(['B1'])
param skuName string = 'B1'
@minValue(1)
@maxValue(1)
param unitCount int = 1

module scopeGuard 'modules/iothub-scope-guard.bicep' = {
  name: 'iot-live-scope-guard'
  params: {
    resourceGroupMustBeAma: resourceGroup().name == 'ama' ? 'ok' : ''
    iotLocationMustBeUKSouth: location == 'uksouth' && hub.location == location ? 'ok' : ''
    existingHubSkuMustMatch: string(hub.sku.name == skuName ? 'ok' : '')
    existingHubUnitsMustMatch: string(hub.sku.capacity == unitCount ? 'ok' : '')
  }
}

resource workspace 'Microsoft.OperationalInsights/workspaces@2023-09-01' existing = {
  name: 'log-cutover-test'
}

resource hub 'Microsoft.Devices/IotHubs@2023-06-30' existing = {
  name: name
}

resource consumerGroup 'Microsoft.Devices/IotHubs/eventHubEndpoints/ConsumerGroups@2023-06-30' = {
  name: '${hub.name}/events/api-consumer'
  dependsOn: [scopeGuard]
  properties: { name: 'api-consumer' }
}

resource diagnostics 'Microsoft.Insights/diagnosticSettings@2021-05-01-preview' = {
  scope: hub
  name: 'to-log-analytics'
  dependsOn: [scopeGuard]
  properties: {
    workspaceId: workspace.id
    logAnalyticsDestinationType: 'AzureDiagnostics'
    logs: [{ categoryGroup: 'allLogs', enabled: false }]
    metrics: [{ category: 'AllMetrics', enabled: true }]
  }
}

output id string = hub.id
output hostname string = hub.properties.hostName
output consumerGroup string = 'api-consumer'
