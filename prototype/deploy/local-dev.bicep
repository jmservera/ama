targetScope = 'resourceGroup'

@description('IPv4 egress observed for this workstation/company proxy; no unrestricted access.')
param allowedIp string
@description('Additional individually approved egress IPv4 addresses, for route-dependent company NAT. Include every approved rule on redeployment.')
param additionalAllowedIps array = []
@description('Entra object ID of the developer receiving inference permission only.')
param developerPrincipalId string
param location string = resourceGroup().location
param accountName string = 'pw-dev-${uniqueString(subscription().id, resourceGroup().id)}'
param deploymentName string = 'case-review'
param modelName string = 'gpt-4.1-mini'
param modelVersion string = '2025-04-14'

module model './model.bicep' = {
  name: 'properwarm-local-model-resources'
  params: {
    location: location
    accountName: accountName
    deploymentName: deploymentName
    modelName: modelName
    modelVersion: modelVersion
    principalId: developerPrincipalId
    principalType: 'User'
    allowFirewallAccess: true
    allowedIps: union([allowedIp], additionalAllowedIps)
  }
}

output endpoint string = model.outputs.endpoint
output deploymentName string = model.outputs.deploymentName
output modelVersion string = model.outputs.modelVersion
output accountId string = model.outputs.accountId
