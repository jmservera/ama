---
title: Regulatory UX optional browser dependency research
description: Focused CI import-boundary investigation for the existing PR
ms.date: 2026-10-16
---

## Research brief and controls

Refs #215. Repair PR #354 on its existing branch after merging origin/main.
Keep unit discovery, pure target-size assertions and axe hash rejection runnable
without Playwright; retain actual browser coverage in source CI. No application
feature redesign, infrastructure action, private data access or human acceptance
claim. Output mode: convergence. Posture: focused, selected from the explicit
caller scope and supplied import failure. No interaction is needed.

Evidence root: `.copilot-tracking/research/2026-10-16/`.
Repository instructions, ADR 0006 and the RPI research protocol apply.
Specialists and external research are skipped: the uncertainty is one small,
coupled import boundary, with sufficient local evidence.

## Questions and prior knowledge

1. Which runtime import makes browser-free unit discovery fail?
2. How can pure assertions retain coverage without suppressing browser failures?
3. What type-checking and merge-integration constraints apply?

## Cycle 1

### Wider

C1: `src/api/tests/test_regulatory_ux_check.py:10` imports `run` and
`target_sizes` at discovery time. All three existing tests are non-browser tests.
C2: `src/api/checks/regulatory_ux_check.py:14` imports Playwright eagerly.
C3: `src/api/pyproject.toml:19` places Playwright in the dev extra, not runtime
dependencies. Adding it to runtime dependencies would conceal the boundary bug.

Reflection: skip decorators alone cannot protect an earlier module import and
would unnecessarily lose pure regression coverage.

### Deeper

C4: `src/api/checks/regulatory_ux_check.py:146` checks axe integrity before
fixture creation. Its Page annotations can remain typed under TYPE_CHECKING;
browser operations need Playwright only after that integrity check.
C5: `.github/workflows/src-ci.yml:73` retains a dedicated browser step installing
Chromium and running both design-system and regulatory checks. No CI/browser
skip is necessary.
C6: `src/api/checks/design_system_browser_check.py:26` uses the real typed
Playwright API; mypy checks `checks/` with the API dev extra installed.

Reflection: use a type-only Page import and local imports for runtime browser
operations. Missing Playwright must still fail explicitly when a browser check
is requested.

### Contrarian

Rejected: skip the whole test module, install Playwright in production, broad
ImportError catches, or silently return from the browser runner. These weaken
the exact boundary or required checks. A no-Playwright import regression should
block Playwright imports explicitly even in dev environments.

C7: `src/api/src/zava_forward/api/web/chat.js:169` conflicts with main's privacy
warning integration. Merge resolution keeps the privacy warning and described-by
association, the branch's list/live-log semantics, plain-language controls and
visible unavailable-chat fallback. Actual browser validation must exercise this.

## Synthesis and readiness

Research disposition: executed. Planning Readiness: Ready.
Selected: lazy browser-only runtime imports, typed Page under TYPE_CHECKING,
and an isolated import-blocking regression. Keep all pure tests and CI browser
execution enabled. One cycle suffices: all bounded questions have local evidence.
Baseline and final execution evidence belongs in changes/review artifacts.

Human staff comprehension, full WCAG conformance, operational legal approval,
real owners/sources and measured chat value remain unproved. Juan Manuel
Servera remains the exercise Legal, Compliance and DPO owner; synthetic
development acceptance authorizes none of those operational decisions.
