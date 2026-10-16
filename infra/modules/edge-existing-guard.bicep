@minLength(1)
@description('Requires an existing internal environment with public network access disabled.')
param privateEnvironment string
@minLength(1)
@description('Requires an enabled Entra-authenticated API in the specified environment. This is not verification of tenant registration, credentials or staff.')
param authenticatedOrigin string

output checked array = [privateEnvironment, authenticatedOrigin]
