---
title: Deployment pipeline review
description: Single post-implementation review for issue 138
ms.date: 2026-10-16
---

## Boundary

Task 138 / cicd-deploy-pipeline-138. Compare new infra-plan/src-deploy workflows,
modified src-ci, infra/scripts/pipeline.py, infra/tests/test_pipeline.py and
actionlint config, source/infra documentation and knowledge index/log.
No Azure execution or live configuration inspection is in scope.

## Inputs

* .copilot-tracking/research/2026-10-16/cicd-deploy-pipeline-138-research.md
* .copilot-tracking/plans/2026-10-16/cicd-deploy-pipeline-138-plan.md
* .copilot-tracking/details/2026-10-16/cicd-deploy-pipeline-138-phase-details.md
* .copilot-tracking/plans/2026-10-16/cicd-deploy-pipeline-138-critique.md
* .copilot-tracking/changes/2026-10-16/cicd-deploy-pipeline-138-changes.md

## Execution and outcome

Execution: Complete. Outcome: Residual work.
Implementation tasks P01-T01 and P02-T01 are complete. P03-T01 validation is
complete; publication awaits this review. No human or live acceptance marker
has been checked.

## Assessed implementation

P01-T01 and P02-T01 match the revised plan. The one critique's sixteen findings
have explicit dispositions. Fresh full releases and an explicit typed
authentication-mode choice are justified changes that preserve the user's
source-only, no-secret and browser-UX boundaries. No local source defect was
identified in the reviewed offline boundary.

The trust chain is default-branch workflow_run -> same-repository successful
source CI -> candidate infra data -> protected environment -> trusted helper.
Hosted builds have no id-token permission. Only private plan/publish/deploy jobs
have job-local id-token write, with separate client variables. All actions in
the three affected workflows are pinned and checkout credentials do not persist.
Release metadata binds registry/repository/digest, source SHA, run and attempt.
All four projects must publish before target approval and apply; partial builds
cannot feed deployment. Runtime failures do not skip scans after a good build.

The helper preserves selected environment profile values, overlays only typed
configuration and forces private access. Plan cannot select apply via metadata.
Only group-scoped incremental operations in ama occur; unsupported/deleting/
out-of-group plans stop apply. SQL discovery is non-vacuous before/after apply.
The exact parameter file is shared by what-if and apply and then removed.
Raw subprocess errors and ARM values are withheld, while failures remain
explicit. Post-deploy failure cannot produce a successful deployment summary.
No real identifiers, stored credentials, private dataset or retired-path edits
were introduced.

## Validation

154 infra tests passed, including all prior 130 tests and 24 new pipeline tests.
New tests cover workflow mutations, permissions/pins/echo, transitive paths,
typed parameters, reviewer settings, plan scope/deletion/SQL controls,
image metadata and quarantine pull denial, immutable publication, fake
what-if/apply ordering and temporary-file removal, PR image preservation,
CLI apply refusal, canary log suppression and local HTTP negatives.
The installed source API also ran on an empty constructed fixture and passed
the same health/anonymous/malformed/forged-header probes.

Ruff/format and strict helper mypy passed. Actionlint 1.7.12 passed all three
changed workflows using declared private runner labels; shellcheck and pyflakes
were disabled, not claimed executed. All three real Bicep parameter examples
compiled through the helper offline with synthetic overrides and expected
profile/private assertions. Git diff whitespace/excluded-path checks passed.
No local Docker daemon, image/Trivy rerun, Azure API operation or workflow
dispatch is claimed.

## Findings and routing

### RV-001 [High]: Platform configuration and approval are unverified

Destination: distinct platform-owner setup/acceptance follow-up.
Every target needs verified exact-subject OIDC federation, ama-only RBAC,
protected main/environments with independent reviewers and no bypass,
ephemeral private runner/network isolation, completed region/quota references,
tenant/runtime prerequisites and an approved quarantine release path. These
are necessary live acceptance gaps, not inferred from YAML or offline tests.

### RV-002 [Medium]: Live release and runtime evidence is unavailable

Destination: distinct owner-authorized deployment acceptance follow-up after
RV-001. Exercise PR what-if artifact, approvals, four scan/push/digest records,
private health 200 and API denial checks, SQL-private state and log audit.
Separate SQL read/write, authorized staff, model access and restart persistence
remain unmet; the pipeline does not claim to prove them. Hosted kernel
hardening remains Partial under the inherited Container Apps limitation.

### RV-003 [Low]: Fresh image and remote CI evidence remains pending

Destination: publication/CI evidence handoff under P03-T01. The local Docker
daemon is unavailable. New release definitions are structurally validated but
not run; existing source CI will build changed images and scan with the reused
policy. Do not label queued/running/skipped jobs as passes.

## Criterion audit

| Criterion | Assessment |
| --- | --- |
| Environment-scoped OIDC authentication | Offline wiring/tests only; live unmet |
| Infra PR what-if and attached result | Trusted trigger/sanitized artifact implemented; live unmet |
| Approval and environment parameter sets | Implemented configuration guard and same template/examples; actual approval/pilot setup unmet |
| Versioned push and deployment image reference | Implemented same-run digest handoff; live unmet |
| Automatic post-deploy health/authentication checks | Local application and negative HTTP tests pass; live checks and remaining README identity/model/restart evidence unmet |
| No secret values in logs/repository | Static/canary evidence only; end-to-end live log audit unmet |

## Handoff

Publish the reviewed source as explicitly requested, preserve all six issue
checkboxes unchecked and state live gaps in the PR body. No second Review is
requested. Route RV-001/RV-002 to later owner-authorized work, not an Azure run
in this task. Publication does not authorize merge or operational reliance.
