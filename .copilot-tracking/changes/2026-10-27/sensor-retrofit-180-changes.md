---
title: Dated retrofit exercise component evidence
ms.date: 2026-10-27
---

Refs #180. Refs #177. Branch feat/retrofit-effects-180-stack.
Common base e7d531c789dbaafafc05fb4cacf7d851e188cd58.

## Implementation and Boundary

Typed independent dated synthetic measure/effect contract. Uses exact stock
home IDs supplied by callers, no generated replacements or private source
reads. Fabric-loss multipliers activate inclusively at recorded completion
instants, combine deterministically and do nothing without matching history.
Supported effects/version/equation and explicit failures documented.
Does not modify the writer or invent source completion dates; integration
remains blocked with #183. All effect magnitudes are exercise values.

## Validation

18 focused tests PASS: test_retrofit_effects (four semantic tests) and
test_sensor_stock (14 regression tests). Targeted Ruff and mypy PASS.
Timing includes one second before, exactly at and one second after completion;
future and other-home measures remain inactive. Order, cumulative effects,
empty history, duplicate IDs and invalid/non-synthetic inputs are covered.

## Original Acceptance Audit

Unit component proves inclusive timing, documented exercise direction/size and
no-history neutrality. It does not prove a generated home history uses actual
#173 dates or that #179/#183 integration exists. No original issue criterion
ticked. Independent parent Review pending. Draft child, do not merge.
