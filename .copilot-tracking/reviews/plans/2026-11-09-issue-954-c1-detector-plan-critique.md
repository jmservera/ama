# Plan critique: issue 954 C1 checker detector correction (2026-11-09)

Execution: one critique pass by an independent read-only rubber-duck agent over the final-candidate research, plan and details, before the checker edit. Not repeated for this task.

## Verdict

Revise: 4 blocking, 1 non-blocking. All compatible with the owner clarification; applied directly to the details record before this commit; no user decision needed.

## Findings and dispositions

* B1 descendant alerts missed when an ancestor is revealed. Applied: sweep all candidates on every observer batch.
* B2 transient state not reliably captured. Applied: capture outerHTML at evaluation time, add 50 ms interval sweep, add a transient self-test case, record the remaining sub-interval limitation.
* B3 selector missed `[role=dialog]` and backdrop/modal/overlay classes. Applied: narrow additions plus regression cases.
* B4 `aria-hidden` is not visual hiding. Applied: rendering judged by CSS, `hidden` attribute and box only.
* N1 self-test controls. Applied: explicit dimensions, awaited delivery, per-case reset, positive and negative assertions, ancestor-reveal and transient cases.
