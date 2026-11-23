# Changes: issue 2313 (Refs #2313)

Status: implemented, reviewed once.

## Files

* `.github/workflows/infra-image-build.yml` (new): PR image build, versioned tag `sha-<sha>-r<run>-a<attempt>`, `contents: read`, no login, push or deploy.
* `infra/tests/test_infra_image_build.py` (new): contract test.
* `docs/reference/research/issue-2313-what-if-live-2026-11-23.md` (new): evidence note.
* `infra-plan.yml` unchanged; it already satisfies the what-if criteria.

## Per-criterion table

| Criterion | Status |
| --- | --- |
| What-if only on infra PRs and uploads result | Proven by inspection and existing tests; unproven live (`INFRA_PLAN_ENABLED` unset, OIDC owner action) |
| Pinned SHAs and least permissions recorded | Proven (tests) |
| Versioned image tagged without deploying | Proven locally (importer build and startup check); unproven on GitHub (no push) |
| OIDC and approvals stay owner actions | Proven (no change) |

## Validation

New test 3 OK; actionlint and ruff clean; infra discover 748 run, 3 environmental errors (stale installed `zava_forward` lacks `AI_SUSPENDED`), unrelated. Complete gate not run (coordinator).
