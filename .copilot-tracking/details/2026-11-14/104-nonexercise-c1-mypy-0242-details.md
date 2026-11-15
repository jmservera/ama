---
title: C1 mypy correction Details
ms.date: 2026-11-14
---

* Add local START, END, CONFIG, MODEL constants.
* Add a local SQLite `Port` with `clock: float` annotation (avoids `no-any-return`).
* Drop the append-only triggers (not needed by these tests).
