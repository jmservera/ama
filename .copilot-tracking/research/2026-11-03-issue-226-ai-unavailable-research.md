---
title: Research, issue 226 asset and board view AI-unavailable state
ms.date: 2026-11-03
---

## Scope

Issue #226 (Refs only), branch feat/issue-226-r3. Task slug issue-226-ai-unavailable. Research disposition: executed (merged PR and main-code check).

## Already delivered (do not redo)

* #639 read-only view, #710 cross-home stock conflict queue, #771 phase check and benefits table, #800 browser check. All merged.
* On main, `asset-board` in `src/api/src/zava_forward/api/web/role-screens.js` shows conflict comparison with source age, owner and status, eligibility Unknown with owner, missing investment inputs, phase checks, separate portfolio scope, evidence boundary with no approval, and AI cost per accepted outcome beside quality floor, value status and evidence class (never token-only).
* #491 closed unmerged; the closure audit comment of 2026-10-31 predates #639, #710, #771 and #800.

## Gap found

When `/api/ai/report` fails the view silently shows Unknown. It does not say the AI report was unavailable and gives no manual path (repository rule: AI features need AI-unavailable behaviour and manual paths).

## Selected slice

Add an "AI report" row (Loaded or Unavailable) and a "Without AI" manual-path row to the AI cost panel. No data, price or approval change.

## Still unmet

Criterion 4 (WCAG 2.2 acceptance, assistive-technology testing, #155 and #151) and criterion 5 (full design-system adoption #150, human review) remain unproven by engineering checks. Criteria 1 to 3 and 6 have code and test evidence on main but need human validation (#155); not ticked here.

## Planning readiness

Ready. Validation tier: focused (web copy only; no security, infrastructure, SQL or deployment).
