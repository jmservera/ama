#!/bin/bash
# Stream replica logs of the running job-live-receiver execution until it ends. No secrets are touched.
cd "$(dirname "$0")"
G=ama; J=job-live-receiver
for i in $(seq 1 400); do
  ex=$(az containerapp job execution list -g $G -n $J --query "[?properties.status=='Running'].name | [0]" -o tsv 2>/dev/null)
  if [ -n "$ex" ] && [ "$ex" != "None" ]; then
    rep=$(az containerapp job replica list -g $G -n $J --execution $ex --query "[0].name" -o tsv 2>/dev/null)
    if [ -n "$rep" ] && [ "$rep" != "None" ]; then
      timeout 100 az containerapp job logs show -g $G -n $J --execution $ex --replica $rep --container live-receiver --format text --follow 2>/dev/null | grep -v WARN >> "watch-$ex.txt"
    fi
    seen=1
  elif [ "$seen" = 1 ]; then break; fi
  az containerapp job execution list -g $G -n $J --query "[0:4].{n:name,s:properties.status,st:properties.startTime,e:properties.endTime}" -o tsv 2>/dev/null > receiver-executions-latest.tsv
  sleep 8
done
az containerapp job execution list -g $G -n $J --query "[0:4].{n:name,s:properties.status,st:properties.startTime,e:properties.endTime}" -o tsv 2>/dev/null > receiver-executions-latest.tsv
