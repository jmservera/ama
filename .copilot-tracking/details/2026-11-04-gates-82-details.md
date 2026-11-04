---
title: Issue 82 gates details
date: 2026-11-04
---

## Slice 1

* `gates.evidence_gate(missing, owner, on)`: pass when none missing, fail listing kinds, unknown when None.
* `Store._evidence_missing` maps the case checklist, None on malformed data.
* `require_booking_gates` appends the evidence gate; existing prior checks unchanged.
* Tests in `src/core/tests/test_gates.py`.
