---
title: Issue 230 r7 research
ms.date: 2026-11-05
---

## Scope

Recheck issue #230 (programme manager and coordinator screens) against merged work before choosing a slice. Disposition: reused (existing evidence adequate). Planning Readiness: Ready (outcome is no new code slice).

## Evidence

* Merged: #662 (screens), #781 (keyboard and axe browser proof), #818 (withheld-items panel), #854 (design-system class guard), #931 (browser check hardening), #969 (queue paging), #1127 (status record, 2026-11-04).
* Issue comments: criteria 1, 2, 3 and 5 ticked; criterion 4 unmet (2026-11-04 RPI check).
* Focused check run on this branch: `tests.test_programme_screen` in `src/api`, 16 tests, OK.
* Issue #155 (user and assistive-technology testing) is still open.

## Unmet

* Criterion 4 (WCAG 2.2 baseline acceptance with textual state meaning and keyboard navigation): needs assistive-technology testing and human review under #151 and #155. Automated keyboard and axe checks exist but do not establish conformance.

## Follow-ups

1. Assistive-technology and manual WCAG test of the programme screens (human, #155).
