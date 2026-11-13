# Critique (rubber-duck, one pass)

Verdict: Revise. Executed before code.

* Blocking: after Previous returns to page 1, syncPager (role-screens.js:344) moves focus from Previous to Next; the later `press_until(page, "Tab", "programme-next", 8)` presses Tab first and would leave Next. Disposition: accepted. Replace with an assertion that focus is already programme-next, then Enter.
* Tab order after fix: disabled Next skipped; Reset is three Tabs from Previous. Confirmed.
* Manifest digests unaffected. Confirmed.
