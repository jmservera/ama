---
title: Environment parameter sets research
description: Current evidence and decision boundaries for issue 137
ms.date: 2026-10-16
---

Task ID: issue-137. Task slug: environment-parameter-sets.
Research disposition: reused and extended by direct repository inspection.
Planning Readiness: Ready.

## Evidence

* Read issue 137 body/comments and issue 139 body/comments with gh.
* Read the original/addendum, reference index/memory, ADR 0006, repository
  instructions, infrastructure entry point, parameter sets, deployment wrapper,
  SQL/Foundry modules and compiled-policy/fake-az tests.
* Existing parameter files cover the three environments, but dev/test enable
  public networking and README/pilot assert settled pilot ownership/region.
* The 2026-10-15 issue comment selects a pilot region and subscription owner;
  the current task explicitly supersedes it. Keep both decisions open.
* Issue 139 already has compiled control, guard-matrix and mutation gates.
  Extend those gates rather than adding a parallel policy implementation.
* SQL currently follows the development public switch, including a full-range
  firewall. Current owner direction requires SQL private in every environment.
* main.bicep exposes location, sqlLocation and modelDeployments including
  SKU/capacity, but does not require a reference to recorded deployment checks.

## Boundaries

No Azure operation is necessary for this infrastructure/offline-test slice.
Resources may only be deployed inside ama; never create/delete a group or bypass
policy. Pilot region/subscription ownership, current quota, costs, private edge
acceptance and actual human approvals remain separate deployment prerequisites.
ADR 0005 acceptance is synthetic-development-only; no operational reliance or
new approval is inferred. No private datasets, configuration or IDs are needed.
