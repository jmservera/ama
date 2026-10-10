targetScope = 'resourceGroup'

@description('Reuse the existing SQL server; do not migrate its retrofit database.')
param sqlServerName string = 'sql-warm-dev-spw6p'
param databaseName string = 'properwarm-exercise'
param storageAccountName string = 'stwarmdevspw6p'
param evidenceContainerName string = 'exercise-evidence'
param location string = 'uksouth'

resource server 'Microsoft.Sql/servers@2023-08-01' existing = {
  name: sqlServerName
}

resource database 'Microsoft.Sql/servers/databases@2023-08-01' = {
  parent: server
  name: databaseName
  location: location
  sku: {
    name: 'Basic'
    tier: 'Basic'
    capacity: 5
  }
  properties: {
    maxSizeBytes: 2147483648
    isLedgerOn: true
    requestedBackupStorageRedundancy: 'Local'
  }
}

resource retention 'Microsoft.Sql/servers/databases/backupShortTermRetentionPolicies@2023-08-01' = {
  parent: database
  name: 'default'
  properties: {
    retentionDays: 7
  }
}

resource storage 'Microsoft.Storage/storageAccounts@2023-05-01' existing = {
  name: storageAccountName
}

resource blobs 'Microsoft.Storage/storageAccounts/blobServices@2023-05-01' existing = {
  parent: storage
  name: 'default'
}

resource evidence 'Microsoft.Storage/storageAccounts/blobServices/containers@2023-05-01' = {
  parent: blobs
  name: evidenceContainerName
  properties: {
    publicAccess: 'None'
  }
}

output sqlDatabase string = database.name
output blobContainer string = evidence.name
