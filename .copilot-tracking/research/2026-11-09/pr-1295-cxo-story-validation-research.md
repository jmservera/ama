<!-- markdownlint-disable-file -->
# PR 1295 CxO story PowerShell validation research (2026-11-09)

Task: `pr-1295-cxo-story-validation`, a bounded continuation of the first recovery [research](pr-1295-cxo-story-recovery-research.md). PR-only lane; no issue mapped. Research disposition: executed. Planning readiness: Ready.

## Identity

* Frozen recovery head `399e31ac14316e05e6be73b49cfcde9de6538ee2`, tree `cdfb1f3ca37fa7e3805ca8e5588a013c2038c10f`, branch `docs/demo-recovery-pr1295-1109`, clean at start.
* PR source head `b671116d571b76ebbbc9e277a791e67f781609cd`. Fetched `origin/main` `b46a9ad9a9619db535368d1b2cbbddec8110e122`.
* The first recovery left Build/Verify, Test-CostStatus, Test-SourceHashes and Test-NativeShapes unrun because `pwsh` was not on PATH. This continuation resolves that prerequisite.

## Tooling guide findings

* [Source guide](../../../docs/capstone/source/README.md) (Linux Preview and Focused regressions): Build uses `pwsh -NoLogo -NoProfile -File tools/capstone/Invoke-Capstone.ps1 -Action Build -RepoRoot "$PWD" -OutputDir <external>`; `Test-NativeShapes.ps1 -RepoRoot` and `Test-SourceHashes.ps1 -RepoRoot` (optional `-SemanticOnly`) are run from the repository root; `Test-CostStatus.ps1 -RepoRoot <root> -CandidatePath <built pptx>` runs against a built candidate. Invoke-Capstone supports `-Action ExportSource|Build|Verify|Render` with mandatory `-RepoRoot` and `-OutputDir`; Render needs native PowerPoint and is out of scope.
* Version requirement: `Invoke-Capstone.ps1`, `Test-CostStatus.ps1` and `Test-SourceHashes.ps1` declare `#Requires -Version 7.4`; `Test-NativeShapes.ps1` requires 5.1. The hosted rubric workflow does not run these scripts, so no workflow pins PowerShell.

## Prerequisite resolution

* No `pwsh` on PATH, in `~/.local/bin`, `/opt` or `/usr/local/bin`; `~/.local/share/powershell` holds only an empty Modules directory.
* Official release resolved from the public GitHub API for `PowerShell/PowerShell` (the authenticated `gh` call is blocked by organisation SAML, so unauthenticated `curl` to the public API was used): latest stable is `v7.6.9` (published 2026-10-25), which satisfies 7.4 or later. Prereleases (`v7.7.0-rc.1`) were not used.
* Asset `powershell-7.6.9-linux-x64.tar.gz`, SHA-256 `1da6d6d6035d651f20e70ddee7c4c15ac6ab8b9fb40ee92240d91263f28a884b`. The published `hashes.sha256` (itself `638e9546...8b45`, equal to the GitHub asset digest) lists the same value (decoded from UTF-16) and the API asset digest matches. Local `sha256sum` of the download matches all three.
* Installed only to the user-owned `~/.local/ama-tools/powershell/7.6.9/` (no sudo, no system package, no global configuration, no PATH edit). Telemetry opt-out variables are set per command. `pwsh` reports version 7.6.9.

## Gaps and limits

* Linux checks do not establish native PowerPoint, keyboard or assistive-technology viewing, or human rehearsal acceptance.
* Original FAIL, stopped-attempt and interrupted-gate records and the first recovery report stay unchanged.
