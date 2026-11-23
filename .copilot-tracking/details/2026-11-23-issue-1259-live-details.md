---
title: Details, issue 1259 live run 8
ms.date: 2026-11-23
---

Phase 1: scenarios return the sentinel path whose existence is unchanged after operations. The unsearchable parent scenario skips when `os.geteuid() == 0` and registers a cleanup that restores mode 0o700. No src change.
