# C1 research: red heading-hierarchy test and mypy error (Refs #149)

* Disposition: executed. Planning Readiness: Ready.
* Finding 1: the failure was a test race, not a template gap. `render` navigated by hash on the same page, so `#app h1` matched the previous view's DOM. Role views `#/overview` were read while the staff list (h2 Filter first) was still shown. Failing subtests varied between runs (2 of 6 cases), and the app code renders `h1` first in `overviewView`.
* The recorded list gap (`#/`, `#/all`, filter and briefing headings before h1) is genuine, disclosed and shrink-only. No HTML change was made, so Fluent 2, WCAG baseline and the browser-recipe SHA are unaffected.
* Finding 2: mypy error at landmarks test line 83 was `no-untyped-call` on `App(...)`. The repo convention is a targeted `# type: ignore[no-untyped-call]` (see `test_case_journey.py`).
* Base SHA note: the stack base resolves locally as 14f6ce45e2cd40d1d5c64b9850b54c5caa59272f.
