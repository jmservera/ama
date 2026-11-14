---
title: Epic 165 seed reproducibility research
ms.date: 2026-11-14
---

Research disposition: executed. Planning Readiness: Ready.

## Findings

* `synthetic/stock_register.py`: seeded `SYN-nnnnn` register; manifest has `source_type=SYNTHETIC`, seed, revision and file hashes.
* `synthetic/scale_fixture.py`: seeded homes, households and retrofit case events (`is_synthetic`, `HH-SYN-` refs, reserved `TE[0-8] 1ST` postcodes).
* `synthetic/sensor_backfill.py`: seeded IoT readings with `SYNTHETIC` source type.
* `synthetic/privacy.py`: `PATTERNS` (email, phone, NI, postcode) and `record_issues`.
* `src/importer` is an XLSX import/export tool with no generator; out of scope for fixtures.
* Gap: no dedicated PAS 2035 case generator exists. The scale fixture's case events and stages are the only seeded case fixture, so the test covers those and states the gap.
* `determinism_audit.py` audits byte identity but has no UPRN check or per-record provenance assertions.
