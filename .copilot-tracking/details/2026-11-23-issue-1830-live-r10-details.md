---
title: Issue 1830 live r10 details (2026-11-23)
ms.date: 2026-11-23
---

* `load_receipt`: wrap `json.loads`, require an object.
* `commands_of`: require a non-empty list of objects with string `group`, list `argv`, aware parseable `started` and `finished`, with `finished` not before `started`.
* Tests: parametrised malformed bodies and non-JSON receipt, each expecting exit 2 and `REFUSED`.
