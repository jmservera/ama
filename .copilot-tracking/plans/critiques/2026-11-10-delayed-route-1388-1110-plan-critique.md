---
title: Issue 1388 delayed-companion route-delivery plan critique
ms.date: 2026-11-10
task_id: 1388-delayed-route-1110
---

## Execution

Critique executed once on the final candidate plan and details, 2026-11-10, before any source edit. It was a same-agent self-critique (no nested agents were launched, as the brief forbids new agents), so it is not independent review. Verdict: proceed with the amendments below, applied directly to the details. No finding conflicts with a confirmed decision, and no significant or divergent issue needs a user decision.

## Findings and dispositions

* Patching `monotonic` on the original checker would raise `AttributeError` and make the red result a setup error instead of the count failure. Applied: `create=True` so the original routine reaches `assert len(pending) == 1`.
* The sentinel must not fire for the pre-count `page.locator("#workspace-status")` used by `expect`. Applied: the sentinel arms only after the DOM-ready signal.
* The regression must not rely on a fixed sleep. Applied: delivery is gated on the routine's own `wait_for_timeout` pump, with a fake clock that advances only there; the original fails because it never pumps.
* The `session_ended` variant calls `page.route` again before its first `evaluate`. Applied: the double keeps the first handler and the sentinel is armed on `evaluate` too.
* A loop that only waits for a non-empty `pending` could miss a duplicate arriving later. Accepted residual: the control proves duplicates delivered before the check fail; no universal loader guarantee is claimed, and later request-count assertions stay.
* A prompt delivery must not add waiting. Applied: the loop condition checks `pending` first and the prompt case asserts zero pumps.
* Real-browser flakiness could block the "all own checks pass" rule. Applied: runs are predeclared and finite, failures are preserved, and no rerun-until-green or longer timeout is allowed; a failed own check goes to Root.
* `checks/*.py` is excluded from `ruff format`; the new test is formatted and strictly typed. No change.
* README documentation is unchanged because the variants, names and commands are recorded in the RPI artifacts as the issue requires. Accepted.
