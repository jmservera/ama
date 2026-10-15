param prefix string
param location string
param tags object
param workspaceId string
param infrastructureSubnetId string
param vnetId string
param identityIds object
param identityClientIds object
param registryServer string
param appInsightsConnectionString string
param sqlServerFqdn string
param sqlDatabaseName string
param storageAccountName string
param foundryEndpoint string
param foundryProjectName string
param modelDeploymentNames object
param keyVaultUri string
param entraClientId string
param entraRoleMap object = {}
param tokenStoreReady bool = false
param tokenStoreAccountName string = ''
param tokenMaintenanceIdentityId string = ''
param tokenMaintenanceClientId string = ''
param zoneRedundant bool = false
@allowed(['blob', 'sharepoint'])
param evidenceStore string = 'blob'
param sharePointSiteId string = ''
param apiImage string
param enableApiAi bool = false
param agentImage string
param orchestratorImage string
param importImage string

var queueEndpoint = 'https://${storageAccountName}.queue.${environment().suffixes.storage}'
var blobEndpoint = 'https://${storageAccountName}.blob.${environment().suffixes.storage}'
@description('Development only. Allows connectivity from external networks in addition to the private endpoints.')
param allowPublicNetworkAccess bool = false
@description('True when Front Door fronts the app; EasyAuth then builds callback URLs from the forwarded edge host.')
param behindPublicEdge bool = false
@description('Map tile URL template (https). Empty means no map background in production.')
param tileUrl string = ''
@description('Attribution text shown with the map tiles.')
param tileAttribution string = ''

resource environmentResource 'Microsoft.App/managedEnvironments@2025-07-01' = {
  name: 'cae-${prefix}'
  location: location
  tags: tags
  properties: {
    zoneRedundant: zoneRedundant
    publicNetworkAccess: allowPublicNetworkAccess ? 'Enabled' : 'Disabled'
    vnetConfiguration: {
      internal: !allowPublicNetworkAccess
      infrastructureSubnetId: infrastructureSubnetId
    }
    workloadProfiles: [
      { name: 'Consumption', workloadProfileType: 'Consumption' }
    ]
    appLogsConfiguration: { destination: 'azure-monitor' }
    peerAuthentication: { mtls: { enabled: true } }
  }
}

resource diagnostics 'Microsoft.Insights/diagnosticSettings@2021-05-01-preview' = {
  scope: environmentResource
  name: 'to-log-analytics'
  properties: {
    workspaceId: workspaceId
    logs: [{ categoryGroup: 'allLogs', enabled: true }]
    metrics: [{ category: 'AllMetrics', enabled: true }]
  }
}

module dns 'envDns.bicep' = if (!allowPublicNetworkAccess) {
  name: 'dns-${prefix}'
  params: {
    prefix: prefix
    tags: tags
    domain: environmentResource.properties.defaultDomain
    staticIp: environmentResource.properties.staticIp
    vnetId: vnetId
  }
}

var authEnabled = !empty(entraClientId)

var commonEnv = [
  { name: 'APPLICATIONINSIGHTS_CONNECTION_STRING', value: appInsightsConnectionString }
  { name: 'OTEL_SERVICE_NAMESPACE', value: 'zava-forward' }
]

resource api 'Microsoft.App/containerApps@2025-07-01' = {
  name: 'ca-${prefix}-api'
  location: location
  tags: union(tags, { workload: 'api' })
  identity: {
    type: 'UserAssigned'
    userAssignedIdentities: { '${identityIds.api}': {} }
  }
  properties: {
    managedEnvironmentId: environmentResource.id
    workloadProfileName: 'Consumption'
    configuration: {
      activeRevisionsMode: 'Single'
      ingress: {
        external: true
        targetPort: 8088
        transport: 'auto'
        allowInsecure: false
      }
      registries: [{ server: registryServer, identity: identityIds.api }]
      secrets: concat(authEnabled ? [
        { name: 'entra-client-secret', keyVaultUrl: '${keyVaultUri}/secrets/entra-client-secret', identity: identityIds.api }
      ] : [], tokenStoreReady ? [
        { name: 'entra-token-store-sas', keyVaultUrl: '${keyVaultUri}/secrets/entra-token-store-sas', identity: identityIds.api }
      ] : [])
    }
    template: {
      containers: [
        {
          name: 'api'
          image: apiImage
          resources: { cpu: json('0.5'), memory: '1Gi' }
          env: concat(commonEnv, [
            { name: 'AZURE_CLIENT_ID', value: identityClientIds.api }
            { name: 'SQL_SERVER', value: sqlServerFqdn }
            { name: 'SQL_DATABASE', value: sqlDatabaseName }
            { name: 'BLOB_ENDPOINT', value: blobEndpoint }
            { name: 'QUEUE_ENDPOINT', value: queueEndpoint }
            { name: 'KEY_VAULT_URI', value: keyVaultUri }
            { name: 'EVIDENCE_STORE', value: evidenceStore }
            { name: 'SHAREPOINT_SITE_ID', value: sharePointSiteId }
            { name: 'ENTRA_TENANT_ID', value: tenant().tenantId }
            { name: 'ENTRA_CLIENT_ID', value: entraClientId }
            // Settings read by the MVP workbench image (src/api/README.md, Configuration).
            { name: 'ZF_TILE_URL', value: tileUrl }
            { name: 'ZF_TILE_ATTRIBUTION', value: tileAttribution }
            { name: 'ZF_STORE', value: 'mssql' }
            { name: 'ZF_SQL_SERVER', value: sqlServerFqdn }
            { name: 'ZF_SQL_DATABASE', value: sqlDatabaseName }
            { name: 'ZF_SQL_AUTH', value: 'msi' }
            { name: 'ZF_SQL_CLIENT_ID', value: identityClientIds.api }
            { name: 'ZF_DOC_STORE', value: 'azure-blob' }
            { name: 'ZF_BLOB_ACCOUNT_URL', value: blobEndpoint }
            { name: 'ZF_BLOB_CONTAINER', value: 'evidence' }
            { name: 'ZF_BLOB_CLIENT_ID', value: identityClientIds.api }
          ], tokenStoreReady ? [
            // A versionless secret reference triggers the supported revision refresh on SAS rotation.
            { name: 'AUTH_TOKEN_STORE_ROTATION', secretRef: 'entra-token-store-sas' }
          ] : [], enableApiAi ? [
            { name: 'AI_ENDPOINT', value: foundryEndpoint }
            { name: 'AI_DEPLOYMENT', value: modelDeploymentNames.standard }
            { name: 'AI_DEPLOYMENT_STRONG', value: modelDeploymentNames.capable }
          ] : [], authEnabled ? [
            { name: 'ZF_AUTH', value: 'trusted-proxy' }
            { name: 'ZF_TRUSTED_PROXY', value: '1' }
            { name: 'ZF_ENTRA_TENANT_ID', value: tenant().tenantId }
            { name: 'ZF_ENV', value: 'production' }
          ] : [], empty(entraRoleMap) ? [] : [
            { name: 'ZF_ROLE_MAP', value: string(entraRoleMap) }
          ])
          probes: [
            { type: 'Liveness', httpGet: { path: '/healthz', port: 8088 } }
            { type: 'Readiness', httpGet: { path: '/healthz', port: 8088 } }
          ]
        }
      ]
      scale: {
        minReplicas: 2
        maxReplicas: 4
        rules: [
          { name: 'http', http: { metadata: { concurrentRequests: '50' } } }
        ]
      }
    }
  }
  dependsOn: [dns]
}

resource apiAuth 'Microsoft.App/containerApps/authConfigs@2025-07-01' = if (!empty(entraClientId)) {
  parent: api
  name: 'current'
  properties: {
    platform: { enabled: true }
    httpSettings: { forwardProxy: { convention: behindPublicEdge ? 'Standard' : 'NoProxy' } }
    login: {
      tokenStore: {
        enabled: tokenStoreReady
        azureBlobStorage: tokenStoreReady ? { sasUrlSettingName: 'entra-token-store-sas' } : null
      }
    }
    globalValidation: {
      unauthenticatedClientAction: 'RedirectToLoginPage'
      redirectToProvider: 'azureactivedirectory'
      excludedPaths: ['/healthz', '/readyz', '/', '/welcome.html', '/style.css', '/zava-logo.png', '/sign-in']
    }
    identityProviders: {
      azureActiveDirectory: {
        enabled: true
        login: {
          loginParameters: tokenStoreReady
            ? ['scope=openid profile email https://graph.microsoft.com/User.Read offline_access', 'prompt=select_account']
            : ['prompt=select_account']
        }
        registration: {
          openIdIssuer: '${environment().authentication.loginEndpoint}${tenant().tenantId}/v2.0'
          clientId: entraClientId
          clientSecretSettingName: 'entra-client-secret'
        }

        validation: {
          allowedAudiences: ['api://${entraClientId}']
        }
      }
    }
  }
}

resource tokenRenewal 'Microsoft.App/jobs@2025-07-01' = if (!empty(tokenMaintenanceIdentityId)) {
  name: 'job-${prefix}-auth-renewal'
  location: location
  tags: union(tags, { workload: 'entra-token-maintenance', dataClassification: 'authentication-secrets' })
  identity: {
    type: 'UserAssigned'
    userAssignedIdentities: { '${tokenMaintenanceIdentityId}': {} }
  }
  properties: {
    environmentId: environmentResource.id
    workloadProfileName: 'Consumption'
    configuration: {
      triggerType: 'Schedule'
      replicaTimeout: 180
      replicaRetryLimit: 2
      scheduleTriggerConfig: { cronExpression: '0 3 * * *', parallelism: 1, replicaCompletionCount: 1 }
      registries: [{ server: registryServer, identity: tokenMaintenanceIdentityId }]
    }
    template: {
      containers: [{
        name: 'auth-renewal'
        image: apiImage
        command: ['python', '-m', 'zava_forward.orchestrator.token_store']
        resources: { cpu: json('0.25'), memory: '0.5Gi' }
        env: [
          { name: 'AZURE_CLIENT_ID', value: tokenMaintenanceClientId }
          { name: 'TOKEN_STORAGE_ACCOUNT', value: tokenStoreAccountName }
          { name: 'KEY_VAULT_URI', value: keyVaultUri }
        ]
      }]
    }
  }
}

// The agent runner has no database, blob or write credential. It reads context and posts proposals only through the API tool contract.
resource agents 'Microsoft.App/containerApps@2025-07-01' = {
  name: 'ca-${prefix}-agents'
  location: location
  tags: union(tags, { workload: 'agents' })
  identity: {
    type: 'UserAssigned'
    userAssignedIdentities: { '${identityIds.agents}': {} }
  }
  properties: {
    managedEnvironmentId: environmentResource.id
    workloadProfileName: 'Consumption'
    configuration: {
      activeRevisionsMode: 'Single'
      registries: [{ server: registryServer, identity: identityIds.agents }]
    }
    template: {
      containers: [
        {
          name: 'agents'
          image: agentImage
          resources: { cpu: json('0.5'), memory: '1Gi' }
          env: concat(commonEnv, [
            { name: 'AZURE_CLIENT_ID', value: identityClientIds.agents }
            { name: 'FOUNDRY_ENDPOINT', value: foundryEndpoint }
            { name: 'FOUNDRY_PROJECT', value: foundryProjectName }
            { name: 'MODEL_DEPLOYMENT_DEFAULT', value: modelDeploymentNames.standard }
            { name: 'MODEL_DEPLOYMENT_CAPABLE', value: modelDeploymentNames.capable }
            { name: 'QUEUE_ENDPOINT', value: queueEndpoint }
            { name: 'TASK_QUEUE', value: 'agent-tasks' }
            { name: 'POISON_QUEUE', value: 'agent-tasks-poison' }
            { name: 'API_BASE_URL', value: 'https://${api.properties.configuration.ingress.fqdn}' }
            { name: 'API_AUDIENCE', value: 'api://${entraClientId}' }
          ])
        }
      ]
      scale: {
        minReplicas: 0
        maxReplicas: 5
        rules: [
          {
            name: 'agent-task-queue'
            custom: {
              type: 'azure-queue'
              metadata: {
                accountName: storageAccountName
                queueName: 'agent-tasks'
                queueLength: '5'
                cloud: 'AzurePublicCloud'
              }
              identity: identityIds.agents
            }
          }
        ]
      }
    }
  }
}

resource orchestrator 'Microsoft.App/jobs@2025-07-01' = {
  name: 'job-${prefix}-orchestrator'
  location: location
  tags: union(tags, { workload: 'orchestrator' })
  identity: {
    type: 'UserAssigned'
    userAssignedIdentities: { '${identityIds.orchestrator}': {} }
  }
  properties: {
    environmentId: environmentResource.id
    workloadProfileName: 'Consumption'
    configuration: {
      triggerType: 'Schedule'
      replicaTimeout: 300
      replicaRetryLimit: 1
      scheduleTriggerConfig: {
        cronExpression: '*/5 * * * *'
        parallelism: 1
        replicaCompletionCount: 1
      }
      registries: [{ server: registryServer, identity: identityIds.orchestrator }]
    }
    template: {
      containers: [
        {
          name: 'orchestrator'
          image: orchestratorImage
          resources: { cpu: json('0.25'), memory: '0.5Gi' }
          env: concat(commonEnv, [
            { name: 'AZURE_CLIENT_ID', value: identityClientIds.orchestrator }
            { name: 'QUEUE_ENDPOINT', value: queueEndpoint }
            { name: 'TASK_QUEUE', value: 'agent-tasks' }
            { name: 'API_BASE_URL', value: 'https://${api.properties.configuration.ingress.fqdn}' }
            { name: 'API_AUDIENCE', value: 'api://${entraClientId}' }
          ])
        }
      ]
    }
  }
}

resource ledgerVerify 'Microsoft.App/jobs@2025-07-01' = {
  name: 'job-${prefix}-ledger-verify'
  location: location
  tags: union(tags, { workload: 'ledger-verify' })
  identity: {
    type: 'UserAssigned'
    userAssignedIdentities: { '${identityIds.api}': {} }
  }
  properties: {
    environmentId: environmentResource.id
    workloadProfileName: 'Consumption'
    configuration: {
      triggerType: 'Schedule'
      replicaTimeout: 900
      replicaRetryLimit: 0
      scheduleTriggerConfig: {
        cronExpression: '0 2 * * *'
        parallelism: 1
        replicaCompletionCount: 1
      }
      registries: [{ server: registryServer, identity: identityIds.api }]
    }
    template: {
      containers: [
        {
          name: 'ledger-verify'
          image: apiImage
          command: ['python', '-m', 'zava_forward.orchestrator.digest_blob', '--publish']
          resources: { cpu: json('0.5'), memory: '1Gi' }
          env: concat(commonEnv, [
            { name: 'AZURE_CLIENT_ID', value: identityClientIds.api }
            { name: 'ZF_STORE', value: 'mssql' }
            { name: 'ZF_SQL_SERVER', value: sqlServerFqdn }
            { name: 'ZF_SQL_DATABASE', value: sqlDatabaseName }
            { name: 'ZF_SQL_AUTH', value: 'msi' }
            { name: 'ZF_SQL_CLIENT_ID', value: identityClientIds.api }
            { name: 'ZF_DIGEST_ACCOUNT_URL', value: blobEndpoint }
            { name: 'ZF_DIGEST_CONTAINER', value: 'ledger-digests' }
            { name: 'ZF_DIGEST_CLIENT_ID', value: identityClientIds.api }
            { name: 'ZF_DIGEST_DIR', value: '/tmp/digests' }
          ])
        }
      ]
    }
  }
}

resource importJob 'Microsoft.App/jobs@2025-07-01' = {
  name: 'job-${prefix}-import'
  location: location
  tags: union(tags, { workload: 'import' })
  identity: {
    type: 'UserAssigned'
    userAssignedIdentities: { '${identityIds.import}': {} }
  }
  properties: {
    environmentId: environmentResource.id
    workloadProfileName: 'Consumption'
    configuration: {
      triggerType: 'Event'
      replicaTimeout: 900
      replicaRetryLimit: 1
      eventTriggerConfig: {
        parallelism: 1
        replicaCompletionCount: 1
        scale: {
          minExecutions: 0
          maxExecutions: 2
          pollingInterval: 30
          rules: [
            {
              name: 'import-queue'
              type: 'azure-queue'
              metadata: {
                accountName: storageAccountName
                queueName: 'import-jobs'
                queueLength: '1'
                cloud: 'AzurePublicCloud'
              }
              identity: identityIds.import
            }
          ]
        }
      }
      registries: [{ server: registryServer, identity: identityIds.import }]
    }
    template: {
      containers: [
        {
          name: 'import'
          image: importImage
          resources: { cpu: json('0.5'), memory: '1Gi' }
          env: concat(commonEnv, [
            { name: 'AZURE_CLIENT_ID', value: identityClientIds.import }
            { name: 'SQL_SERVER', value: sqlServerFqdn }
            { name: 'SQL_DATABASE', value: sqlDatabaseName }
            { name: 'BLOB_ENDPOINT', value: blobEndpoint }
            { name: 'QUEUE_ENDPOINT', value: queueEndpoint }
            { name: 'IMPORT_QUEUE', value: 'import-jobs' }
          ])
        }
      ]
    }
  }
}

output environmentId string = environmentResource.id
output environmentName string = environmentResource.name
output apiFqdn string = api.properties.configuration.ingress.fqdn
output apiName string = api.name
output apiId string = api.id
output ledgerVerifyJobName string = ledgerVerify.name
