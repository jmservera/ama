# Plan: resident demo agenda guard (#1053)

Date: 2026-11-14. Critique: one pass, no conflicts (small bounded change; focused tier).

* Add `agenda_available` to the view and keep `callbacks_available` as a compatible alias.
* demo.js keys all callback UI on `agenda_available`; unconfigured lede states that synthetic callback booking is not connected in this showcase environment.
* Connected behaviour and the callback form stay unchanged.
* Update the two test files; run resident tests, accessibility baseline, mypy, ruff.
