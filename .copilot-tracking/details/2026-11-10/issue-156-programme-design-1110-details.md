# Details: #156 Programme queue/paging proposed v1 design (2026-11-10)

Plan: [plan](../../plans/2026-11-10/issue-156-programme-design-1110-plan.md).

## Design content (P1)

Version label `programme-queue-paging-v1`, status PROPOSED, pending named review.

1. Status and scope box: partial scope = Programme queue screen `programme-queue`, roles listed as installed in source at the pin; not all #230 roles, not 74 designs, not whole #156 C1.
2. User and task goal: a programme user finds returned or handed-off cases across the permitted cases, keeps the chosen home, and recovers from a failed load without losing context. Anchored to programme journey 1 and UX-02/03/07.
3. Current (pin) versus proposed table: rows F2 two lists, F3 reset on select, F4 no row link, F6 end-of-list controls, F7 retry, F8 filtered-empty wording, F12 narrow order. Each proposal is labelled proposal and owner decision where it changes behaviour.
4. Components with labels and status text: page heading, evidence boundary, selected-home context line, page position line, scope filter, Apply, Reset, pager, status region, table, side list.
5. State inventory with wireframes: ready, loading first load, loading next page (rows kept), filtered-empty, genuinely empty (total 0), page failure (rows kept, Retry), first-load failure, denied, role-unavailable, session ended, invalid page.
6. Task flow in text (steps and branch to recovery).
7. Desktop and narrow wireframes with numbered reading/focus order; focus rules (no focus theft on page change; Retry failure focus; reset focus).
8. Page-local versus portfolio semantics table: what a number refers to.
9. Safe error/recovery/manual boundary: read-only; manual route is the existing case workspace and the user's own work list; no contacts invented.
10. Content and accessibility considerations aligned with Fluent 2 native semantics and WCAG baseline; unmet evidence listed.
11. Evidence/approval gaps and owner decisions (O1 offset in URL, O2 merge lists, O3 row link, O4 page size confirmation, O5 supported devices, O6 help route).

## Register note (P2)

One additive paragraph after the #230 row, dated 2026-11-10, naming exact partial scope; no row text edited.

## Index and log (P3)

Extend the existing #152 workbench navigation row or add one row adjacent for the Programme queue design; append log entry.

## Validation (P4)

Relative links resolved by script; `python3 tools/check-design-trace.py` exit expected 1; `python3 -m unittest tools/test_check_design_trace.py` if offline-capable.
