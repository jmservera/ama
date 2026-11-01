---
title: DPIA scope drift guard phase details
description: Detail for P01 to P03
ms.date: 2026-11-01
---

* P01: read the DPIA file relative to the repository root via `Path(__file__).parents[3]`;
  match record-class storage names from `CLASSES` by their leading identifier tokens.
* P02: `python3 -m unittest` in `src/core`; `ruff check`, `ruff format --check`, `mypy` on core.
* P03: Conventional Commit `test(regulatory): pin DPIA scope to retention classes (Refs #217)`.
