---
title: Issue 1214 creation record
description: Created issue record for the 320px case-summary browser gate regression
ms.date: 2026-11-05
ms.topic: reference
---

## Created Issue

* Issue: #1214, https://github.com/jmservera/ama/issues/1214
* Created: 2026-11-05T11:14:09Z by the coordinator after bounded duplicate searches (320x800, case-summary, case summary, reflow, 320px) found no exact technical duplicate.
* Title: fix(web): recover 320px case-summary browser gate without weakening its contract
* Template: generic; no custom issue template exists. Labels: none. Assignees: none.
* Severity: Medium product-layout regression that blocks the browser prerequisite of the complete local gate.
* Branch: fix/mobile-summary-gate-1214 (worktree issue-1214-mobile-summary), base main c6d5a8f3c3a35892322300be27b9747f7b11362d, declared PR target main. Deliberate independent main-based isolation, not a feature epic child.
* Backlog readiness: READY (backlog-manager refinement, 2026-11-05). Refs #96, #151, #152 and #440. Eventual `Closes #1214` only if every literal criterion below is proven; otherwise `Refs #1214` with the unmet criteria named.

## Supplied Body Summary

* Failure: at unchanged main, existing `checks.case_journey_browser_check` fails at `src/api/checks/case_journey_browser_check.py:1526`; at 320x800 `.case-summary` bottom is 1676.40625, above the 1600 bound that came from #529 and must not be relaxed.
* The browser process exits 1; the diagnostic wrapper echoing `EXIT 1` then returning 0 is not a pass.
* Adverse baseline evidence (external, preserved): /tmp/g96-c6-1105a/receipt.json (failed, scope full, resume_eligible false), /tmp/g96-diag-out/run2.log. MSSQL never ran.
* Scope: FOCUSED tier while genuinely small CSS/layout work; reassess FULL on expansion. Heavy lock /tmp/ama-rpi-heavy.lock held nonblocking for all browser work. The source-bytecode discovery question is a separate tooling investigation and out of scope. No cleanup authorised.

## Acceptance Criteria (verbatim, unticked)

* [ ] Diagnose and record the actual vertical-layout cause; make the smallest Fluent 2-preserving correction against fresh main.
* [ ] Existing exact 320x800 browser contract passes without changing the 1600 bound or hiding, clipping, removing or reordering safety, approval or resident content.
* [ ] Preserve the existing 390px and 1280px behavior, keyboard/manual paths, non-colour state meaning and reduced-motion behavior.
* [ ] Add or strengthen only a focused regression if needed; run the existing exact case-journey browser/axe/keyboard check and relevant existing API layout tests/static checks, recording actual test-process exits and module/source identities.
* [ ] Deliver dated original RPI research/plan/changes/review, current independent exact-head review and required hosted checks. Do not equate focused success with a complete full-gate pass or product accessibility acceptance.

## Planning Comments

* Existing #151 and #152 stay open and broader; this record does not deliver supported-device policy, profile manifest, conformance target or human assistive-technology acceptance.
* Criterion 5 includes independent exact-head review and hosted checks, which this local candidate cannot prove. Expect `Refs #1214` until they exist.
