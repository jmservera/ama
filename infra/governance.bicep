targetScope = 'subscription'

@description('Short workload prefix used in assignment names.')
param workload string = 'forward'

@description('Set to true only after the subscription owner has accepted the Defender plan cost in infra/README.md (Governance controls). False leaves every plan on Free.')
param enableDefenderPlans bool = false

@description('Defender for Cloud plans decided for the demonstrator. Each name is a Microsoft.Security/pricings plan.')
param defenderPlans array = [
  'StorageAccounts'
  'SqlServers'
  'KeyVaults'
  'Containers'
]

@description('Default audits and reports. DoNotEnforce keeps policy in audit mode so a policy never blocks the exercise; Default with a Deny effect is an owner decision.')
@allowed(['Default', 'DoNotEnforce'])
param enforcementMode string = 'DoNotEnforce'

@description('Tag names every resource must carry. Mirrors allTags in main.bicep.')
param requiredTags array = [
  'workload'
  'environment'
  'dataClassification'
  'owner'
]

var policyDefinitionRoot = '/providers/Microsoft.Authorization/policyDefinitions'

var builtInAssignments = [
  {
    key: 'sql-no-public'
    displayName: 'Public network access on Azure SQL Database should be disabled'
    definitionId: '1b8ca024-1d5c-4dec-8995-b1a932b41780'
  }
  {
    key: 'storage-no-public'
    displayName: 'Storage accounts should disable public network access'
    definitionId: 'b2982f36-99f2-4db5-8eff-283140c09693'
  }
  {
    key: 'kv-purge-protect'
    displayName: 'Key vaults should have deletion protection enabled'
    definitionId: '0b60c0b2-2dc2-4e1c-b5c9-abbed971de53'
  }
]

resource builtIn 'Microsoft.Authorization/policyAssignments@2024-04-01' = [for item in builtInAssignments: {
  name: '${workload}-${item.key}'
  properties: {
    displayName: item.displayName
    policyDefinitionId: '${subscription().id}${policyDefinitionRoot}/${item.definitionId}'
    enforcementMode: enforcementMode
    metadata: { owner: 'Juan Manuel Servera', issue: 'jmservera/ama#147' }
  }
}]

resource requireTag 'Microsoft.Authorization/policyAssignments@2024-04-01' = [for tagName in requiredTags: {
  name: '${workload}-tag-${toLower(tagName)}'
  properties: {
    displayName: 'Require tag ${tagName} on resource groups'
    policyDefinitionId: '${subscription().id}${policyDefinitionRoot}/96670d01-0a4d-4649-9c89-2d3abc0a5025'
    enforcementMode: enforcementMode
    parameters: { tagName: { value: tagName } }
    metadata: { owner: 'Juan Manuel Servera', issue: 'jmservera/ama#147' }
  }
}]

resource defender 'Microsoft.Security/pricings@2024-01-01' = [for plan in defenderPlans: {
  name: plan
  properties: {
    pricingTier: enableDefenderPlans ? 'Standard' : 'Free'
  }
}]
