# Plan critique (rubber-duck, independent) - verdict: Revise, then applied

Blocking findings and dispositions:

* Fallback must respect skill scope: applied (skill_sources filter).
* Fallback citations need own source map: applied (exact rules facts).
* Failure metering end-to-end: tested at the panel boundary with a raised exception; caller wiring is outside the write surface.
* Banned terms in case values: documented known limit.
* Write surface exceeds constraint: fixed to four files.

Non-blocking applied: no MAX_SOURCES raise (prompt budget), disclaimer first, unblock precedence first, settlement resets source.
