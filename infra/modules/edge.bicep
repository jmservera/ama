// WARNING (open item): Private Link to groupId 'managedEnvironments' of an internal, VNet-injected Container Apps
// environment is unverified for this configuration. Confirm in a production-profile deployment that the pending
// private endpoint connection appears and the origin becomes healthy before relying on enablePublicEdge.
// Public edge: Front Door Premium, WAF policy and a Private Link origin to the internal Container Apps environment
// (ADR 0002 decision 6, issue 143). Deployed only when enablePublicEdge is true in the production profile.
param prefix string
param tags object
@description('Container Apps environment resource ID used as the Private Link origin target.')
param environmentId string
@description('Internal FQDN of the API Container App; the origin host name and host header.')
param originHostName string
@description('Azure region for the Private Link request (the environment region).')
param privateLinkLocation string
@description('Optional custom domain (managed certificate). Empty uses the default azurefd.net endpoint. Ordering: the domain is attached to the route and WAF in the same deployment, but a managed certificate stays Pending until the owner creates the _dnsauth TXT validation record and the CNAME to the endpoint; traffic on the custom host does not work before that. Deploy without a domain first, or expect the domain to validate after deployment.')
param customDomain string = ''
@description('Detection logs only until false positives are reviewed against the synthetic pilot traffic; Prevention is the target.')
@allowed(['Detection', 'Prevention'])
param wafMode string = 'Prevention'
param workspaceId string

var wafName = replace('waf${prefix}', '-', '')
var hasDomain = !empty(customDomain)

resource profile 'Microsoft.Cdn/profiles@2024-09-01' = {
  name: 'afd-${prefix}'
  location: 'global'
  tags: tags
  sku: { name: 'Premium_AzureFrontDoor' }
}

resource waf 'Microsoft.Network/FrontDoorWebApplicationFirewallPolicies@2024-02-01' = {
  name: wafName
  location: 'global'
  tags: tags
  sku: { name: 'Premium_AzureFrontDoor' }
  properties: {
    policySettings: {
      enabledState: 'Enabled'
      mode: wafMode
      requestBodyCheck: 'Enabled'
    }
    managedRules: {
      managedRuleSets: [
        { ruleSetType: 'Microsoft_DefaultRuleSet', ruleSetVersion: '2.1', ruleSetAction: 'Block' }
        { ruleSetType: 'Microsoft_BotManagerRuleSet', ruleSetVersion: '1.1' }
      ]
    }
  }
}

resource endpoint 'Microsoft.Cdn/profiles/afdEndpoints@2024-09-01' = {
  parent: profile
  name: 'ep-${prefix}'
  location: 'global'
  tags: tags
  properties: { enabledState: 'Enabled' }
}

resource domain 'Microsoft.Cdn/profiles/customDomains@2024-09-01' = if (hasDomain) {
  parent: profile
  name: 'cd-${prefix}'
  properties: {
    hostName: customDomain
    tlsSettings: { certificateType: 'ManagedCertificate', minimumTlsVersion: 'TLS12' }
  }
}

resource originGroup 'Microsoft.Cdn/profiles/originGroups@2024-09-01' = {
  parent: profile
  name: 'og-api'
  properties: {
    loadBalancingSettings: { sampleSize: 4, successfulSamplesRequired: 3 }
    healthProbeSettings: { probePath: '/', probeRequestType: 'HEAD', probeProtocol: 'Https', probeIntervalInSeconds: 100 }
  }
}

resource origin 'Microsoft.Cdn/profiles/originGroups/origins@2024-09-01' = {
  parent: originGroup
  name: 'api'
  properties: {
    hostName: originHostName
    originHostHeader: originHostName
    httpsPort: 443
    enforceCertificateNameCheck: true
    sharedPrivateLinkResource: {
      privateLink: { id: environmentId }
      groupId: 'managedEnvironments'
      privateLinkLocation: privateLinkLocation
      requestMessage: 'Front Door Premium private origin for ${prefix}'
    }
  }
}

resource route 'Microsoft.Cdn/profiles/afdEndpoints/routes@2024-09-01' = {
  parent: endpoint
  name: 'route-api'
  dependsOn: [origin]
  properties: {
    originGroup: { id: originGroup.id }
    customDomains: hasDomain ? [{ id: domain.id }] : []
    supportedProtocols: ['Https']
    httpsRedirect: 'Enabled'
    forwardingProtocol: 'HttpsOnly'
    linkToDefaultDomain: 'Enabled'
  }
}

resource securityPolicy 'Microsoft.Cdn/profiles/securityPolicies@2024-09-01' = {
  parent: profile
  name: 'sp-waf'
  properties: {
    parameters: {
      type: 'WebApplicationFirewall'
      wafPolicy: { id: waf.id }
      associations: [
        {
          domains: concat([{ id: endpoint.id }], hasDomain ? [{ id: domain.id }] : [])
          patternsToMatch: ['/*']
        }
      ]
    }
  }
}

resource diagnostics 'Microsoft.Insights/diagnosticSettings@2021-05-01-preview' = {
  scope: profile
  name: 'to-log-analytics'
  properties: {
    workspaceId: workspaceId
    logs: [
      { category: 'FrontDoorAccessLog', enabled: true }
      { category: 'FrontDoorWebApplicationFirewallLog', enabled: true }
    ]
  }
}

output endpointHostName string = endpoint.properties.hostName
output publicHostName string = hasDomain ? customDomain : endpoint.properties.hostName
output entraRedirectUri string = 'https://${hasDomain ? customDomain : endpoint.properties.hostName}/.auth/login/aad/callback'
