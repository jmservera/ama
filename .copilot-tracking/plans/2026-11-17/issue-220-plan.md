---
title: Issue 220 plan
ms.date: 2026-11-17
---

# Plan

* [x] Add one API regression test: challenge opened with `hazard_concern=True` on a case with a live hazard leaves protected state and hazard clock unchanged and records the referral.
* [x] Record the assessment (criteria 1-4 proven, criterion 5 gaps) in the `src/core/README.md` #220 status record.
* [x] Run targeted tests, ruff format check, mypy for src/api.
* Critique (single pass): scope is a test and a doc note; no store, legal or hazard-clock change. Accepted.
