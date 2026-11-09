<!-- markdownlint-disable-file -->
# PR 1295 CxO story PowerShell validation phase details (2026-11-09, prospective)

Plan: [plan](../../plans/2026-11-09/pr-1295-cxo-story-validation-plan.md).

## Phase 1: Build and Verify

* `PS=~/.local/ama-tools/powershell/7.6.9/pwsh`; `Run=$(mktemp -d /tmp/ama-capstone-val-XXXXXX)`.
* `$PS -NoLogo -NoProfile -File tools/capstone/Invoke-Capstone.ps1 -Action Build -RepoRoot "$PWD" -OutputDir "$Run/build"` then `-Action Verify` with the same flags and a fresh output directory.
* Success: exit 0, report with 54 slides and 54 notes, and an unchanged tracked tree.

## Phase 2: Guards

* `Test-CostStatus.ps1 -RepoRoot "$PWD" -CandidatePath "$Run/build/zava-forward-cowork-v2-draft.pptx"`.
* `Test-SourceHashes.ps1 -RepoRoot "$PWD" -SemanticOnly`, then default mode.
* `Test-NativeShapes.ps1 -RepoRoot "$PWD"`.

## Phase 3 and 4

Record exits and output counts. Run `git status --short` to confirm no tracked or untracked change besides new tracking records. Independent coordinator review of the exact head follows.
