// Parameter guard (the outputs only reference the parameters). Each minLength constraint fails template validation, before
// any resource changes, with a message that names the unsupported combination.
@minLength(1)
@description('Must not be empty. Empty means the production profile was combined with allowPublicNetworkAccess=true; use deploymentProfile=development for a reachable throwaway stack.')
param productionProfileForbidsPublicNetworkAccess string

@minLength(1)
@description('Must not be empty. Empty means the production profile was combined with keyVaultPurgeProtection=false.')
param productionProfileRequiresKeyVaultPurgeProtection string

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

output checked array = [
  pilotRequiresProductionProfile
  publicEdgeRequiresProductionProfile
  publicEdgeRequiresApplications
  productionProfileForbidsPublicNetworkAccess
  productionProfileRequiresKeyVaultPurgeProtection
  sharePointEvidenceStoreRequiresSiteId
  tokenStoreReadyRequiresTokenStore
  entraRoleMapRequiresEntraClientId
  bearerOnlyRequiresAudience
]
