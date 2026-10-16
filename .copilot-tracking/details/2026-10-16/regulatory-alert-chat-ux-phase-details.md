---
title: Issue 215 phase details
description: Implementation and evidence boundaries
ms.date: 2026-10-16
---

## P01-T01

Use current me.user.role, never a user-selectable authority. A shared role help
panel includes data handling for everyone and role-specific recognition content.
Source status is read from server, never inferred by UI. Read alerts for exact
case ID and show empty as no visible alerts, not no risk. Failure stays unknown.
Do not add acknowledgement/approval controls; existing named-owner routes remain.

## P01-T02

Use answer.sections and citations from #348, not generated or client-interpreted
legal text. Default short explanations plus expandable exact source details.
Plain mode changes presentation, never stored evidence. Preserve disabled
regulatory chat visibility with explanatory text instead of silent disappearance.
Show source gaps and name the exercise owner; send only through existing doubt
API with explicit receipt/error. Preserve ordinary chat behaviour.

## P02-T01

New browser check runs against the actual loopback SQL-backed API using core
regulatory_fixture, blocks outbound inference, and uses Chromium. Assert field
shape, plain mode, safety path outside collapsed chat, no-source/refusal,
persisted doubt and permission denial. Cover all seven existing staff role help
mappings; supplier is design-only and must not gain chat/law access.
Run axe for WCAG 2.2 A/AA, keyboard Tab/Shift-Tab/Enter/Space, focus and 320px
reflow against changed surfaces. Record automated scope, not full conformance.

## P02-T02 and P02-T03

Use absolute per-project source/test PYTHONPATH, existing relevant unit suites,
ruff and mypy. README owns seven-audience design and staff test protocol with
predeclared tasks, scoring, consent and stop rules, no invented results.
Append KB log; keep index pointing to durable API guide. Review once after
implementation; remaining findings route to later work with severity and owner.
Blocking findings require a draft PR and partial outcome, not a pass claim.
Do not repeat review or re-enter implementation within this task.
PR criterion audit
explicitly distinguishes proved engineering slices and unmet human criteria.

## Critique reconciliation

The README matrix covers the actual seven issue audiences, separately from the
seven staff account roles. Suppliers remain design-only with current denial.
Leasehold and resident/representative guidance is supplementary design-only;
data handling is cross-cutting. Do not substitute the critique's seven research
rows for the issue's seven acceptance audiences. Test staff mappings and denial
separately from documenting proposed patterns for unmapped audiences.

## Final execution state

P01 and P02 completed; feature commit 82bd6c2 pushed to the existing topic.
PR #354 targets main with Refs #215, a five-criterion audit and all unmet gates.
One Review completed with Residual work. No operational/full-WCAG/staff result
is claimed; issue checkboxes and the owner's merge authority remain unchanged.

## P03 independent review implementation

Scope explicitly requested on 2026-10-16: address both findings from independent
CHANGES at d79a737 on existing PR #354. Merge main first; keep both log sides.
Add regulatory_ux_check next to design_system_browser_check in src-api CI.
Fetch axe 4.10.3 with bounded curl time/retries; validate its existing SHA-256
before execution. On download failure emit a CI warning, record axe skipped
and still execute all non-axe assertions; corrupt supplied content must fail.
Use absolute API/core/agents test paths with API tests first.

Measure all visible enabled interactive targets on the changed surfaces, plus
the outer chat disclosure, across exercised states and viewport sizes. Include
the cited-lookup summary and preserve its designed 44px height as a stronger
regression floor: its unstyled 24px line box already meets the AA minimum.
Do not infer target size from CSS text or from a few activated controls.
Remove the regulatory summary rule for a local mutation run and require
a target-size assertion failure; restore it immediately afterward.
Run both normal and no-axe browser paths, relevant unit tests, ruff/format/mypy.
Record that hosted CI is pending because the owner says push and do not wait.
Leave WCAG/staff/value/operational acceptance gaps unchanged.

P03 completed: d2b8df4 committed and pushed without force; existing PR #354
body updated. Both download modes and exact CSS-deletion mutation verified
locally; hosted CI intentionally not awaited. No issue checkbox changed.
