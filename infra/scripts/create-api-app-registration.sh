#!/usr/bin/env bash
# Creates (idempotently) the single-tenant Entra app registration that protects the workbench
# API through Container Apps built-in authentication, with the app roles the MVP maps to
# workbench roles (src/api/src/zava_forward/api/auth.py DEFAULT_ROLE_MAP).
#
# Run as a user who can create applications (Application Administrator or Global Administrator).
# Sign in first with: az login --tenant <tenant> --allow-no-subscriptions
#
# Usage: create-api-app-registration.sh [options]
#   -n NAME      display name (default zava-forward-api)
#   -u URL       base URL of the API, adds the built-in auth redirect URI (repeatable)
#   -a UPN:ROLE  assign a user to an app role, for example admin@contoso.com:ProgrammeManager (repeatable)
#   -v VAULT     store a new client secret in this Key Vault as entra-client-secret
# The secret is written with the Azure CLI session in KV_AZURE_CONFIG_DIR when set (for a vault
# the app administrator cannot reach), otherwise the current session. It is never printed.
# Prints the application (client) id on stdout.
set -euo pipefail

name=zava-forward-api vault="" urls=() assigns=()
while getopts "n:u:a:v:" opt; do
  case $opt in
    n) name=$OPTARG ;;
    u) urls+=("${OPTARG%/}") ;;
    a) assigns+=("$OPTARG") ;;
    v) vault=$OPTARG ;;
    *) exit 2 ;;
  esac
done

roles=(
  "Coordinator|Retrofit Coordinator"
  "LiaisonOfficer|Resident Liaison Officer"
  "SafetyLiaison|Building Safety Liaison"
  "GrantsOfficer|Grants and Evidence Officer"
  "QualityInspector|Quality Inspector"
  "ProgrammeManager|Retrofit Programme Manager"
  "SupportOfficer|Programme Support Officer"
  "Contractor|Contractor"
  "RuleAuthor|Regulatory rule author"
  "RuleOwner|Regulatory named owner"
  "RegulatoryChat|Regulatory chat user"
)
roles_json=$(python3 - "${roles[@]}" <<'PY'
import json, sys, uuid
ns = uuid.UUID("6f1d0c5e-6a0e-4c43-9a55-0c8f7a1b2d34")  # stable ids so a re-run does not replace roles
out = []
for item in sys.argv[1:]:
    key, label = item.split("|")
    out.append({"id": str(uuid.uuid5(ns, key)), "displayName": label, "description": f"Zava Forward workbench: {label}",
                "value": f"ZavaForward.{key}", "isEnabled": True, "allowedMemberTypes": ["User"]})
print(json.dumps(out))
PY
)

app_id=$(az ad app list --display-name "$name" --query "[0].appId" -o tsv)
if [[ -z $app_id ]]; then
  app_id=$(az ad app create --display-name "$name" --sign-in-audience AzureADMyOrg --enable-id-token-issuance true \
    --query appId -o tsv)
fi
object_id=$(az ad app show --id "$app_id" --query id -o tsv)

redirects=$(python3 - "${urls[@]:-}" <<'PY'
import json, sys
print(json.dumps([f"{u}/.auth/login/aad/callback" for u in sys.argv[1:] if u]))
PY
)
body=$(python3 - "$app_id" "$roles_json" "$redirects" <<'PY'
import json, sys
app_id, roles, redirects = sys.argv[1], json.loads(sys.argv[2]), json.loads(sys.argv[3])
body = {"identifierUris": [f"api://{app_id}"], "appRoles": roles,
        "api": {"requestedAccessTokenVersion": 2},
        "web": {"redirectUris": redirects, "implicitGrantSettings": {"enableIdTokenIssuance": True}}}
print(json.dumps(body))
PY
)
az rest --method PATCH --url "https://graph.microsoft.com/v1.0/applications/$object_id" --body "$body" -o none

sp_id=$(az ad sp list --filter "appId eq '$app_id'" --query "[0].id" -o tsv)
[[ -n $sp_id ]] || sp_id=$(az ad sp create --id "$app_id" --query id -o tsv)
# Only users with an assigned app role can sign in.
az rest --method PATCH --url "https://graph.microsoft.com/v1.0/servicePrincipals/$sp_id" \
  --body '{"appRoleAssignmentRequired": true}' -o none

for entry in "${assigns[@]:-}"; do
  [[ -n $entry ]] || continue
  upn=${entry%%:*} role=${entry##*:}
  user_id=$(az ad user show --id "$upn" --query id -o tsv)
  role_id=$(python3 -c "import json,sys;print(next(r['id'] for r in json.loads(sys.argv[1]) if r['value']=='ZavaForward.'+sys.argv[2]))" "$roles_json" "$role")
  az rest --method POST --url "https://graph.microsoft.com/v1.0/users/$user_id/appRoleAssignments" \
    --body "{\"principalId\":\"$user_id\",\"resourceId\":\"$sp_id\",\"appRoleId\":\"$role_id\"}" -o none 2>/dev/null \
    || echo "role $role already assigned to $upn or could not be assigned" >&2
done

if [[ -n $vault ]]; then
  az ad app credential reset --id "$app_id" --append --display-name "container-apps-auth" --years 1 \
    --query password -o tsv \
    | tr -d '\n' \
    | AZURE_CONFIG_DIR=${KV_AZURE_CONFIG_DIR:-${AZURE_CONFIG_DIR:-$HOME/.azure}} \
      az keyvault secret set --vault-name "$vault" --name entra-client-secret --file /dev/stdin --encoding utf-8 -o none
fi
echo "$app_id"
