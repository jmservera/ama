# Issue 350 r7 critique (2026-11-23)

Executed once on the final candidate. Verdict: proceed.

* Risk: tool must never print credentials or send them; it uses anonymous GET only, no credentials at all. Accepted by design.
* Risk: classifying 302 as pass would hide the defect. The tool reports `fail` for any browser-style API 302 and `pass` only for 401 on all API probes and redirect on pages.
* Risk: tool must not claim an acceptance. Header states it is a measurement, not an exemption proof. Applied directly.
