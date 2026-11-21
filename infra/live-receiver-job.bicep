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
param certStorageName string = ''
@secure()
@description('Demo single-environment profile: files for /certs (object of file name to content) held as job secrets instead of Azure Files, for estates where storage shared-key access is disabled. Empty uses certStorageName. Never commit values.')
param secretFiles object = {}
@description('File names (keys of secretFiles) to mount under /certs; not secret.')
param secretFileNames array = []
@description('Existing SQL logical server FQDN and database; the receiver identity needs the sensor-table writes listed in infra/README.md.')
param sqlServerFqdn string
param sqlDatabaseName string
@description('Set true only after the hub route to sensor-readings and the api-consumer group are verified.')
param routingReady bool = false
@minValue(60)
@maxValue(3600)
param windowSeconds int = 240
@description('Optional cron schedule (UTC). Empty keeps the Manual trigger.')
param cronExpression string = ''
@minValue(1000)
@maxValue(100000)
@description('Event cap per window; the receiver replays the retained backlog and counts duplicates.')
param maxEvents int = 1000
@allowed(['enforced', 'off'])
@description('The image refuses to start with enforced hardening where the platform keeps inherited capabilities (Container Apps); the demo profile sets off, as the app does.')
param containerHardening string = 'enforced'
@description('Use MQTT/AMQP over WebSockets on 443. The demo private endpoints are reachable on 443 only (8883 and 5671 time out).')
param useWebSockets bool = false
@description('Read the device origin from the message annotations the hub stamps (the demo hub does) instead of application properties. A device-supplied origin property is still refused.')
param systemOrigin bool = false
param location string = resourceGroup().location

var jobName = 'job-live-receiver'
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
      triggerType: empty(cronExpression) ? 'Manual' : 'Schedule'
      replicaTimeout: windowSeconds + 120
      replicaRetryLimit: 0
      manualTriggerConfig: empty(cronExpression) ? { parallelism: 1, replicaCompletionCount: 1 } : null
      scheduleTriggerConfig: empty(cronExpression) ? null : { cronExpression: cronExpression, parallelism: 1, replicaCompletionCount: 1 }
      registries: [{ server: registryServer, identity: identity.id }]
      // Values come from the @secure secretFiles parameter; the linter cannot see through the index.
      #disable-next-line use-secure-value-for-secure-inputs
      secrets: [for (n, i) in secretFileNames: { name: 'file-${i}', value: secretFiles[n] }]
    }
    template: {
      containers: [{
        name: 'live-receiver'
        image: image
        command: ['python', '-m', 'zava_forward.api.live_receiver']
        args: ['--control-file', '/certs/control.json', '--seconds', string(windowSeconds), '--events', string(maxEvents)]
        resources: { cpu: json('0.25'), memory: '0.5Gi' }
        env: [
          { name: 'ZF_CONTAINER_HARDENING', value: containerHardening }
          { name: 'PYTHONDONTWRITEBYTECODE', value: '1' }
          { name: 'TMPDIR', value: '/tmp' }
          { name: 'ZF_STATE', value: '/state' }
          { name: 'ZF_SIM_HUB_HOSTNAME', value: hubHostname }
          { name: 'ZF_SIM_APPROVAL', value: approvalReference }
          { name: 'ZF_SIM_SYSTEM_ORIGIN', value: systemOrigin ? '1' : '0' }
          { name: 'ZF_SIM_WEBSOCKETS', value: useWebSockets ? '1' : '0' }
          { name: 'ZF_SIM_ROUTING_READY', value: routingReady ? '1' : '0' }
          { name: 'ZF_SIM_CLIENT_ID', value: identity.properties.clientId }
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

output jobName string = job.name
