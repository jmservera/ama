---
title: Employee progress dashboard 533 correction research
description: Bounded successor to the rejected scale-fixture review
ms.date: 2026-10-31
---

## Brief and Prior-Knowledge Gate

Task 533 / employee-progress-dashboard-533-correction, parent task 533 /
employee-progress-dashboard-533. Explicit owner selection authorizes a new
automatic correction loop and publication on the existing named branch.
Focused internal research; no Azure, private dataset, model, dependency changes
or runtime redesign. Existing research and original Review are reused, not
regraded. RPI research and repository guidance selected; specialist research
delegation skipped because this is one bounded fixture-contract trace.

## Cycle 1

### Wider

C1: Original Review RV-001 identifies the only implement-routed defect:
raw cases bypass store funding initialization. RV-002 requires fresh candidate
unit/browser/publication evidence. RV-003 is separate live/human/hosted work.
Source: .copilot-tracking/reviews/logs/2026-10-31/employee-progress-dashboard-533-review.md,
Findings and Defects and Routed Findings.

W1: Issue 533 and its 2026-10-29 owner comment retrieved on 2026-10-31:
https://github.com/jmservera/ama/issues/533 . Browser/unit checks remain open;
the owner explicitly retains deployed dashboard/archive acceptance.
Local checks do not establish that acceptance, so use Refs #533.

### Deeper

C2: src/api/tests/test_progress_dashboard.py:102-123 copies raw templates;
:1043-1050 replaces initialized reader cases. Its existing lifecycle_case
helper at :149-160 instead clones self.store.cases. Reuse that initialized
template pattern for scale construction, retaining the original browser
fixture defaults and lifecycle/AI semantics.

C3: src/api/checks/progress_browser_check.py:314-428 already supplies actual
small and scale local Chromium/axe validation with owned synthetic loopback
servers. Its browser fixture is initialized normally, unlike the unit overlay.

### Contrarian

Adding funding directly would encode a partial store contract and miss future
defaults. Reloading 60,000 cases into SQLite would change this reader regression
into a persistence test and increase cost. Clone the existing initialized four
templates for the unit overlay; leave production loading and persistence tests
unchanged. No other implement-routed defect appears in the original Review.

## Disposition and Readiness

Research executed; Planning Readiness: Ready. Findings C1-C3 establish the
bounded correction. User direction now explicitly permits later nonblocking
lock-admission retries within this session; the prior no-retry restriction
does not govern this successor. Only heavy checks take the shared lock.
Full publication still requires a committed clean candidate, complete external
receipt, current-main verification and independent exact-head assessment.
Missing prerequisite or failed validation blocks publication, not a skip.
