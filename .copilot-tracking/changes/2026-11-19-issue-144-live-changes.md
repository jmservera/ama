# Changes: issue 144 deployed image audit (2026-11-19)

Status: implementation starting. Tier: FOCUSED (new read-only script, no src/ change, no Bicep, workflow, permission or deploy change). Witness note: first `plan-done` was refused (state lacked artifact paths); corrected and accepted at seq 4. The refusal stays in the witness log.

## Files

* infra/scripts/deployed_images.py (new, read-only offline audit)
* infra/tests/test_deployed_images.py (new, 3 tests)
* docs/reference/research/issue-144-live-deployed-images-2026-11-19.md, docs/reference/README.md, docs/reference/log.md

## Validation

* `python3 -m unittest infra/tests/test_deployed_images.py`: 3 tests OK.
* `ruff check` and `ruff format --isolated --line-length 100 --check` on both Python files: clean (an initial EXE001 and SIM115 finding was fixed).
* Live run on `az containerapp|job list -g ama` output: 12 containers, all digest-pinned, exit 0.
* mypy not applicable (no src/<project> change); rpi-checks --all not run (heavy lock, FOCUSED tier).

## Per-criterion table

| Criterion | Status |
| --- | --- |
| Worker and job images real, versioned, deployed through the pipeline | Partly: real and immutable proven live; tags and pipeline deployment UNPROVEN (private ACR, no src-deploy runs) |
| Container hardening enforced in deployed app | UNPROVEN, adverse: deployed specs lack hardening env and scratch volumes |
| Scale rules, probes, limits, rollback | ticked already; not re-proven |
| Load test on declared fixture | ticked already; not re-proven |
| Single-replica and restart with audit persistence | ticked already; not re-proven |
| Tokenomics usage and cost drivers | ticked already; not re-proven |

## Rerun 2026-11-19 (live-20261119T141822Z)

No source edits. The audit script was re-run against a fresh live listing: 13 of 13 containers digest-pinned, exit 0; deployed securityContext null. Both unticked criteria stay unproven: the pipeline clause needs self-hosted runners with OIDC (src-deploy.yml never run), and Container Apps ARM has no read-only root or capability-drop field, so enforcing hardening means a production redeploy. Nothing buildable for the demo remains. Validation: FOCUSED, no src change, Azure access read-only.
