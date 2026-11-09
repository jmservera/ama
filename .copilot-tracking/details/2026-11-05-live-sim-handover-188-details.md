---
title: Details for #188 live-sim handover omission correction
ms.date: 2026-11-05
---

* Phase 1: `src/api/tests/test_sensor_consistency.py` `LiveEnvelopeReplayTests`: raw replay stays exact; handover with a live row is refused (library, replay and CLI exit 2 with unchanged store); legacy-only window still passes.
* Phase 2: `sensor_handover_verify.py` refusal; `src/api/README.md`.
* Phase 3: lint, type and focused tests; clean-freeze of own-generated caches under the retention policy; commit.
