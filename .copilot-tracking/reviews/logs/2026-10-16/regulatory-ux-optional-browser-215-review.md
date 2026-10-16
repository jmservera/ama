---
title: Regulatory UX optional browser dependency review
description: One post-implementation review of the bounded CI repair
ms.date: 2026-10-16
---

Refs #215. Review execution: Complete.
Outcome: Conformant for the bounded import repair; not full issue acceptance.

## Assessed boundary and inputs

Compared research, plan, phase details, single critique and changes using the
shared `regulatory-ux-optional-browser-215` task slug dated 2026-10-16.
Reviewed the complete repair diff, related README/index/log changes, and chat
merge-conflict integration. Direct review was sufficient; no review worker ran.
Publication remains the explicit pending P03 action, not a claimed result.

## Implementation assessment

The postponed Page annotation imports only under TYPE_CHECKING. No runtime
dependency or mypy suppression is added. Each browser helper imports its own
expect, and run imports both expect and sync_playwright after hash validation,
before fixture startup. Thus pure size/hash assertions do not load a browser;
a requested browser run still fails explicitly if the dependency is missing.
PC-001 is directly resolved. Existing pure tests remain enabled.

The fresh subprocess rejects Playwright through a meta-path finder and imports
the check using current test paths. It runs both with and without the installed
library. This does not replace the real browser execution.

Source CI is unchanged: its dev installation supplies Playwright, its dedicated
browser step installs Chromium and invokes both harnesses, and its existing
evidence upload remains. No skip or success-shaped fallback was added.

Merge resolution retains the privacy warning/retention metadata and textarea
association while keeping proper list/live-log semantics and visible disabled
chat guidance. Actual browser interactions and axe run pass after integration.
Both log histories are preserved line-for-line in order.

## Validation evidence

| Check | Result |
| --- | --- |
| Baseline runtime-only full API suite | Reproduced eager Playwright import error: 558 tests, 110 skips, one error |
| Fixed full API suite, Playwright absent | 561 tests, 110 opt-in skips, pass |
| Fixed full API suite, Playwright 1.64.0 installed | 561 tests, 110 opt-in skips, pass |
| Harness pure/import-blocking tests | Four pass in both environments |
| Merged core regulatory contracts | 56 tests pass |
| API Ruff/format plus isolated check lint/format | Pass |
| API strict mypy | Pass, 47 source files |
| Actual design-system synthetic loopback browser check | Pass, including responsive app and shared workbench checks |
| Actual regulatory synthetic loopback browser check | Pass, pinned axe executed, 17 states, 142 targets, zero detected violations |
| Git whitespace and both append-only histories | Pass |
| Hosted latest-head CI | Not yet run at review; publication action remains |

## Complete finding set

No substantive implementation defects found in the bounded repair.
No unresolved significant/divergent decisions or unrecorded amendments.
No RV defect entries are fabricated for already disclosed acceptance gaps.

## Issue criterion audit

| Issue criterion | Disposition |
| --- | --- |
| Role-shaped patterns and know-at-least content | Met only as synthetic design/existing-role guidance, not validated staff needs |
| Noticed, source/status, safe action, owner and clock | Met only for existing scoped contracts; no broader rule coverage |
| Full WCAG 2.2 AA including text/keyboard/plain language | Partial/unmet; eight axe contrast-incomplete states and manual/assistive-technology assessment remain |
| Doubt and no-source states | Met in bounded synthetic slice, not actual notification or approval |
| Repairs/housing/grants staff comprehension before use | Unmet/Not run; protocol only |

## Routing and remaining work

Owner-authorized publication: commit with required identity/trailer, normal push
to existing branch, update existing PR #354 and verify remote head. Do not create
a duplicate PR or change issue checkboxes.

Distinct existing follow-ups, not defects introduced by this repair:
full accessibility assessment, authorized real staff comprehension, measured
paired chat value, real accountable owners and applicable source verification.
No additional research is needed to fill a list or complete this repair.
Human legal interpretation/rule activation, resident consent, safety and
financial commitments remain under named human approval. Juan Manuel Servera
is the synthetic exercise Legal, Compliance and DPO owner only.
