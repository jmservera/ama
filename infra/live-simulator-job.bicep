targetScope = 'resourceGroup'

// Issue 184 stage 2 live simulator job. Authored and compiled only; NOT deployed. Deployment needs the
// owner steps listed in infra/README.md (IoT Hub live approval, device registration, certificate
// storage, SQL read grant, AcrPull, image push by digest). No secret, key or connection string here.

@description('Existing Container Apps environment in ama. This template never creates or changes an environment.')
param environmentName string = 'cae-cutover-test-demo'
@description('Existing registry login server.')
param registryServer string = 'crcutovertestrzsrg.azurecr.io'
@description('Simulator image by immutable digest built from src/api/live-simulator.Dockerfile. Tags are refused.')
@minLength(1)
param image string
@description('Existing user-assigned identity with AcrPull and read-only SQL access; its client id is passed to the job.')
param identityName string
@description('Existing IoT Hub host name, for example iot-cutover-test-rzsrg.azure-devices.net. Device registration is a separate owner step.')
param hubHostname string = 'iot-cutover-test-rzsrg.azure-devices.net'
@description('Owner approval reference for sending synthetic readings to the hub. Empty refuses the deployment.')
@minLength(1)
param approvalReference string
@description('Existing Container Apps environment storage (Azure Files share) holding <device>.pem, <device>.key and the admin-written control.json (cohort, owner, expiry, stop), mounted read-only.')
param certStorageName string = ''
@secure()
@description('Demo single-environment profile: files for /certs (object of file name to content) held as job secrets instead of Azure Files, for estates where storage shared-key access is disabled. Empty uses certStorageName. Never commit values.')
param secretFiles object = {}
@description('File names (keys of secretFiles) to mount under /certs; not secret.')
param secretFileNames array = []
@description('Existing SQL logical server FQDN and database; the identity needs read access to the case ids only.')
param sqlServerFqdn string
param sqlDatabaseName string
@description('Cron schedule in UTC. Every five minutes matches the reading slot; each run sends the current slot and exits.')
param cronExpression string = '*/5 * * * *'
@minValue(1)
@maxValue(100)
param maxPerSecond int = 10
@allowed(['enforced', 'off'])
@description('The image refuses to start with enforced hardening where the platform keeps inherited capabilities (Container Apps); the demo profile sets off, as the app does.')
param containerHardening string = 'enforced'
@description('Use MQTT/AMQP over WebSockets on 443. The demo private endpoints are reachable on 443 only (8883 and 5671 time out).')
param useWebSockets bool = false
@description('Chance 0 to 0.9 that a device sends nothing in a slot, so the demo shows missing readings (issue 2191). Seeded, so a slot repeats. 0 keeps every reading.')
param failureRate string = '0'
param location string = resourceGroup().location
@description('Optional Action Group resource id. When set, a failed-execution alert is created for this job; empty creates no rule.')
param failureAlertActionGroupId string = ''

var jobName = 'job-live-simulator'
var digestOk = contains(image, '@sha256:') && !contains(image, ' ') && startsWith(image, '${registryServer}/')
var hubOk = contains(hubHostname, '.azure-devices.net') && !contains(hubHostname, ' ')
var useSecret = !empty(secretFileNames)
var secretRefs = [for (n, i) in secretFileNames: { secretRef: 'file-${i}', path: n }]
var certVolume = useSecret ? {
  name: 'device-certs'
  storageType: 'Secret'
  secrets: secretRefs
} : {
  name: 'device-certs'
  storageType: 'AzureFile'
  storageName: certStorageName
  mountOptions: 'ro'
}
var scopeOk = (useSecret || !empty(certStorageName)) && resourceGroup().name == 'ama' && environmentName == 'cae-cutover-test-demo' && digestOk && hubOk && !empty(trim(approvalReference))

module guard './modules/staff-initializer-guard.bicep' = {
  name: 'live-simulator-scope'
  params: {
    approvedScope: scopeOk ? 'ama' : ''
  }
}

resource environment 'Microsoft.App/managedEnvironments@2025-07-01' existing = {
  name: environmentName
}
resource identity 'Microsoft.ManagedIdentity/userAssignedIdentities@2023-01-31' existing = {
  name: identityName
}

resource job 'Microsoft.App/jobs@2025-07-01' = {
  name: jobName
  location: location
  tags: { workload: 'live-simulator', 'zava-forward-synthetic': 'true' }
  identity: {
    type: 'UserAssigned'
    userAssignedIdentities: { '${identity.id}': {} }
  }
  properties: {
    environmentId: environment.id
    workloadProfileName: 'Consumption'
    configuration: {
      triggerType: 'Schedule'
      replicaTimeout: 240
      replicaRetryLimit: 0
      scheduleTriggerConfig: { cronExpression: cronExpression, parallelism: 1, replicaCompletionCount: 1 }
      registries: [{ server: registryServer, identity: identity.id }]
      // Values come from the @secure secretFiles parameter; the linter cannot see through the index.
      #disable-next-line use-secure-value-for-secure-inputs
      secrets: [for (n, i) in secretFileNames: { name: 'file-${i}', value: secretFiles[n] }]
    }
    template: {
      containers: [{
        name: 'live-simulator'
        image: image
        command: ['python', '-m', 'zava_forward.api.live_simulator']
        args: ['--sink', 'iothub', '--once', '--max-per-second', string(maxPerSecond)]
        resources: { cpu: json('0.25'), memory: '0.5Gi' }
        env: [
          { name: 'ZF_CONTAINER_HARDENING', value: containerHardening }
          { name: 'PYTHONDONTWRITEBYTECODE', value: '1' }
          { name: 'TMPDIR', value: '/tmp' }
          { name: 'ZF_STATE', value: '/state' }
          { name: 'ZF_SIM_HUB_HOSTNAME', value: hubHostname }
          { name: 'ZF_SIM_APPROVAL', value: approvalReference }
          { name: 'ZF_SIM_WEBSOCKETS', value: useWebSockets ? '1' : '0' }
          { name: 'ZF_SIM_FAILURE_RATE', value: failureRate }
          { name: 'ZF_SIM_CERT_DIR', value: '/certs' }
          { name: 'ZF_SIM_CONTROL_FILE', value: '/certs/control.json' }
          { name: 'ZF_STORE', value: 'mssql' }
          { name: 'ZF_SQL_AUTH', value: 'msi' }
          { name: 'ZF_SQL_CLIENT_ID', value: identity.properties.clientId }
          { name: 'ZF_SQL_SERVER', value: sqlServerFqdn }
          { name: 'ZF_SQL_DATABASE', value: sqlDatabaseName }
        ]
        volumeMounts: [
          { volumeName: 'device-certs', mountPath: '/certs' }
          { volumeName: 'tmp', mountPath: '/tmp' }
          { volumeName: 'state', mountPath: '/state' }
        ]
      }]
      volumes: [
        certVolume
        { name: 'tmp', storageType: 'EmptyDir' }
        { name: 'state', storageType: 'EmptyDir' }
      ]
    }
  }
  dependsOn: [guard]
}

resource failureAlert 'Microsoft.Insights/metricAlerts@2018-03-01' = if (!empty(failureAlertActionGroupId)) {
  name: 'alert-${jobName}-failed'
  location: 'global'
  properties: {
    description: 'Simulator job failed execution. Owner: Digital service owner (proposed role, actual appointment pending). Runbook: https://github.com/jmservera/ama/blob/main/infra/monitoring-runbooks.md#job-live-simulator.'
    severity: 2
    enabled: true
    scopes: [job.id]
    evaluationFrequency: 'PT5M'
    windowSize: 'PT15M'
    criteria: {
      'odata.type': 'Microsoft.Azure.Monitor.SingleResourceMultipleMetricCriteria'
      allOf: [
        {
          name: 'failed-execution'
          metricNamespace: 'Microsoft.App/jobs'
          metricName: 'Executions'
          dimensions: [{ name: 'state', operator: 'Include', values: ['Failed'] }]
          operator: 'GreaterThan'
          threshold: 0
          timeAggregation: 'Total'
          criterionType: 'StaticThresholdCriterion'
        }
      ]
    }
    actions: [{ actionGroupId: failureAlertActionGroupId }]
  }
}

output jobName string = job.name
