# Changes (Refs #201, evidence only, tier FOCUSED, no src change)

Files: docs/reference/research/cutover-gate-live-2026-11-18.md (new), docs/reference/README.md (index), docs/reference/log.md (entry), `.copilot-tracking/` artifacts.

| Criterion | Result | Evidence |
| --- | --- | --- |
| CI, Docker, Bicep paths and scripts repointed | Proven (repo checks) | 0 tracked mvp/prototype files; src-ci/src-deploy build from `src/`; `infra tests.test_pipeline` 32 OK |
| Build from `src/` deployed and healthy | Healthy proven; src provenance unproven | Revision 0000031 Healthy/Running, /healthz 200; ACR private, no src-deploy runs, no build label |
| Private `mvp/data/` relocated and backed up | Unproven, deferred | Owner-only attestation; no agent may read |
| Owner signs off | Unproven, deferred | Human decision |

Validation: `python3 -m unittest tools.test_check_legacy_references tools.test_private_mvp_data_exclusion tools.test_epic_legacy_path_retirement`: 18 run, 1 FAIL (pre-existing, 11 violations in three tools/test_*.py files, recorded as adverse, not fixed). Mypy/ruff: not applicable, no Python changed. rpi-checks --all not run. Azure: read-only; no resource created.
