targetScope = 'resourceGroup'

@description('Existing internal workload-profile environment. This additive entry point never changes environment or data-service networking.')
param environmentName string
@description('Existing authenticated API in that environment, the sole origin.')
param apiName string
param workspaceName string
param prefix string
param tags object = {}
@description('False restores browser redirects. True is only for deliberate bearer-only service tests; neither mode provisions a registration or credential.')
param entraBearerOnly bool = false

resource existingEnvironment 'Microsoft.App/managedEnvironments@2025-07-01' existing = {
  name: environmentName
}
resource api 'Microsoft.App/containerApps@2025-07-01' existing = {
  name: apiName
}
resource auth 'Microsoft.App/containerApps/authConfigs@2025-07-01' existing = {
  parent: api
  name: 'current'
}
resource workspace 'Microsoft.OperationalInsights/workspaces@2023-09-01' existing = {
  name: workspaceName
}

module guard 'modules/edge-existing-guard.bicep' = {
  name: 'edge-existing-guard'
  params: {
    privateEnvironment: existingEnvironment.properties.vnetConfiguration.internal == true && existingEnvironment.properties.publicNetworkAccess == 'Disabled' ? 'ok' : ''
    authenticatedOrigin: api.properties.managedEnvironmentId == existingEnvironment.id && auth.properties.platform.enabled == true && !empty(auth.properties.identityProviders.azureActiveDirectory.registration.clientId) ? 'ok' : ''
  }
}

module edge 'modules/edge.bicep' = {
  name: 'public-edge-existing'
  dependsOn: [browserAuth]
  params: {
    prefix: prefix
    tags: union(existingEnvironment.tags, tags)
    environmentId: existingEnvironment.id
    originHostName: api.properties.configuration.ingress.fqdn
    privateLinkLocation: existingEnvironment.location
    workspaceId: workspace.id
    wafMode: 'Prevention'
  }
}

module browserAuth 'modules/edge-existing-auth.bicep' = {
  name: 'edge-existing-auth'
  dependsOn: [guard]
  params: {
    apiName: apiName
    currentAuth: auth.properties
    entraBearerOnly: entraBearerOnly
  }
}

output publicHostName string = edge.outputs.publicHostName
output entraRedirectUri string = edge.outputs.entraRedirectUri
