---
title: PR 1654 Cycle 1 mypy plan
ms.date: 2026-11-14
---

* Type the Provider factory as `Callable[[], Any]` before calling it.
* Use `# type: ignore[misc,unused-ignore]` on the Base subclass so configured and ad hoc runs both pass.
* Verify focused unit test, ruff check/format, and three mypy variants. No push, no uv, no full discover.
