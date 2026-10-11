#!/usr/bin/env bash
# Grants the workbench API managed identity read/write on ONE SharePoint site
# (Sites.Selected), instead of tenant-wide Sites access.
# Needs a Global/Privileged Role Administrator and SharePoint admin consent.
# Usage: grant-sharepoint-access.sh <api-identity-principal-id> <site-id> <read|write>
set -euo pipefail
principal=$1 site=$2 role=${3:-write}
client=$(az ad sp show --id "$principal" --query appId -o tsv)
graph=$(az ad sp show --id 00000003-0000-0000-c000-000000000000 --query id -o tsv)
# Sites.Selected application permission on Microsoft Graph
role_id=883ea226-0bf2-4a8f-9f9e-0fc2f2b7e5c4
az rest --method POST --url "https://graph.microsoft.com/v1.0/servicePrincipals/$principal/appRoleAssignments" \
  --body "{\"principalId\":\"$principal\",\"resourceId\":\"$graph\",\"appRoleId\":\"$role_id\"}"
# Scope the grant to the single site
az rest --method POST --url "https://graph.microsoft.com/v1.0/sites/$site/permissions" \
  --body "{\"roles\":[\"$role\"],\"grantedToIdentities\":[{\"application\":{\"id\":\"$client\",\"displayName\":\"zava-forward-api\"}}]}"
