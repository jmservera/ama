---
title: Issue 2201 live8 critique
ms.date: 2026-11-23
---

Verdict: approve with direct dispositions. Executed once on the final candidate plan.

* Risk: leaking connection detail through the diagnostic. Disposition: only `type(exc).__name__` is kept; test uses a `KeyError` carrying a marker string.
* Risk: changing the stable `IOT_CALLBACK_FAILED` code. Disposition: code unchanged; class name is a separate attribute and stderr line.
* Risk: claiming the 09:30 to 11:30 cause. Disposition: the change makes later failures attributable; the past cause stays unproven.
* Scope: src change, so full tier; no `rpi-checks.py --all` by the worker; targeted tests, mypy, ruff only.
