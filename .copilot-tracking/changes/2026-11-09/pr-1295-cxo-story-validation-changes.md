<!-- markdownlint-disable-file -->
# PR 1295 CxO story PowerShell validation changes (2026-11-09)

Plan: [plan](../../plans/2026-11-09/pr-1295-cxo-story-validation-plan.md). Executed after the research and plan records, on frozen head `399e31ac14316e05e6be73b49cfcde9de6538ee2` (tree `cdfb1f3c...`), `origin/main` `b46a9ad9a9619db535368d1b2cbbddec8110e122`.

## Source changes

None. No deck, slide content, financial, slide-count, navigation or protected-cost change. Tracked tree unchanged by every check (`git diff --quiet` passes; only these tracking records are new).

## Tool provenance

* PowerShell 7.6.9 (stable, published 2026-10-25) from `PowerShell/PowerShell` release `v7.6.9`, asset `powershell-7.6.9-linux-x64.tar.gz`, SHA-256 `1da6d6d6035d651f20e70ddee7c4c15ac6ab8b9fb40ee92240d91263f28a884b`, matching the published `hashes.sha256` entry and the GitHub asset digest. Installed only under `~/.local/ama-tools/powershell/7.6.9/` (explicit path; no PATH, sudo, system or global change). Scripts require 7.4 or later.
* Scratch outputs were written to `/tmp/ama-capstone-val-*` outside the repository (not committed).

## Executed commands (repository root, `pwsh` = explicit path)

| Command | Exit | Result |
| --- | --- | --- |
| `Invoke-Capstone.ps1 -Action Build -RepoRoot $PWD -OutputDir $Run/build` | 0 | 54 slides and notes; assets, navigation, timing, protected cost verified |
| `Invoke-Capstone.ps1 -Action Verify -RepoRoot $PWD -OutputDir $Run/verify` (copy of the build) | 0 | status pass, 54 slides, 54 non-empty notes, 108 navigation actions, manifest and media verified |
| `Test-CostStatus.ps1 -RepoRoot $PWD -CandidatePath <built pptx>` | 0 | protected-cost tests passed, all six pages, denied unapproved status, number, geometry and note mutations |
| `Test-SourceHashes.ps1 -RepoRoot $PWD -SemanticOnly` | 0 | canonical source semantics passed |
| `Test-SourceHashes.ps1 -RepoRoot $PWD` | 0 | four canonical source bindings, convention and exact delivery hash passed |
| `Test-NativeShapes.ps1 -RepoRoot $PWD` | 0 | 32 native-shape checks passed |

## Notes and failures

* A first Verify attempt with an empty output directory exited 1 (`Could not find file .../verify/zava-forward-cowork-v2-draft.pptx`): Verify checks an existing candidate in its output directory and does not build one. It was a wrong invocation, not a source failure; the correct run (above) used a copy of the built candidate. No check was waived.
* The rebuilt candidate SHA-256 `47098c84516c044e3baa4ce74cb8dbb67588f988e24c01a62196746807122129` equals the delivered `docs/capstone/deck/zava-forward-cowork-v2-draft.pptx`.

## Not established

Native PowerPoint viewing, keyboard and assistive-technology acceptance, PDF/projector review and human rehearsal were not run and are not inferred. Hosted checks and independent exact-head review remain mandatory. No `rpi-checks --all`.
