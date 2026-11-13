---
title: Issue 74 criterion 2 discriminator prospective critique
description: Independent read-only critique of the populated-building probe plan, obtained before any install or run
ms.date: 2026-11-13
---

Verdict: PASS-WITH-FINDINGS, no blocker, executed once before the probe.

* Rows must satisfy exact schema, valid statuses, known scope IDs and decimal costs; invalid data degrades to Unknown, so assert populated rows. Applied.
* Use valid legacy decision statuses (Accepted, Waiting); measure decisions are separate. Applied.
* Assert exact per-store, per-home expected values and exact building rows; check sentinel absence, not absence of all home values. Applied.
* Assert `__file__` origins inside the runner process; use a finance role. Applied.
