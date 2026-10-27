---
title: Neutral household exercise component evidence
ms.date: 2026-10-27
---

Refs #181. Refs #177. Branch feat/household-conditions-181-stack.
Common base e7d531c789dbaafafc05fb4cacf7d851e188cd58.

## Implementation and Boundary

Versioned, ID/seed-specific independent fixture profiles and dated conditions.
Explicit distributions for schedules, setpoints, occupancy, ventilation and
drying/moisture; no demographic inputs or resident assessments.
Declined/unknown synthetic monitoring yields no profile/conditions/RNG draw.
Original stock ID retained. No private register or household data read.

Not yet integrated with writer/projection; does not replace existing stock,
grant fictional consent or imply actual observed household behaviour.

## Validation

19 focused tests PASS: test_household_conditions (five) and test_sensor_stock
(14). Includes 3,000 profiles against declared equal-choice
shares/ranges, schedule endpoints, deterministic subset/order/seed checks,
neutral closed output shape and monitoring exclusions. Targeted Ruff,
format check and mypy PASS. Initial line-length and strict re-export typing
findings were fixed before this passing run.

## Original Acceptance Audit

Independent exercise component supplies documented household variation and
no monitoring output for declined/unknown. Existing writer exclusions retained.
No original checkbox ticked: full projection/writer integration and independent
Review remain outstanding. Draft child, do not merge.
