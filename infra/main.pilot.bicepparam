using './main.bicep'

param workload = 'forward'
param environmentName = 'dev'
param alertEmail = 'platform-alerts@example.invalid'
param sqlAdminGroupName = 'sg-zava-forward-sql-admins'
param sqlAdminGroupObjectId = '00000000-0000-0000-0000-000000000000'
param entraClientId = ''
param zoneRedundant = false
param enableLocks = true
param deploymentProfile = 'production'
