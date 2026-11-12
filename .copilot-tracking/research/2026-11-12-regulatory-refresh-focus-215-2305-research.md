---
title: Research - keyboard focus after Refresh alerts (#215, finding 215-R1)
description: Evidence for the single admitted finding 215-R1 and its bounded fix
ms.date: 2026-11-12
ms.topic: reference
---

## Scope and disposition

Research disposition: `reused`. The read-only readiness result `rpi-215-readiness-2255-result.json` (external evidence root, not committed) is the only source of the finding. Only 215-R1 is admitted. Owned paths: `src/api/src/zava_forward/api/web/chat.js` (`regulatoryAlertsPanel`), `src/api/checks/regulatory_ux_check.py`, and one description in `src/api/README.md`. Distinct from #233 (queues), #96 (funding) and #216 (citations). Planning Readiness: `Ready`.

## Finding 215-R1

`load()` in `regulatoryAlertsPanel` sets `refresh.disabled = true` and the `finally` block re-enables it. Chromium blurs a focused button that becomes disabled, so a keyboard user who pressed Enter on "Refresh alerts" lands on `BODY` and loses their place (WCAG 2.2 SC 2.4.3 Focus Order, Understanding document fetched 2026-11-12). The harness only mouse-clicks the control (two steps), so the 21 scoped states cannot catch it. The lookup form in the same file already refocuses its input in `finally`.

## Disclosed non-canonical readiness validation

The readiness run used source-package `PYTHONPATH` and the shared editable installs pointed at `/home/azureuser/source/ama/src`, not this worktree. Its 85-test and browser result is not canonical validation and is not reused. A new owned venv (`/tmp/ama-215-own-venv-2305`, pip only) has editable `zava-forward-core/agents/api` pointing at this worktree. Canonical baseline before any edit: 85 tests OK (1 skipped) with only test-helper paths (`tests:../core/tests:../agents/tests`) under `flock -n /tmp/ama-rpi-heavy.lock`.

## Guidance fetched 2026-11-12

* Web Interface Guidelines `command.md` fetched in full: relevant rules are visible focus, async updates in `aria-live`, buttons for actions, submit stays enabled until request starts, no `autoFocus`.
* WCAG 2.2 Understanding SC 2.4.3 (first 3000 characters retrieved; partial).
* Preserve the Fluent 2 design system, plain-language standard and existing `role=status` update; no visual change.

## Scoped history and budget

Scoped history (`git log` on the three owned paths): latest `chat.js` change #1245, harness #640 (2026-11-01), README #1469. No earlier #215 implementation attempt or `215-R1` record exists in the repository. This is one admitted slice; no renewal, reset or borrowed budget is claimed.

## Design constraints

* Recover focus only when the refresh button held focus when `load()` started and focus is still unclaimed (on `BODY`/none) when it finishes. If the person moved focus to another control, or pressed the pointer elsewhere, do not move it.
* Cover success, error and the synchronous law-store-unloaded branch.
* Do not use `aria-disabled` (changes harness and semantics); keep native `disabled`.
* No AC3 conformance and no AC5 staff claim; no ticks.
