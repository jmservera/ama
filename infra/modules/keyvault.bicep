param name string
param location string
param tags object
param workspaceId string
param actionGroupId string
param peSubnetId string
param zoneId string
param secretsUserPrincipalIds array
param enableLock bool
@description('Development only. Allows connectivity from external networks in addition to the private endpoints.')
param allowPublicNetworkAccess bool = false
@description('Development only. False allows a 7 day soft delete and purge so disposable environments can reuse names. Once enabled on a vault, purge protection cannot be turned off.')
param purgeProtection bool = true

resource vault 'Microsoft.KeyVault/vaults@2024-11-01' = {
  name: name
  location: location
  tags: tags
  properties: {
    tenantId: tenant().tenantId
    sku: { family: 'A', name: 'standard' }
    enableRbacAuthorization: true
    enableSoftDelete: true
    softDeleteRetentionInDays: purgeProtection ? 90 : 7
    enablePurgeProtection: purgeProtection ? true : null
    publicNetworkAccess: allowPublicNetworkAccess ? 'Enabled' : 'Disabled'
    networkAcls: {
      defaultAction: allowPublicNetworkAccess ? 'Allow' : 'Deny'
      bypass: 'None'
    }
  }
}

resource secretsUser 'Microsoft.Authorization/roleAssignments@2022-04-01' = [for principalId in secretsUserPrincipalIds: {
  scope: vault
  name: guid(vault.id, principalId, 'kv-secrets-user')
  properties: {
    principalId: principalId
    principalType: 'ServicePrincipal'
    roleDefinitionId: subscriptionResourceId('Microsoft.Authorization/roleDefinitions', '4633458b-17de-408a-b874-0445c86b69e6')
  }
}]

resource diagnostics 'Microsoft.Insights/diagnosticSettings@2021-05-01-preview' = {
  scope: vault
  name: 'to-log-analytics'
  properties: {
    workspaceId: workspaceId
    logs: [{ categoryGroup: 'allLogs', enabled: true }]
    metrics: [{ category: 'AllMetrics', enabled: true }]
  }
}

resource lock 'Microsoft.Authorization/locks@2020-05-01' = if (enableLock) {
  scope: vault
  name: 'do-not-delete'
  properties: { level: 'CanNotDelete' }
}

module endpoint 'privateEndpoint.bicep' = {
  name: 'pe-${name}'
  params: {
    name: name
    location: location
    tags: tags
    subnetId: peSubnetId
    targetResourceId: vault.id
    groupId: 'vault'
    dnsZoneIds: [zoneId]
  }
}

output id string = vault.id
output name string = vault.name

// Secret expiry and failed-access alerts read the AuditEvent logs sent by the diagnostic setting above.
resource expiryAlert 'Microsoft.Insights/scheduledQueryRules@2023-03-15-preview' = {
  name: 'alert-${name}-secret-expiry'
  location: location
  tags: tags
  properties: {
    displayName: 'Key Vault secret near expiry or expired (${name})'
    description: 'A secret is within its Key Vault near-expiry window or has expired. Rotate it using infra/README.md, Key Vault secret lifecycle.'
    severity: 2
    enabled: true
    scopes: [workspaceId]
    evaluationFrequency: 'PT1H'
    windowSize: 'P1D'
    criteria: {
      allOf: [
        {
          query: 'AzureDiagnostics | where ResourceProvider == "MICROSOFT.KEYVAULT" and OperationName in ("SecretNearExpiryEventGridNotification", "SecretExpiredEventGridNotification") and Resource =~ "${name}"'
          timeAggregation: 'Count'
          operator: 'GreaterThan'
          threshold: 0
          failingPeriods: { numberOfEvaluationPeriods: 1, minFailingPeriodsToAlert: 1 }
        }
      ]
    }
    actions: { actionGroups: [actionGroupId] }
  }
}

resource deniedAccessAlert 'Microsoft.Insights/scheduledQueryRules@2023-03-15-preview' = {
  name: 'alert-${name}-denied-access'
  location: location
  tags: tags
  properties: {
    displayName: 'Key Vault data-plane access denied (${name})'
    description: 'Repeated 401 or 403 results on the vault data plane. Review the caller and the access review record.'
    severity: 3
    enabled: true
    scopes: [workspaceId]
    evaluationFrequency: 'PT15M'
    windowSize: 'PT1H'
    criteria: {
      allOf: [
        {
          query: 'AzureDiagnostics | where ResourceProvider == "MICROSOFT.KEYVAULT" and Resource =~ "${name}" and httpStatusCode_d in (401, 403)'
          timeAggregation: 'Count'
          operator: 'GreaterThan'
          threshold: 4
          failingPeriods: { numberOfEvaluationPeriods: 1, minFailingPeriodsToAlert: 1 }
        }
      ]
    }
    actions: { actionGroups: [actionGroupId] }
  }
}
