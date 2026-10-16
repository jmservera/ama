---
title: Deployment pipeline research
description: Focused offline research for issue 138
ms.date: 2026-10-16
---

## Brief

Implement issue 138 end-to-end without executing Azure operations. Audience:
repository maintainers. Scope: src images, infra helpers and workflows; retired
layouts excluded. User explicitly requests implementation, validation and PR.
Research posture: focused, inline; no independent research lane is needed.
RPI skills selected for lifecycle evidence; legal research is not applicable.

## Cycle 1

### Wider

* C1: `.github/workflows/src-ci.yml:1` owns source CI, hardened startup and
  Trivy gate. Existing legacy workflow names must remain unchanged.
* C2: `infra/README.md:230` describes dev/test/pilot examples and ama-only scope.
* C3: issue 138 and its comments require four workload images with project tags
  and path-aware builds, not the retired layout.

### Deeper

* C4: `infra/README.md:55` requires bootstrap, SQL/auth initialization and
  private runners before application deployment.
* C5: `infra/README.md:63` documents the image-preserving deploy wrapper.
* C6: `infra/README.md:194` requires exact health 200, protected API 401,
  malformed bearer 401 and forged-header 401.

### Contrarian

GitHub YAML cannot enforce reviewer configuration by itself. Private ACR and
ingress cannot be reached from ordinary hosted runners. Untrusted PR code
must never receive OIDC on a privileged runner. What-if output can contain
identifiers, so raw output must not be published. A workflow is not evidence
of federation, approval, release or deployment success.

## Decisions and readiness

Use separate offline validation, trusted same-repository PR what-if, and
manually dispatched environment-gated release. Require protected GitHub
environments and dedicated ephemeral private runners. Fail closed on missing
configuration, restrict all management queries to ama, deploy immutable image
digests and retain only sanitized plan summaries.

Research disposition: executed. Planning Readiness: Ready for offline
implementation. Live setup and deployment acceptance remain unmet.
