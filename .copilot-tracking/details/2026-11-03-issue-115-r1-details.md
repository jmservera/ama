---
title: Issue 115 round 1 details
ms.date: 2026-11-03
---

* Record format: name to head SHA-256; names must pass the publisher's canonical filename rule.
* Remote anchors reuse the existing validity rules; invalid candidates are reported without names or content.
* Exit codes: 0 match, 1 alert, 2 not configured or missing argument.
* Manual path: reconciliation is a human check; no AI is involved, so no AI-unavailable behaviour applies.
