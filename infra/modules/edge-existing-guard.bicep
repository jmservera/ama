@minLength(1)
@description('Requires an existing internal environment with public network access disabled.')
param privateEnvironment string
@minLength(1)
@description('Requires an enabled Entra-authenticated API in the specified environment. This is not verification of tenant registration, credentials or staff.')
param authenticatedOrigin string

@minLength(1)
@description('Requires an Entra application clientId in hexadecimal UUID form, not systemAssignedIdentity. Run python3 infra/scripts/setup-entra.py before deploying this edge. UUID syntax alone does not verify registration, credentials or human sign-in.')
param registeredClient string

output checked array = [privateEnvironment, authenticatedOrigin, registeredClient]
