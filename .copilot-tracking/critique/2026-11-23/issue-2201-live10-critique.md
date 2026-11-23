---
title: Issue 2201 live10 critique
ms.date: 2026-11-23
---

Executed once. Verdict: approve. Direct dispositions: print only `type(error).__name__` (no message, no traceback, no args) so the fixed-code redaction contract holds; keep exit code 4 and the fixed line unchanged; test persistence failure with a message containing a sentinel that must not appear on stderr.
