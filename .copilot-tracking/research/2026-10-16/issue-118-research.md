---
title: Issue 118 deployment hardening research
description: Existing evidence and bounded implementation readiness
ms.date: 2026-10-16
---

Task ID: 118. Slug: issue-118. Disposition: reused repository and supplied evidence,
with direct schema verification. Planning Readiness: Ready.

## PR 347 continuation evidence

Owner's review-fix direction supersedes the historical guard and scan-gate
boundary below. Read PR 347 body/diff before edits and kept its branch/identity.
Merged origin/main (8ac9367), preserving both append-only log sides and pushing.
Resolved latest python:3.12-slim-bookworm via Docker Hub: same index digest
34386ef0cb081344d7ec1c103ba398e6e9f64e9ab3a1509accc92a4e24a07258.
All four --pull --no-cache rebuilds reran apt upgrade: zero packages upgraded.
Fresh Trivy 0.76.0 comparison with one DB: each pre/post image has 61 HIGH and
two CRITICAL package findings, all unfixed (16 unique CVEs), zero reduction.
Fixable-only gates return zero findings/exit 0. Full reports retain the risk.
PR run 38932286066 also exposed API/orchestrator test PYTHONPATH values rooted
at /src: github.workspace was unavailable during matrix construction. Resolve
workspace-dependent absolute paths in the step environment instead.
Local Docker works using sudo; no Azure/private dataset needed.

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
