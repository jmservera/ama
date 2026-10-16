---
title: Issue 118 deployment hardening research
description: Existing evidence and bounded implementation readiness
ms.date: 2026-10-16
---

Task ID: 118. Slug: issue-118. Disposition: reused repository and supplied evidence,
with direct schema verification. Planning Readiness: Ready.

## Evidence

* Read issue 118 body and comments: container/CI evidence remains here; 143,
  144 and 147 carry detailed infrastructure follow-ups. User explicitly requests
  gated definitions and honest acceptance audit, not public deployment.
* Read original/addendum, reference index/memory, housing primer, instructions,
  ADR 0006, cutover evidence, four Dockerfiles, src-ci and existing infra tests.
* All images set UID 10001 but do not enforce runtime kernel settings.
  src-ci only prints versions; Trivy ignores unfixed vulnerabilities.
* Application API, agents, orchestrator, import and maintenance jobs already
  exist in Bicep. Job command overrides would bypass a new image entrypoint.
* Front Door Premium/WAF/Private Link already have production/default-off guards.
* Policy is DoNotEnforce and Defender is Free-by-default at subscription scope.
  Applying Free would overwrite an existing paid plan, so disabled opt-in must
  mean no pricing resource is submitted.
* Microsoft Learn containerApps 2025-07-01 and 2026-07-01 references checked
  2026-10-16: no securityContext/readOnlyRootFilesystem/capabilities fields.
  https://learn.microsoft.com/azure/templates/microsoft.app/2025-07-01/containerapps
* Local Docker needs sudo; sudo Docker works. Bicep 0.48.1 is available.
  No Azure execution is needed or authorized by this implementation.

## Boundary

Dockerfile cannot set host mount flags or capability bounding sets. Use a shared,
dependency-free fail-closed entrypoint and actual Docker positive/negative tests.
Document that explicit entrypoint/ACA command overrides bypass it and that
unsupported hosted kernel controls block rollout, not invent Bicep properties.
Keep worker behavior and human legal/consent/financial approval gaps explicit.
