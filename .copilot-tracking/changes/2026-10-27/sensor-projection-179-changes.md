---
title: Indoor exercise projection child evidence
ms.date: 2026-10-27
---

Refs #179. Refs #177. Branch feat/indoor-projection-179-stack.
Common base e7d531c789dbaafafc05fb4cacf7d851e188cd58.

## Implementation

Extracted legacy equation to a typed, versioned helper with explicit input
domain. Generator delegates without changing arithmetic/RNG order.
Helper is fingerprinted; manifest binds version/equations/exercise domain.
This intentionally changes provenance metadata, not supported reading values.

No private stock or approved climate records were read. Existing per-ID fabric
and stock choice exclusions are retained. Exercise fallback is authorized by
the owner's #178 comment; historical/scientific acceptance remains blocked.

## Validation

48 focused tests PASS: test_indoor_projection, test_sensor_backfill,
test_sensor_stock, test_sensor_faults, test_sensor_plausibility,
test_synthetic_determinism. New/changed tests and helper pass Ruff and mypy.
Existing backfill tests emit unclosed-file ResourceWarnings; no test fails.
Initial run exposed the existing exact dependency-set assertion's dependence
on list length; updated that tightly coupled assertion for the new helper.
Initial mypy findings in new guards/test narrowing were fixed before this
passing run. Tests include 1,500 exact equation/RNG
comparisons, domain endpoints/nonfinite/singularity errors, construction
direction, helper fingerprint sensitivity and actual manifest binding.

## Original Acceptance

Inputs/equations/version and explicit exercise parameter classification are
implemented in code/README/manifest. No issue checkbox is changed: independent
Review remains pending and record-grounded physical bounds are UNMET.
No claim of sourced building physics or integrated new retrofit/household model.
