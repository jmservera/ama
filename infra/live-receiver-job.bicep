targetScope = 'resourceGroup'

// Issue 110/184 live receiver job (manual). Authored and compiled only; NOT deployed. Separate from the simulator job: it uses its own receiver identity, so the simulator's read-only cases grant is unchanged. Deployment needs the
// owner steps listed in infra/README.md (receiver identity grants, verified hub route, image push by digest). No secret, key or connection string here.

@description('Existing Container Apps environment in ama. This template never creates or changes an environment.')
param environmentName string = 'cae-cutover-test-demo'
@description('Existing registry login server.')
param registryServer string = 'crcutovertestrzsrg.azurecr.io'
@description('Simulator image by immutable digest built from src/api/live-simulator.Dockerfile. Tags are refused.')
@minLength(1)
param image string
@description('Existing RECEIVER user-assigned identity (not the simulator identity): AcrPull, Azure Event Hubs Data Receiver on sensor-readings and the minimum sensor-table writes listed in infra/README.md.')
param identityName string
@description('Existing IoT Hub host name, for example iot-cutover-test-rzsrg.azure-devices.net. Device registration is a separate owner step.')
param hubHostname string = 'iot-cutover-test-rzsrg.azure-devices.net'
@description('Owner approval reference for sending synthetic readings to the hub. Empty refuses the deployment.')
@minLength(1)
param approvalReference string
@description('Existing Container Apps environment storage (Azure Files share) holding the admin-written control.json (cohort, owner, expiry, stop), mounted read-only. No device certificate is used by the receiver.')
param certStorageName string
@description('Existing SQL logical server FQDN and database; the receiver identity needs the sensor-table writes listed in infra/README.md.')
param sqlServerFqdn string
param sqlDatabaseName string
@description('Set true only after the hub route to sensor-readings and the api-consumer group are verified.')
param routingReady bool = false
@minValue(60)
@maxValue(3600)
param windowSeconds int = 240
param location string = resourceGroup().location

var jobName = 'job-live-receiver'
var digestOk = contains(image, '@sha256:') && !contains(image, ' ') && startsWith(image, '${registryServer}/')
var hubOk = contains(hubHostname, '.azure-devices.net') && !contains(hubHostname, ' ')
var scopeOk = resourceGroup().name == 'ama' && environmentName == 'cae-cutover-test-demo' && digestOk && hubOk && !empty(trim(approvalReference))

module guard './modules/staff-initializer-guard.bicep' = {
  name: 'live-receiver-scope'
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
  tags: { workload: 'live-receiver', 'zava-forward-synthetic': 'true' }
  identity: {
    type: 'UserAssigned'
    userAssignedIdentities: { '${identity.id}': {} }
  }
  properties: {
    environmentId: environment.id
    workloadProfileName: 'Consumption'
    configuration: {
      triggerType: 'Manual'
      replicaTimeout: windowSeconds + 120
      replicaRetryLimit: 0
      manualTriggerConfig: { parallelism: 1, replicaCompletionCount: 1 }
      registries: [{ server: registryServer, identity: identity.id }]
    }
    template: {
      containers: [{
        name: 'live-receiver'
        image: image
        command: ['python', '-m', 'zava_forward.api.live_receiver']
        args: ['--control-file', '/certs/control.json', '--seconds', string(windowSeconds)]
        resources: { cpu: json('0.25'), memory: '0.5Gi' }
        env: [
          { name: 'ZF_SIM_HUB_HOSTNAME', value: hubHostname }
          { name: 'ZF_SIM_APPROVAL', value: approvalReference }
          { name: 'ZF_SIM_ROUTING_READY', value: routingReady ? '1' : '0' }
          { name: 'ZF_SIM_CLIENT_ID', value: identity.properties.clientId }
          { name: 'ZF_SIM_CONTROL_FILE', value: '/certs/control.json' }
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
