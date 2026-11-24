#!/usr/bin/env bash
# Tune how warm the demo Container Apps stay. Jobs are never touched.
#
#   tools/demo-scale.sh status               show min/max replicas and cooldown per app
#   tools/demo-scale.sh min 1|0 [--dry-run]  set the minimum replicas of every app
#   tools/demo-scale.sh cooldown SECONDS     set the idle time before scale-to-zero (0-3600)
#
# `min 1` keeps the demo warm at a small constant cost; `min 0` saves cost. With min 0 a longer
# cooldown (up to 3600 s) keeps an app warm for an hour after its last request.
# Environment: ZF_RESOURCE_GROUP (default ama). Needs `az login`.
set -euo pipefail

usage() { sed -n '2,10p' "$0" | sed 's/^# \{0,1\}//'; exit "${1:-2}"; }

[ $# -ge 1 ] || usage
cmd=$1
shift
rg=${ZF_RESOURCE_GROUP:-ama}
sub=$(az account show --query id -o tsv)
dry=0
value=""
for arg in "$@"; do
  case "$arg" in
    --dry-run) dry=1 ;;
    -h | --help) usage 0 ;;
    *) value=$arg ;;
  esac
done

list_apps() {
  az containerapp list -g "$rg" -o tsv 2>/dev/null \
    --query "[].[name, properties.template.scale.minReplicas, properties.template.scale.maxReplicas, properties.template.scale.cooldownPeriod]"
}

case "$cmd" in
  status)
    printf '%-34s %4s %4s %9s\n' app min max cooldown
    list_apps | while IFS=$'\t' read -r name min max cool; do
      printf '%-34s %4s %4s %9s\n' "$name" "${min:-0}" "${max:-?}" "${cool:-300}"
    done
    exit 0
    ;;
  min)
    [[ "$value" =~ ^[01]$ ]] || { echo "min must be 0 or 1" >&2; exit 2; }
    ;;
  cooldown)
    [[ "$value" =~ ^[0-9]+$ ]] && [ "$value" -le 3600 ] || { echo "cooldown must be 0-3600" >&2; exit 2; }
    ;;
  -h | --help) usage 0 ;;
  *) usage ;;
esac

failed=0
while IFS=$'\t' read -r name min max cool; do
  [ -n "$name" ] || continue
  if [ "$cmd" = min ]; then
    args=(az containerapp update -g "$rg" -n "$name" --min-replicas "$value")
    # A maximum below the new minimum is invalid, so raise it.
    [ "${max:-0}" -ge "$value" ] || args+=(--max-replicas "$value")
  else
    url="https://management.azure.com/subscriptions/$sub/resourceGroups/$rg/providers/Microsoft.App/containerApps/$name?api-version=2025-01-01"
    args=(az rest --method patch --url "$url" --body "{\"properties\":{\"template\":{\"scale\":{\"cooldownPeriod\":$value}}}}")
  fi
  if [ "$dry" = 1 ]; then echo "dry-run  ${args[*]}"; continue; fi
  if "${args[@]}" -o none >/dev/null 2>&1; then echo "updated  $name ($cmd $value)"; else echo "FAILED   $name" >&2; failed=1; fi
done < <(list_apps)
exit "$failed"
