@description('Resource name prefix.')
param prefix string
param location string
param tags object

@description('One user-assigned identity per workload so each gets only the roles it needs.')
var workloads = ['api', 'agents', 'orchestrator', 'import']

resource identities 'Microsoft.ManagedIdentity/userAssignedIdentities@2023-01-31' = [for workload in workloads: {
  name: 'id-${prefix}-${workload}'
  location: location
  tags: tags
}]

output ids object = {
  api: identities[0].id
  agents: identities[1].id
  orchestrator: identities[2].id
  import: identities[3].id
}
output principalIds object = {
  api: identities[0].properties.principalId
  agents: identities[1].properties.principalId
  orchestrator: identities[2].properties.principalId
  import: identities[3].properties.principalId
}
output clientIds object = {
  api: identities[0].properties.clientId
  agents: identities[1].properties.clientId
  orchestrator: identities[2].properties.clientId
  import: identities[3].properties.clientId
}
