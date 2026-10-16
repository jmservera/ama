---
title: Deployment pipeline changes
description: Implementation evidence for issue 138
ms.date: 2026-10-16
---

## Scope

Full plan P01-T01 through P03-T01, explicitly requested by user. One critique
completed and dispositions recorded. No Azure execution is permitted.

## P01-T01

Implementation complete. Trusted workflow_run planning and main-only manual
release replace the initial directly privileged PR job. Hosted image testing is
separated from private OIDC publication. Full fresh releases replace cache reuse.

## P02-T01

Updated infra/source READMEs, reference routing and appended the knowledge log.
Documented exact variables, subjects, reviewer and runner configuration, scoped
RBAC, quarantine admission and all six live-unverified acceptance criteria.

## Amendments and divergences

Compatible critique changes applied before implementation. Authentication mode
is explicitly selected as a typed environment variable, preserving browser mode
rather than silently forcing service-test mode. Fresh full releases supersede
the original cache-reuse proposal. No source application or template security
behavior changed. No Azure operation or workflow dispatch was performed.

## Validation (P03-T01)

154 infra tests pass with REQUIRE_AZ_BICEP=1 and absolute core/agents test paths.
Includes 24 new pipeline tests, real installed local API startup on an empty
constructed fixture, strict HTTP negative probes, workflow mutation checks,
fake-command orchestration and canary error-output checks. Ruff/format and
strict mypy pass for new helper; actionlint 1.7.12 passes all three changed
workflows with declared runner labels (optional shellcheck/pyflakes disabled).
Git diff whitespace check passes. Existing 130 infra tests pass unchanged.
All three actual Bicep parameter examples also compiled through the new helper
offline with constructed override fixtures; profile and privacy assertions pass.
Final implementation validation fixed plan/apply CLI cross-wiring and made
path-filter subprocess failures propagate before emitting outputs.
Local Docker daemon is unavailable; images/Trivy were not rerun locally.
Release workflow retains those gates, and live criteria remain unmet.

Implementation ready for the single post-implementation Review. Publication
remains P03-T01 work after Review; no unresolved local test failures.

## Review and publication (P03-T01)

One Review executed, Complete, outcome Residual work. No local source defect
identified; external configuration/live acceptance and remote CI evidence are
routed separately in RV-001 through RV-003. No second Review or Azure run.

Reviewed code committed as 22f04b1 with the verified authenticated account's
repository-local noreply email and required Copilot trailer. Topic branch
pushed without history rewrite; PR https://github.com/jmservera/ama/pull/357
opened against main with Refs #138 only. All six acceptance criteria remain
unchecked, and every live gap is explicit in the PR body. Final tracking-only
closeout does not alter the reviewed source. Remote CI is not presumed passed.
