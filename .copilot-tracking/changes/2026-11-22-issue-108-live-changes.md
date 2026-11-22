# Changes: issue 108 live 2026-11-22

Refs #108. Tier: focused; no `src/` change (FULL tier not triggered). Divergence from the goal: no code was implemented because the demo assistants already have offline AI quality checks and no demo-relevant buildable gap remains.

## Files

* docs/reference/research/issue-108-live-20261122-2026-11-22.md (new note)
* docs/reference/research/issue-108-live-20261122-2026-11-22/ (azure_outputs.txt, app_config.txt, unittest.txt)
* `.copilot-tracking/` research, plan, details, changes, review and state files

## Validation

171 offline tests pass (unittest.txt). Azure calls were read-only; no secret read or printed.

## Per-criterion proven/unproven

| Criterion | Status | Evidence or reason |
| --- | --- | --- |
| Model names, versions and quotas in the chosen region | Partly proven | azure_outputs.txt: uksouth deployments confirmed; TPM headroom not returned; `aoai-resident-469` gone |
| Frozen independent held-out split | Unproven | Needs independent labeller |
| Human detection of seeded critical errors | Unproven | Needs authorised participants |
| Effort and cost against alternatives | Unproven | Needs people and Finance |
| Hashes, serving version, reviewer protocol | Unproven | Needs real held-out batch; resident serving deployment not attested |
| Actual-call authorization and consent | Unproven | Production authority |
| Real AI/SQL/Azure proof (CON-009/AC-057) | Unproven | Production build |
