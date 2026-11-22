#!/usr/bin/env bash
# usage: mk-live.sh N slug "goal text"
# Creates an isolated worktree and branch from origin/main, writes a fresh brief, records the
# phase-witness launch and starts the worker in the tmux session rpi-N-live.
set -e
N=$1; SLUG=$2; GOAL=$3; ST=$(date -u +%Y%m%dT%H%M%SZ)
C=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)
REPO=$(cd "$C/../.." && pwd)
WTROOT=${AMA_WT_ROOT:-$HOME/source/ama-wt}
cd "$REPO"
git fetch -q origin main
WT=$WTROOT/issue-$N-live-$ST
EV=$HOME/.local/share/ama/phase-witness/$N-live-$ST
BR=test/$SLUG-live-$ST
git worktree add -q "$WT" -b "$BR" origin/main
git -C "$WT" config --local user.email 8036360+jmservera@users.noreply.github.com
git -C "$WT" config --local user.name jmservera
mkdir -p "$EV"
B=/tmp/brief-$N-live-$ST.md
STATE=$WT/.copilot-tracking/rpi-sessions/$(date -u +%F)/issue-$N-live-state.json
cat > "$B" <<EOT
Run the full RPI loop (research, critique, plan, implement, review) for GitHub issue #$N, using agent hve-core-all:rpi-agent. Separate dated artifacts are required even if no source changes.
First read $C/brief-common.md and obey it (including phase witness calls).
Goal: $GOAL
Owner decisions 2026-11-18 (authoritative): this is the synthetic DEMO, desktop only. Live Azure is authorised (resource group ama, cap USD 700, no drills, no Key Vault rotation, no production changes). Azure billing reconciliation, DPO/Legal approval and person-run assistive-technology testing are NOT needed for the demo. Sign-in credentials are in ~/.ama-test-user, ~/.ama-test-user-id, ~/.ama-resident-test-user: read at runtime, NEVER print, echo or cat them. Use the Azure CLI with the existing login; apps: ca-cutover-test-demo-api, ca-resident-demo. Delete any throwaway resource you create. Use Playwright for browser proofs.
For each unticked acceptance criterion in the issue: prove it with recorded evidence (commands, outputs without secrets, screenshots) in a research note under docs/reference/research/, or state precisely why it cannot be proven for the demo. Tier FULL only if you change src code; never run rpi-checks.py --all.
Worktree: $WT ; branch $BR ; session rpi-$N-live ; evidence dir $EV ; state file $STATE.
Never push or open PRs. Return a clean frozen local commit with a per-criterion proven/unproven table in the changes record. Refs #$N.
EOT
python3 tools/rpi_phase_witness.py record launch --repo "$WT" --issue "$N" --evidence-dir "$EV" --brief "$B" --session "rpi-$N-live" --actor coordinator --claim-model claude-sonnet-5.5
tmux new-session -d -s "rpi-$N-live" -c "$WT" "bash $C/launch.sh rpi-$N-live $ST $B claude-sonnet-5.5"
echo "launched rpi-$N-live"
