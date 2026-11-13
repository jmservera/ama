---
title: "#144 C1 plan critique"
ms.date: 2026-11-13
---

Executed once (rubber-duck). Verdict: Revise. All findings compatible, applied directly; no user decision.

* PC-001 applied: README says "per the Bicep configuration and current code", not observed deployment.
* PC-002 applied: timeout derivation scans upward from 1 until the first rejected value and asserts the cap is found below a 1000 s ceiling.
* PC-003 applied: replace_worker uses an iteration cap through `alive`, asserts ack happened and cancels nothing it does not own; a hard timeout is not claimed.
* PC-004 applied: infra/README.md:1627 corrected to separate standby from enabled-but-misconfigured.
