---
title: Capacity and work orders issue 523 plan critique
description: Single final-candidate assessment of the bounded acceptance extension
ms.date: 2026-10-30
---

## Metadata

* Task ID: 523 / capacity-work-orders-page-523
* Critique date: 2026-10-30
* Plan: .copilot-tracking/plans/2026-10-30/capacity-work-orders-page-523-plan.md
* Phase details: .copilot-tracking/details/2026-10-30/capacity-work-orders-page-523-phase-details.md
* Critique execution status: Complete
* Candidate baseline: 5634f9a077d175a931c15e3400114665d8c071ee

## Inputs and Criterion Boundary

* Supplied research: .copilot-tracking/research/2026-10-30/capacity-work-orders-page-523-research.md.
* Caller scope: optional pinned axe scans of seeded, both initial failed-read
  states and empty capacity; native keyboard retry; at most four helper test
  methods in one new API test file; the related README. No duplicate #528 repair.
* Required execution after planning: ordered RPI evidence, owned local SQL demo,
  every actual manager navigation entry, full API discovery/Ruff/format/mypy,
  local Playwright/axe and serialized heavy admission with flock -w 600.
* Boundaries: no Azure/deploy/live sign-in, credential files, private data,
  secrets or push; local commit uses Refs #523 only. Synthetic loopback login
  is part of the authorized local demo, not live sign-in.
* Inspected exact source: src/api/checks/capacity_browser_check.py,
  src/api/checks/regulatory_ux_check.py,
  src/api/tests/test_regulatory_ux_check.py,
  src/api/tests/test_procurement_api.py,
  src/core/src/zava_forward/core/appointments.py,
  src/core/src/zava_forward/core/mssqlstore.py,
  src/api/src/zava_forward/api/server.py, component manifests, component guides
  and relevant tools/rpi-checks.py lock/environment definitions.
* This assesses implementation credibility, not fresh runtime success,
  accessibility conformance, live acceptance or publication readiness.

## Coverage Assessment

| Requirement, research, phase, or task ID | Coverage | Evidence or concern |
| --- | --- | --- |
| AC1, AC4; research C2-C3 | Covered | Existing null-preserving binding and legacy read/write-denial regression support reuse, not another runtime fix. |
| P01-T01; seeded/error/empty axe | Covered | Explicit digest reuse, pre-store byte validation, #app scope, existing tags and violation failure; clean and omitted scans remain distinct. |
| P01-T01; AC3 keyboard recovery | Covered | Native focus plus Enter and focused-state/successful-read assertions extend the two existing initial-503 paths. |
| P01-T01; test budget and documentation | Covered | One new file, at most four methods, constructed helper tests and bounded README update; no removals or duplicated HTTP regression. |
| P02-T01; required package checks | Covered | Owned pip environment and explicit discovery/Ruff/format/mypy; API dependencies include core SQL support and API dev includes Playwright. |
| P02-T02; AC2, AC5 | Partial | Owned SQL and actual manager navigation are already supported; bypassing main also bypasses its environment isolation. PC-001. |
| P02-T02; heavy admission | Covered | Outer timed lock with direct helper calls avoids reacquiring the CLI's nonblocking lock. |
| P02-T03; ordered RPI and original evidence | Covered | One independent Review after reconciled validation, retained outcome, local commit, then complete gate attempt with failures as publication blockers. |
| AC6; prohibited operations | Covered | Live verification remains owner-pending; no deployment, push or live-success claim is authorized. |

## Verdict

* Verdict: Revise
* Rationale: The test-only extension is proportionate and otherwise credible.
  One direct correction must preserve the CLI's environment boundary when its
  main function is intentionally bypassed for timed lock admission.
* Severity summary: 0 Critical, 0 High, 1 Medium, 0 Low.

## Findings

<!-- rpi:critique id=PC-001 -->
### PC-001 [Medium]: Preserve environment isolation in the direct SQL runner

* Related IDs: P02-T02, AC2, local-only and owned-store requirements.
* Evidence: src/api/checks/capacity_browser_check.py:762-790 clears the process
  environment to a small allowlist before generating fixtures and calling
  owned_store/check. P02-T02 instead specifies direct calls from an external
  session runner to avoid nested lock acquisition, without preserving that
  environment step. owned_store passes the current environment to Docker and
  overrides only selected SQL keys. src/core/src/zava_forward/core/mssqlstore.py:227
  also consumes ZF_SQL_TOKEN when constructing its connection.
* Concern: The proposed execution path omits an existing isolation control.
  Constructing an owned database does not by itself remove inherited SQL tokens,
  application configuration or provider settings. This is a credible execution
  hazard, not evidence that such values are present.
* Impact: Local acceptance could inherit unrelated configuration or sensitive
  environment values, violating the synthetic-only boundary or failing for
  reasons unrelated to this extension.
* Smallest useful change: Amend P02-T02 to mirror main's clear=True environment
  allowlist around fixture generation, owned_store and check. Preserve only
  explicitly needed non-secret tool/runtime paths; do not read credential
  files or inspect/log secret values. Keep pinned byte validation before store
  startup and retain the existing outer timed-lock approach.
* Action owner: Planning parent; implementation executor owns the later runner.
* Exact resolving evidence: Updated P02-T02 explicitly requires the clearing
  context before fixture/store/application construction. The retained execution
  command or runner source must show that context and its non-secret allowlist;
  subsequent local SQL/browser results must identify that sanitized invocation.
  No additional unit-test file or test method is required.
* Decision route: Direct planner correction. Existing user direction already
  requires isolation; no significant or divergent user decision is needed.

## Strengths and Residual Risk

* The existing check verifies actual manager navigation, headings, browser reads
  and rendered data; reuse is substantially stronger than creating parallel
  route tests.
* Existing draft-retention, cancellation, transport, 403 and late-401 coverage
  is explicitly retained. This critique does not expand axe to those scenarios.
* Axe and keyboard engineering checks are not whole-screen accessibility,
  assistive-technology, production SQL or post-deployment acceptance.
* Missing prerequisites or failed complete-gate results remain publication
  blockers. No success, skip waiver, cloud fallback or protection change follows.
* Original adverse validation and Review evidence must remain unchanged.

## Questions or Blocking Evidence Gaps

* None requiring user input. PC-001 can be resolved directly in phase details.

## Limitations

* No heavy gates, installs, SQL/container startup, browser execution, external
  research or authenticated operations were performed for this critique.
* Prior research execution claims were not rerun. Source inspection confirms the
  relevant existing contracts, not current-candidate execution results.
* Existing untracked RPI inputs were left intact. Only this critique was added;
  no source, plan, details, research or earlier review evidence was changed.

## Recommended Next Action

* Highest-impact finding: PC-001.
* Action owner: Planning parent.
* Smallest next action: Add the sanitized-runner requirement to P02-T02 and
  record this critique's disposition; finalize without another critique.
* User response required: No.

## Next Steps

The active planning parent applies PC-001 directly, preserves this original
Revise outcome, then continues the authorized ordered RPI stages. No user
action, additional critique or expanded implementation scope is required.
