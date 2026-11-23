---
title: Issue 2243 review r4
ms.date: 2026-11-23
---

Review executed once on the diff (one test, research note, index, log). Outcome: conformant for the stated scope.

* The test uses the existing fixtures and asserts transport call counts, so a hard-coded expiry would fail it.
* No secrets in the probe result (script asserts credentials absent).
* Open work routed later: tie the live image digest to a commit (needs registry access).
