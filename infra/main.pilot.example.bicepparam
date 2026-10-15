using './main.bicep'

// NON-DEPLOYABLE EXAMPLE. Copy to a private, untracked file and replace every
// placeholder before use. Never pass this file to az deployment.
param workload = 'forward'
param environmentName = 'pilot'
param alertEmail = 'platform-alerts@example.invalid'
param sqlAdminGroupName = 'sg-zava-forward-sql-admins'
param sqlAdminGroupObjectId = '00000000-0000-0000-0000-000000000000'
param entraClientId = ''
param zoneRedundant = false
param enableLocks = true
param deploymentProfile = 'production'
