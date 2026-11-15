---
title: Issue 1530 C1 fix critique
description: Independent plan critique outcome
ms.date: 2026-11-13
---

Executed once (rubber-duck, before code). Verdict: Revise; no user decision required.

* PC-1 blocking: enlarged root font is not browser zoom. Disposition: applied. Add a 640 px viewport at device scale factor 2 (200% zoom of a 1280 px window) and keep the 320 px root font check separately.
* PC-2 blocking: scan could pass without populated hazards. Disposition: applied. Fixture preserves the fetched case, injects two hazards, and the check asserts two visible safety cards and the panel's field-hint text before each scan.
* PC-3 non-blocking: Sam is not the referral receiver. Disposition: accepted as limitation; the panel is scanned for its populated read view and raise form, receiver forms are covered by unit tests.
* Verified: open hazards render above tabs; manifest binds only workbench_browser_check.py, so no digest edit is needed.
