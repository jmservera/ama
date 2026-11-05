# Plan: issue 233 withheld panels on evidence screens

Research: ../research/2026-11-04-issue-233-withheld-evidence-screens-research.md. Details: ../details/2026-11-04-issue-233-withheld-evidence-screens-details.md.

* [x] Phase 1: add `screenWithheld` to per-home `technical-queue` and `quality-queue` in `role-screens.js`
* [x] Phase 2: add source-level test in `test_role_screens_conformance.py`
* [x] Phase 3: update `atlas-screen-trace.md` tension row; append `log.md` entry
* [x] Phase 4: focused validation

Critique (single pass, self-applied): compatible. Text-only panels reuse the existing component, add no control, change no access, and keep the no-action statement.
