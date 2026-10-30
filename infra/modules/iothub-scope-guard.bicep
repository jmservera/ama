@minLength(1)
@description('Must not be empty. Empty means the target resource group is not ama; never create or delete a resource group for this module.')
param resourceGroupMustBeAma string

@minLength(1)
@description('Must not be empty. Empty means the primary IoT location is not uksouth.')
param iotLocationMustBeUKSouth string

@minLength(1)
@description('Standalone reconciliation verifies the actual existing B1 hub before child writes.')
param existingHubSkuMustMatch string = 'not-applicable'

@minLength(1)
param existingHubUnitsMustMatch string = 'not-applicable'

output checked array = [
  resourceGroupMustBeAma
  iotLocationMustBeUKSouth
  existingHubSkuMustMatch
  existingHubUnitsMustMatch
]
