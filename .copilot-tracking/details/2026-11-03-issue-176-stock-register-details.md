---
title: Details, issue 176 fictional stock register generator
ms.date: 2026-11-03
---

* Phase 1: `write(out, n, seed, as_of)` writes `stock-register.csv` and `manifest.json` through `provenance.prepare_output` (refuses non-empty output). Identifiers `SYN-nnnnn`; RNG keyed by seed and version.
* Phase 2: tests cover byte identity, seed sensitivity, manifest fields, fabric compatibility, non-empty refusal, invalid input.
* Phase 3: `python -m unittest` on three modules, `ruff check`, `mypy --cache-dir=/tmp/mypy-176`.
