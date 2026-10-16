param apiName string
@description('Non-secret auth configuration read from the existing API. Preserve provider validation, exclusions, token storage and credential references.')
param currentAuth object
param entraBearerOnly bool = false

resource api 'Microsoft.App/containerApps@2025-07-01' existing = {
  name: apiName
}

resource auth 'Microsoft.App/containerApps/authConfigs@2025-07-01' = {
  parent: api
  name: 'current'
  properties: union(currentAuth, {
    httpSettings: union(currentAuth.httpSettings, {
      requireHttps: true
      forwardProxy: {
        convention: 'Custom'
        customHostHeaderName: 'X-Forwarded-Host'
        customProtoHeaderName: 'X-Forwarded-Proto'
      }
    })
    globalValidation: union(currentAuth.globalValidation, {
      unauthenticatedClientAction: entraBearerOnly ? 'Return401' : 'RedirectToLoginPage'
      redirectToProvider: 'azureactivedirectory'
    })
  })
}
