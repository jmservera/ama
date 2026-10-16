// Parameter guard (the outputs only reference the parameters). Each minLength constraint fails template validation, before
// any resource changes, with a message that names the unsupported combination.
@minLength(1)
@description('Must not be empty. Empty means the production profile was combined with allowPublicNetworkAccess=true; use deploymentProfile=development for a reachable throwaway stack.')
param productionProfileForbidsPublicNetworkAccess string

@minLength(1)
@description('Must not be empty. Empty means the production profile was combined with keyVaultPurgeProtection=false.')
param productionProfileRequiresKeyVaultPurgeProtection string

@minLength(1)
@description('Must not be empty. Empty means production was combined with registryQuarantineEnabled=false.')
param productionProfileRequiresRegistryQuarantine string

@minLength(1)
@description('Must not be empty. Empty means regionCheckReference is missing; record a dated capability check for the selected regions first.')
param regionCheckMustBeRecorded string

@minLength(1)
@description('Must not be empty. Empty means quotaCheckReference is missing; record a dated quota check for the selected configuration first.')
param quotaCheckMustBeRecorded string

@minLength(1)
@description('Must not be empty. Empty means location or sqlLocation is still an unresolved owner placeholder.')
param deploymentLocationsMustBeSelected string

@minLength(1)
@description('Must not be empty. Empty means evidenceStore=sharepoint without sharePointSiteId.')
param sharePointEvidenceStoreRequiresSiteId string

@minLength(1)
@description('Must not be empty. Empty means entraTokenStoreReady=true without enableEntraTokenStore=true.')
param tokenStoreReadyRequiresTokenStore string

@minLength(1)
@description('Must not be empty. Empty means entraRoleMap was set without entraClientId.')
param entraRoleMapRequiresEntraClientId string

@minLength(1)
@description('Must not be empty. Empty means bearer-only authentication lacks entraClientId or enables delegated token storage.')
param bearerOnlyRequiresAudience string

@minLength(1)
@description('Must not be empty. Empty means enablePublicEdge=true in the development profile or with allowPublicNetworkAccess=true; the edge needs the internal production environment.')
param publicEdgeRequiresProductionProfile string

@minLength(1)
@description('Must not be empty. Empty means enablePublicEdge=true without deployApplications=true.')
param publicEdgeRequiresApplications string

@minLength(1)
@description('Must not be empty. Empty means environmentName=pilot with the development profile or allowPublicNetworkAccess=true; the pilot keeps every isolation control.')
param pilotRequiresProductionProfile string

@minLength(1)
@description('Must not be empty. Empty means demoDirectIngress=true without deploymentProfile=development; direct demo ingress is never a production override.')
param demoRequiresDevelopmentProfile string

@minLength(1)
@description('Must not be empty. Empty means demoDirectIngress=true with enablePublicEdge=true; select exactly one ingress mode.')
param demoForbidsPublicEdge string

@minLength(1)
@description('Must not be empty. Empty means demoDirectIngress=true with allowPublicNetworkAccess=true; demo backing services must remain private.')
param demoRequiresPrivateBackingServices string

@minLength(1)
@description('Must not be empty. Empty means demo applications lack entraClientId or use entraBearerOnly=true; shared demos require browser authentication. Environment-only staging may omit the audience.')
param demoRequiresBrowserAuthentication string

output checked array = [
  pilotRequiresProductionProfile
  publicEdgeRequiresProductionProfile
  publicEdgeRequiresApplications
  productionProfileForbidsPublicNetworkAccess
  productionProfileRequiresKeyVaultPurgeProtection
  productionProfileRequiresRegistryQuarantine
  regionCheckMustBeRecorded
  quotaCheckMustBeRecorded
  deploymentLocationsMustBeSelected
  sharePointEvidenceStoreRequiresSiteId
  tokenStoreReadyRequiresTokenStore
  entraRoleMapRequiresEntraClientId
  bearerOnlyRequiresAudience
  demoRequiresDevelopmentProfile
  demoForbidsPublicEdge
  demoRequiresPrivateBackingServices
  demoRequiresBrowserAuthentication
]
