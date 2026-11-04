---
title: Research for #138 run summary slice
ms.date: 2026-11-04
---

Task: issue-138-run-summary. Disposition: executed. Planning Readiness: Ready.

## Delivered by merged PRs (evidence)

* PR 357: `.github/workflows/infra-plan.yml` (PR what-if, per-environment OIDC client IDs, `-plan` environments), `src-deploy.yml` (build, scan, SBOM, publish digest, approval-gated deploy, `pipeline.py deploy`), `infra/scripts/pipeline.py` (smoke: health 200, anonymous, malformed bearer and forged principal 401, sign-in 302, SQL private check).
* PR 500 and 672: pilot locks, source-validated image releases, scripted rebuild.
* `infra/tests/test_pipeline.py` covers these offline (29 tests before this slice).

## Gaps

* All six criteria need live Azure, GitHub environment reviewers and federated credentials: not locally provable.
* Criterion 2 says the what-if result is "attached": today only a 7-day artifact. Locally testable: write sanitized counts to `GITHUB_STEP_SUMMARY`.
* Dependencies #137 and #118 are open; not blocking offline work.

## Selected slice

Sanitized job summary for what-if and deployment. Touches deployment pipeline code: focused tier only, the coordinator owns any gate.
