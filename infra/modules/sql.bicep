param name string
param databaseName string
param location string
@description('Region of the private endpoint, which must match the VNet. Defaults to location.')
param endpointLocation string = location
param tags object
param workspaceId string
param peSubnetId string
param zoneId string
param entraAdminGroupName string
param entraAdminGroupObjectId string
@allowed(['Group', 'User', 'Application'])
param entraAdminPrincipalType string = 'Group'
param enableLock bool
param zoneRedundant bool = false
@description('Serverless vCores keep a non-production demonstrator cheap; raise for production.')
param maxVCores int = 2

resource server 'Microsoft.Sql/servers@2024-05-01-preview' = {
  name: name
  location: location
  tags: tags
  properties: {
    minimalTlsVersion: '1.2'
    publicNetworkAccess: 'Disabled'
    restrictOutboundNetworkAccess: 'Disabled'
    administrators: {
      administratorType: 'ActiveDirectory'
      principalType: entraAdminPrincipalType
      login: entraAdminGroupName
      sid: entraAdminGroupObjectId
      tenantId: tenant().tenantId
      azureADOnlyAuthentication: true
    }
  }
}

resource database 'Microsoft.Sql/servers/databases@2024-05-01-preview' = {
  parent: server
  name: databaseName
  location: location
  tags: tags
  sku: {
    name: 'GP_S_Gen5'
    tier: 'GeneralPurpose'
    family: 'Gen5'
    capacity: maxVCores
  }
  properties: {
    collation: 'SQL_Latin1_General_CP1_CI_AS'
    autoPauseDelay: 60
    minCapacity: json('0.5')
    zoneRedundant: zoneRedundant
    requestedBackupStorageRedundancy: zoneRedundant ? 'Zone' : 'Local'
    // Ledger gives tamper-evident history for transitions, approvals and audit records (NFR-004).
    isLedgerOn: true
  }
}

resource backupRetention 'Microsoft.Sql/servers/databases/backupShortTermRetentionPolicies@2024-05-01-preview' = {
  parent: database
  name: 'default'
  properties: { retentionDays: 14 }
}

resource serverAudit 'Microsoft.Sql/servers/auditingSettings@2024-05-01-preview' = {
  parent: server
  name: 'default'
  properties: {
    state: 'Enabled'
    isAzureMonitorTargetEnabled: true
    auditActionsAndGroups: [
      'SUCCESSFUL_DATABASE_AUTHENTICATION_GROUP'
      'FAILED_DATABASE_AUTHENTICATION_GROUP'
      'BATCH_COMPLETED_GROUP'
    ]
  }
}

resource threatProtection 'Microsoft.Sql/servers/securityAlertPolicies@2024-05-01-preview' = {
  parent: server
  name: 'Default'
  properties: { state: 'Enabled' }
}

resource masterDb 'Microsoft.Sql/servers/databases@2024-05-01-preview' existing = {
  parent: server
  name: 'master'
}

resource serverDiagnostics 'Microsoft.Insights/diagnosticSettings@2021-05-01-preview' = {
  scope: masterDb
  name: 'sql-audit-to-log-analytics'
  properties: {
    workspaceId: workspaceId
    logs: [
      { category: 'SQLSecurityAuditEvents', enabled: true }
    ]
  }
  dependsOn: [serverAudit]
}

resource databaseDiagnostics 'Microsoft.Insights/diagnosticSettings@2021-05-01-preview' = {
  scope: database
  name: 'to-log-analytics'
  properties: {
    workspaceId: workspaceId
    logs: [
      { categoryGroup: 'allLogs', enabled: true }
    ]
    metrics: [{ category: 'Basic', enabled: true }]
  }
}

resource lock 'Microsoft.Authorization/locks@2020-05-01' = if (enableLock) {
  scope: server
  name: 'do-not-delete'
  properties: { level: 'CanNotDelete' }
}

module endpoint 'privateEndpoint.bicep' = {
  name: 'pe-${name}'
  params: {
    name: name
    location: endpointLocation
    tags: tags
    subnetId: peSubnetId
    targetResourceId: server.id
    groupId: 'sqlServer'
    dnsZoneIds: [zoneId]
  }
}

output id string = server.id
output fqdn string = server.properties.fullyQualifiedDomainName
output databaseName string = database.name
