using './main.bicep'

param workload = 'warm'
param environmentName = 'dev'
param alertEmail = 'platform-alerts@example.invalid'
param sqlAdminGroupName = 'sg-proper-warm-sql-admins'
param sqlAdminGroupObjectId = '00000000-0000-0000-0000-000000000000'
param entraClientId = ''
param zoneRedundant = false
param enableLocks = false
