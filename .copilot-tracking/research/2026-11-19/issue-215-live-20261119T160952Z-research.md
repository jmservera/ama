---
title: Issue 215 live research, 2026-11-19
description: Opening research for the unticked criteria of #215 against prior dated evidence
ms.date: 2026-11-19
---

## Scope

Issue #215 has two unticked criteria: (3) WCAG 2.2 AA with no colour-only status, keyboard operation and plain-language mode; (5) comprehension tested with repairs, housing and grants staff. Research disposition: reused. Planning Readiness: Ready.

## Evidence reviewed

* docs/reference/research/regulatory-ux-live-215-2026-11-18.md, issue-215-live-alert-chat-ux-evidence-2026-11-18.md, issue-215-live-populated-states-evidence-2026-11-18.md, issue-215-live-rerun3-evidence-2026-11-18.md, issue-215-live-helper-line-fix-2026-11-18.md.
* docs/reference/research/ux/wcag-conformance-baseline.md: automation does not establish conformance.
* Repository tests already cover the criterion-3 parts: test_alert_chat_plain_language_noncolour_215.py, test_alert_chat_role_wcag_plain_matrix.py, test_alert_chat_keyboard_live.py, test_regulatory_ux_accessibility.py, test_alert_chat_accessibility.py.

## Findings

* Criterion 3 parts (no colour-only, keyboard, plain-language) are covered by existing code and tests and were proven live on 2026-11-18 for the reachable panels. The "WCAG 2.2 AA as written" claim needs person-run assistive-technology review, which the owner waived for the demo; the baseline forbids claiming conformance from automation, so no tickable code gap remains.
* Criterion 5 needs real staff participants. None exist in the synthetic demo and nobody may be simulated.
* No buildable code or test gap was identified that would change either verdict. A fourth live probe would repeat earlier runs.

## Decision

No source change. Record a per-criterion table and stop.
