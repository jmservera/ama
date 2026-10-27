targetScope = 'resourceGroup'

@description('Existing demo Container Apps environment in ama. This template never creates or changes an environment.')
param environmentName string = 'cae-cutover-test-demo'
@description('Existing private vault holding the two owner-written resident demo secrets.')
param keyVaultName string = 'kv-cutovertest-rzsrg'
@description('Existing registry login server.')
param registryServer string = 'crcutovertestrzsrg.azurecr.io'
@description('Existing registry name, used only to scope AcrPull.')
param registryName string = 'crcutovertestrzsrg'
@description('Resident demo image by immutable digest, for example <registry>/zava-resident-demo@sha256:<64 hex>. Tags are refused.')
@minLength(1)
param image string
@description('Existing SQL logical server FQDN and database; runtime access is the read-only view principal only.')
param sqlServerFqdn string
param sqlDatabaseName string
@description('Explicit UTC expiry, no later than the packaged resident demo policy maximum (inclusive). The service refuses to start at or after its configured expiry.')
@minLength(20)
@maxLength(20)
param expiresAt string
@description('False is the rollback: the app has no ingress and cannot be reached.')
param externalIngress bool = true
param location string = resourceGroup().location

var appName = 'ca-resident-demo'
var identityName = 'id-resident-demo'
var verifierSecret = 'resident-demo-password-verifier'
var sessionSecret = 'resident-demo-session-key'
var maximumExpiry = loadJsonContent('../src/core/src/zava_forward/core/resident-demo.json').maximum_expiry_utc
var digestOk = contains(image, '@sha256:') && !contains(image, ' ') && startsWith(image, '${registryServer}/')
var scopeOk = resourceGroup().name == 'ama' && environmentName == 'cae-cutover-test-demo' && digestOk && endsWith(expiresAt, 'Z') && dateTimeToEpoch(expiresAt) <= dateTimeToEpoch(maximumExpiry)

module guard './modules/staff-initializer-guard.bicep' = {
  name: 'resident-demo-scope'
  params: {
    approvedScope: scopeOk ? 'ama' : ''
  }
}

resource environment 'Microsoft.App/managedEnvironments@2025-07-01' existing = {
  name: environmentName
}
resource vault 'Microsoft.KeyVault/vaults@2023-07-01' existing = {
  name: keyVaultName
}
resource verifier 'Microsoft.KeyVault/vaults/secrets@2023-07-01' existing = {
  parent: vault
  name: verifierSecret
}
resource sessionKey 'Microsoft.KeyVault/vaults/secrets@2023-07-01' existing = {
  parent: vault
  name: sessionSecret
}
resource registry 'Microsoft.ContainerRegistry/registries@2023-07-01' existing = {
  name: registryName
}

resource identity 'Microsoft.ManagedIdentity/userAssignedIdentities@2023-01-31' = {
  name: identityName
  location: location
  tags: { workload: 'resident-demo', 'zava-forward-synthetic': 'true' }
  dependsOn: [guard]
}

var secretsUserRole = subscriptionResourceId('Microsoft.Authorization/roleDefinitions', '4633458b-17de-408a-b874-0445c86b69e6')

resource verifierReader 'Microsoft.Authorization/roleAssignments@2022-04-01' = {
  scope: verifier
  name: guid(verifier.id, identity.id, 'resident-demo-secrets-user')
  properties: {
    roleDefinitionId: secretsUserRole
    principalId: identity.properties.principalId
    principalType: 'ServicePrincipal'
  }
}

resource sessionKeyReader 'Microsoft.Authorization/roleAssignments@2022-04-01' = {
  scope: sessionKey
  name: guid(sessionKey.id, identity.id, 'resident-demo-secrets-user')
  properties: {
    roleDefinitionId: secretsUserRole
    principalId: identity.properties.principalId
    principalType: 'ServicePrincipal'
  }
}

resource acrPull 'Microsoft.Authorization/roleAssignments@2022-04-01' = {
  scope: registry
  name: guid(registry.id, identity.id, 'resident-demo-acr-pull')
  properties: {
    roleDefinitionId: subscriptionResourceId('Microsoft.Authorization/roleDefinitions', '7f951dda-4ed3-4680-a7ca-43fe172d538d')
    principalId: identity.properties.principalId
    principalType: 'ServicePrincipal'
  }
}

resource app 'Microsoft.App/containerApps@2025-07-01' = {
  name: appName
  location: location
  tags: { workload: 'resident-demo', 'zava-forward-synthetic': 'true' }
  identity: {
    type: 'UserAssigned'
    userAssignedIdentities: { '${identity.id}': {} }
  }
  properties: {
    managedEnvironmentId: environment.id
    workloadProfileName: 'Consumption'
    configuration: {
      activeRevisionsMode: 'Single'
      ingress: externalIngress ? {
        external: true
        targetPort: 8089
        transport: 'http'
        allowInsecure: false
      } : null
      registries: [{ server: registryServer, identity: identity.id }]
      secrets: [
        { name: 'demo-password-verifier', keyVaultUrl: '${vault.properties.vaultUri}secrets/${verifierSecret}', identity: identity.id }
        { name: 'demo-session-key', keyVaultUrl: '${vault.properties.vaultUri}secrets/${sessionSecret}', identity: identity.id }
      ]
    }
    template: {
      containers: [{
        name: 'resident-demo'
        image: image
        resources: { cpu: json('0.25'), memory: '0.5Gi' }
        env: [
          { name: 'ZF_DEMO_EXPIRES_AT', value: expiresAt }
          { name: 'ZF_DEMO_ALLOWED_HOSTS', value: '${appName}.${environment.properties.defaultDomain}' }
          { name: 'ZF_DEMO_CLIENT_ADDRESS', value: 'ingress-rightmost' }
          { name: 'ZF_DEMO_PASSWORD_VERIFIER', secretRef: 'demo-password-verifier' }
          { name: 'ZF_DEMO_SESSION_KEY', secretRef: 'demo-session-key' }
          { name: 'ZF_SQL_AUTH', value: 'msi' }
          { name: 'ZF_SQL_CLIENT_ID', value: identity.properties.clientId }
          { name: 'ZF_SQL_SERVER', value: sqlServerFqdn }
          { name: 'ZF_SQL_DATABASE', value: sqlDatabaseName }
          { name: 'PORT', value: '8089' }
        ]
      }]
      scale: { minReplicas: 0, maxReplicas: 1 }
    }
  }
  dependsOn: [guard, verifierReader, sessionKeyReader, acrPull]
}

output appName string = app.name
output identityName string = identity.name
output allowedHost string = '${appName}.${environment.properties.defaultDomain}'
