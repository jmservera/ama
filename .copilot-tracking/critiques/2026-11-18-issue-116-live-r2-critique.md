---
title: Issue 116 live r2 critique
ms.date: 2026-11-18
---

Executed once on the final plan. Verdict: proceed.

* Blocking 1: a second role may be obtainable by creating a throwaway Entra user. Disposition: probed read-only first; directory privileges are insufficient, so the attempt is recorded as blocked rather than forced.
* Blocking 2: zero hits on exact strings could be misread as a full leak proof. Disposition: limit stated in the note.
* Non-blocking: avoid real AI calls; applied.
