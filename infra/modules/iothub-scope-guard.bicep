@minLength(1)
@description('Must not be empty. Empty means the target resource group is not ama; never create or delete a resource group for this module.')
param resourceGroupMustBeAma string

@minLength(1)
@description('Must not be empty. Empty means the primary IoT location is not uksouth.')
param iotLocationMustBeUKSouth string

output checked array = [
  resourceGroupMustBeAma
  iotLocationMustBeUKSouth
]
