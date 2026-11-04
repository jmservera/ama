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
@description('Existing Container Apps environment storage (Azure Files share) holding <device>.pem and <device>.key, mounted read-only.')
param certStorageName string
@description('Existing SQL logical server FQDN and database; the identity needs read access to the case ids only.')
param sqlServerFqdn string
param sqlDatabaseName string
@description('Cron schedule in UTC. Every five minutes matches the reading slot; each run sends the current slot and exits.')
param cronExpression string = '*/5 * * * *'
@minValue(1)
@maxValue(100)
param maxPerSecond int = 10
param location string = resourceGroup().location

var jobName = 'job-live-simulator'
var digestOk = contains(image, '@sha256:') && !contains(image, ' ') && startsWith(image, '${registryServer}/')
var hubOk = contains(hubHostname, '.azure-devices.net') && !contains(hubHostname, ' ')
var scopeOk = resourceGroup().name == 'ama' && environmentName == 'cae-cutover-test-demo' && digestOk && hubOk && !empty(trim(approvalReference))

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
    }
    template: {
      containers: [{
        name: 'live-simulator'
        image: image
        command: ['python', '-m', 'zava_forward.api.live_simulator']
        args: ['--sink', 'iothub', '--once', '--max-per-second', string(maxPerSecond)]
        resources: { cpu: json('0.25'), memory: '0.5Gi' }
        env: [
          { name: 'ZF_SIM_HUB_HOSTNAME', value: hubHostname }
          { name: 'ZF_SIM_APPROVAL', value: approvalReference }
          { name: 'ZF_SIM_CERT_DIR', value: '/certs' }
          { name: 'ZF_STORE', value: 'mssql' }
          { name: 'ZF_SQL_AUTH', value: 'msi' }
          { name: 'ZF_SQL_CLIENT_ID', value: identity.properties.clientId }
          { name: 'ZF_SQL_SERVER', value: sqlServerFqdn }
          { name: 'ZF_SQL_DATABASE', value: sqlDatabaseName }
        ]
        volumeMounts: [{ volumeName: 'device-certs', mountPath: '/certs' }]
      }]
      volumes: [{ name: 'device-certs', storageType: 'AzureFile', storageName: certStorageName, mountOptions: 'ro' }]
    }
  }
  dependsOn: [guard]
}

output jobName string = job.name
