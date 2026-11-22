#!/usr/bin/env bash
# usage: launch.sh NAME STAMP BRIEF_PATH MODEL   (MODEL "automatic" omits --model)
name=$1 stamp=$2 brief=$3 model=$4
log=/tmp/$name.log
echo "--- launch $stamp" >> "$log"
[ "$model" = automatic ] && model_args=() || model_args=(--model "$model")
copilot --agent hve-core-all:rpi-agent "${model_args[@]}" \
  --allow-all-tools --allow-all-paths --deny-tool 'shell(git push --force)' \
  -p "$(cat "$brief")" 2>&1 | tee -a "$log"
status=${PIPESTATUS[0]}
echo "exit=$status" >> "$log"
exit "$status"
