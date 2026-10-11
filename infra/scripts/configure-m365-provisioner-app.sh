#!/usr/bin/env bash
# Adds the Microsoft Graph delegated permissions the SharePoint evidence site and Teams alert
# channel set-up needs to an existing public-client app registration (the one the m365 CLI signs
# in with), and optionally grants tenant-wide admin consent.
#
# Runtime access does not need any of this. The workbench API identity gets only the
# application permission Sites.Selected plus a grant on one site (grant-sharepoint-access.sh).
# Teams alerts use a Workflows webhook URL, which needs no Graph permission and cannot be
# created through Graph; create it in the channel (Workflows, "Post to a channel when a webhook
# request is received") and pass it as teamsWebhookUrl.
#
# Run as a Global Administrator or Privileged Role Administrator:
#   az login --tenant <tenant> --allow-no-subscriptions
# Usage: configure-m365-provisioner-app.sh <app-client-id> [--consent]
set -euo pipefail
app_id=${1:?usage: configure-m365-provisioner-app.sh <app-client-id> [--consent]}
consent=${2:-}

# Delegated permissions and what each is for:
#   Sites.FullControl.All            POST /sites/{id}/permissions, to scope the API identity to one site (the only permission Graph accepts for this call)
#   Team.Create                      create the exercise team, which also provisions its SharePoint site
#   Channel.Create                   create the alerts channel
#   AppRoleAssignment.ReadWrite.All  assign the Sites.Selected app role to the API managed identity
#   Application.Read.All             look up service principals and app role ids
scopes=(Sites.FullControl.All Team.Create Channel.Create AppRoleAssignment.ReadWrite.All Application.Read.All)
graph_app=00000003-0000-0000-c000-000000000000
graph_sp=$(az ad sp show --id $graph_app --query id -o tsv)

for scope in "${scopes[@]}"; do
  id=$(az ad sp show --id $graph_app --query "oauth2PermissionScopes[?value=='$scope'].id | [0]" -o tsv)
  [[ -n $id ]] || { echo "unknown Graph scope $scope" >&2; exit 1; }
  az ad app permission add --id "$app_id" --api $graph_app --api-permissions "$id=Scope" -o none
  echo "requested $scope"
done

if [[ $consent == --consent ]]; then
  client_sp=$(az ad sp show --id "$app_id" --query id -o tsv)
  granted=$(printf '%s ' "${scopes[@]}")
  existing=$(az rest --method GET \
    --url "https://graph.microsoft.com/v1.0/oauth2PermissionGrants?\$filter=clientId eq '$client_sp' and resourceId eq '$graph_sp'" \
    --query "value[0].id" -o tsv)
  if [[ -n $existing ]]; then
    current=$(az rest --method GET --url "https://graph.microsoft.com/v1.0/oauth2PermissionGrants/$existing" --query scope -o tsv)
    merged=$(echo "$current $granted" | tr ' ' '\n' | sort -u | grep . | tr '\n' ' ')
    az rest --method PATCH --url "https://graph.microsoft.com/v1.0/oauth2PermissionGrants/$existing" \
      --body "{\"scope\":\"$merged\"}" -o none
  else
    az rest --method POST --url "https://graph.microsoft.com/v1.0/oauth2PermissionGrants" \
      --body "{\"clientId\":\"$client_sp\",\"consentType\":\"AllPrincipals\",\"resourceId\":\"$graph_sp\",\"scope\":\"User.Read $granted\"}" -o none
  fi
  echo "admin consent recorded"
else
  echo "permissions requested but not consented; re-run with --consent or grant them in the Entra portal"
fi
