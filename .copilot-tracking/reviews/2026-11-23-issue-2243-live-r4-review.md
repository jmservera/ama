---
title: Issue 2243 review r4
ms.date: 2026-11-23
---

Review executed once on the final diff. Outcome: conformant, no open material findings.

* Behaviour stays fail closed; only the reason and label differ when the setting is unset or invalid.
* `expires_at()` semantics unchanged (existing expiry test passes).
* Regression test covers unset, malformed, valid-past and both entry points, and asserts no provider call.
* Residual, routed to later work: the topic-selector adapter `assistant.py` `select()` still reports `not_activated` for this case; roll-out of the image remains owner/registry gated.
