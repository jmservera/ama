---
title: Deployment pipeline phase details
description: Bounded implementation details for issue 138
ms.date: 2026-10-16
---

## P01-T01

Add PR infra what-if and manual main-only release. Forks cannot use OIDC or
private runners. Protected environments must review exact candidate code.
Use separate plan/publish/deploy OIDC client variables and ephemeral runners.
Parameter compilation reads existing examples and replaces placeholders from
environment variables; only explicitly allowed overrides. Do not print ARM
parameters, resource IDs, Azure stderr or raw what-if values. Reject Delete.
Build all four workload images fresh from one main commit; no registry cache
reuse or partial release. Per-project path filtering applies to PR image checks.
Always run hardening and the same fixable/full Trivy policy before versioned push.
Deploy immutable digests, then exact HTTP checks without redirect following.
Authentication mode is an explicit typed environment choice, not a silent switch
away from browser UX.
SQL check uses scoped list and fails on any non-Disabled server.

## P02-T01

Document variables, GitHub environment reviewer/no-self-review/branch rules,
federated subject/audience patterns, ama-only roles, runner/network prerequisites,
manual initialization, quarantine release prerequisite and honest live gaps.

## P03-T01

Run fake-Azure and local HTTP tests, structure/mutation checks, ruff, mypy,
actionlint and relevant existing infra suite. Do not invoke deployment workflow
or Azure commands. Review once, route residual live work without claiming proof.
