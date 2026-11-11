---
title: "Review: issue 1362 inherited one correction"
description: Single post-implementation Review of the exact Current design version field assertion
author: Copilot
ms.date: 2026-11-10
ms.topic: reference
---

Executed once, by the author after implement-done (no nested agent). This is a self-review, not product approval and not independent exact-head review, which Root must perform before publication. Assessed boundary: the two-file checker and unit-test change at the frozen local commit, focused owner demo tier.

## Outcome

Conformant on the local evidence for the authorised scope; no material finding open. Independent exact-head review and publication gates remain pending (not satisfied here).

## Findings (routed, none reopens this task)

| # | Observation | Routing |
| --- | --- | --- |
| 1 | Critique finding 4 named `innerText`; the final helper reads `textContent` after the 320px failure. `textContent` still rejects `1<span>0</span>` (`10`) and any hidden extra text, so it is stricter, not weaker. Disclosed divergence, covered by the changes record. | None; for the independent reviewer. |
| 2 | Visibility relies on `checkVisibility()` default, which does not report `content-visibility: auto` skipped content; the non-blank text check carries that risk and passed at 1280px and 320px. | Later work only if the independent reviewer disagrees. |
| 3 | The unit doubles cover the Python decision logic; the in-page script is proven only by the browser mutation controls (external diagnostic, not a committed regression). | Later, optional: a committed native negative control needs a fresh authority decision. Not authorised here. |
| 4 | `design_name` and the latest note remain whole-panel substring checks (unchanged, out of scope). | Later, separate work if wanted. |
| 5 | Allowance: one inherited cycle debited; conservative remaining minimum 0; exact balance UNKNOWN. No second correction or retry is allowed in this task. | Root. |

## Scope check

Source diff is exactly `src/api/checks/atlas_tensions_browser_check.py` and `src/api/tests/test_atlas_tensions_checker.py`; no app, panel, CSS, fixture, schema, role, identity, policy or backend change. Evidence: baseline reproduced the D1 false positives on current main; the amended candidate passed the full Atlas browser check (370 PASS, 1280px and 320px), 17 unit tests, role conformance, atlas trace, Ruff lint and format, strict mypy; every diagnostic negative failed at the new assertion and the correct value passed. Attempt 1's 320px failure is preserved as adverse history.

## Limits

No assistive technology, WCAG, usability, production, live or whole-issue acceptance. The D1 Playwright 1.64.1 and harness-leak records stay adverse for D1; this task used the declared 1.64.0 pin in an own environment.
