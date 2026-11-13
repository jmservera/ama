---
title: Role 231 Technical and Quality renderer web-guideline review research
description: Bounded static research for the named unperformed current web-guideline review of the installed #231 renderers
ms.date: 2026-11-13
---

## Scope and disposition

* Research disposition: executed, bounded, one attempt, native claude-sonnet-5.5.
* Base: main 347962dace94171724cc8db4044c8d783335fecf, branch review/demo-role231-web-review-0835. src tree d6a78d52e9e31ce123c0c788c6c8f6ff7cca25a1 (git rev-parse HEAD:src).
* Named gap: trace 6cd98f5bb disclosed no current web-guideline review and no keyboard/browser/AT witness. Data/contract tracing and the 16 Node renderer tests are not repeated.
* Source read: `src/api/src/zava_forward/api/web/role-screens.js` lines 1-48 (screen helpers), 114-147 (assetDate, assetAgeDays, assetStatus, invoked by Technical), 532-663 (signoffState, technical-queue, qualityMeasures, qualityNext, quality-queue). Invoked DOM helper `h` in `app.js:21-35`. Styles actually reached: `style.css` lines 48, 86, 134-135, 223-225, 289-290, 300-303, 320, 323, 330 and the forced-colors block at 190.
* Declared constructed states (static requirement context, not observations): `src/api/checks/role_screens_browser_check.py` selectors 231 and 231q (negative), 231p and 231qp (positive), lines 25-80ish. No browser, test, SQL, Docker or cloud call was made.

## Evidence retrieved

* Web Interface Guidelines: complete `command.md` fetched in full (single retrieval, not truncated) from https://raw.githubusercontent.com/vercel-labs/web-interface-guidelines/main/command.md on 2026-11-13. Output format: grouped `file:line - finding`.
* Skills loaded: `.github/skills/web-design-guidelines` and the installed accessibility skill entry. `.agents/skills/` does not exist in this worktree, so design-taste and redesign skills named by repository guidance were unavailable (disclosed; not applicable to a read-only review of non-public screens).
* Owner standards consulted by targeted reading (grep of headings and rules, not a full end-to-end read): `docs/reference/research/ux/design-system.md` (lines 94-136, 157-159: table region, status line glyph plus words, empty state, blocked container), `wcag-conformance-baseline.md` (lines 23-55: WCAG 2.2 AA target, tables, status messages 4.1.3 partial), `content-standard.md` (grep only; plain-language rules not fully read).

## Planning readiness

Ready: bounded source, fetched rules and static-only method are fixed.
