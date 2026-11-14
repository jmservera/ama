---
title: Epic 149 form error summary associations research
ms.date: 2026-11-14
---

## Scope

Focused validation tier. Refs #149. Stacked child branch `test/demo-149-form-error-summary-associations-0501`.
Research disposition: executed (direct source reading of `src/api/src/zava_forward/api/web/*.js`).

## Findings

* Eight `setAttribute("aria-invalid", "true")` sites are pinned by `test_accessibility_baseline.py`: assistants.js:68, ops.js:184, 439, 534, progress.js:82, app.js:528, panels.js:479, role-screens.js:1416.
* Every site pairs with an `aria-describedby` that names a message element id built in the same file.
* Field focus on marking: assistants, ops (note, version), app, panels call `.focus()`. Recorded gaps with no field focus: ops.js:534 (native `oninvalid`), progress.js:82, role-screens.js:1416.
* aftercare.js marks invalid through a spread attribute (`"aria-invalid": error ? "true" : undefined`), so it is outside the counted baseline. It has the only error summary (`#ac-error-summary`, `role="alert"`, `tabindex="-1"`, anchors `#ac-<name>` matching field ids) and `acFocus` moves focus to it.
* No script renders `.stack` or traceback text. Copy uses "Enter ..." plus Owner and Next action wording; async-action.js appends owner and next action to unowned messages.

## Planning Readiness

Ready. No web source change is needed; test-only addition.
