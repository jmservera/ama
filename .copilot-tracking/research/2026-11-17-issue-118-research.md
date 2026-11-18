# Issue 118 research: hardened deployment, CI and IaC (2026-11-17)

Base: origin/main eb51af5c9ab0b1353ac380fc8960ee8dd96d17c4. Scope: evidence-only reassessment, no deployment, no Azure action.
Research disposition: executed. Planning Readiness: Ready once measurements below are recorded.

## Prior evidence
* Closure audit 2026-10-31 and batch004 (2026-11-05): criteria 1 to 4 ticked; criterion 5 unmet (owner decision).
* Log entry 2026-11-04 (Refs #118).

## Measurements on main eb51af5c9 (local, offline, sequential)
| Check | Result |
| --- | --- |
| `python3 -m unittest discover -s infra/tests -p test_container_contract.py` | 9 tests OK |
| `... -p test_bicep_policy.py` | 62 tests OK (asserts `enableDefenderPlans` default false, Policy `DoNotEnforce`) |
| `... -p test_governance.py` | 9 tests OK |
| `... -p test_edge_module.py` | 9 tests OK |
| `... -p test_pipeline.py` | OK |
| `... -p test_container_hosting_completeness.py` | 16 tests OK |
| `src/check-container.py` | Needs a built image (`project image`); not run (no Docker image build, brief forbids heavy services). Controls `--read-only`, `--cap-drop=ALL`, `no-new-privileges` present at lines 13-15, 21. |

## Criteria against main
1. Non-root/read-only/caps dropped: `src/api/Dockerfile:30 USER 10001:10001`; runtime controls enforced by `src/check-container.py`; invoked in `.github/workflows/src-ci.yml:140,149`. Delivered (image run not repeated here).
2. Scan and tests in CI: Trivy steps `src-ci.yml:152,165`, config `src/trivy.yaml`. Delivered; no hosted run observed in this pass.
3. Application in Bicep: `infra/main.bicep`, `infra/modules/containerapps.bicep`; offline tests pass. Delivered offline; no live state read.
4. Front Door Premium, WAF, Private Link: `infra/modules/edge.bicep`, `test_edge_module.py` passes. Delivered offline.
5. Policy and Defender decided: `infra/defender-decision.json` (recorded 2026-11-01) says Audit-only, Deny open, Defender deferred, `costApproval.status` pending, `approvedOn` null. UNMET: owner decision.

## Defect search
No failing test, no drift between decision record and Bicep defaults. No defect reproduced, so no source fix or regression test is justified.
Not proven: live Azure state, hosted CI of this head, image run, load tests (named in the issue body as outstanding; tracked in #136 children).
Planning Readiness: Ready. Follow-up: owner Defender/Deny decision (no code step).
