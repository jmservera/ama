---
title: Issue 1830 live r12 details (2026-11-24)
ms.date: 2026-11-24
---

Phase 1: edit the one containment line in the map check (`r.top >= p.top - 1 && r.bottom <= p.bottom + 1`). Phase 2: rerun the check directly with axe-core 4.10.3 (sha256 prefix 880970c081707360) six times, plus tests, ruff and mypy. Phase 3: note, README row, log entry, changes record. Success: reruns pass at load above 20 or the residual is stated.
