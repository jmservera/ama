@minLength(1)
@description('Empty refuses staff restart permission outside ama or for a non-initializer identity.')
param approvedScope string

output checked string = approvedScope
