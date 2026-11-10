---
title: Ranking archive ancestor durability 1258 continuation plan
description: Plan for the missing boundary and API ancestor-fault tests (LIGHT, tests only)
ms.date: 2026-11-08
---

Tier: final FULL unchanged; this is LIGHT test preparation. Tests only; no production edits. Details inline.

* [x] C1 Core: non-writable ancestor ends the chain (chmod 0o555 on `a`, restored in `finally`, skipped as uid 0). Expect file, link, archive, b only.
* [x] C2 Core: mocked `os.access` True (stand-in for a privileged run; mocked, not live root) syncs b, a, root.
* [x] C3 API: parent-folder fsync fault gives 409 `committed_unconfirmed`, path-free, record and audit kept, repeat still 409, unfaulted retry `written False` with original bytes and valid audit chain. Existing archive-directory tests kept.
* [x] C4 Run only these plus publication selections in a new scratch venv `/home/azureuser/.local/share/ama/gates/g1258-boundary-api-light-1108`; no heavy gate.

Critique: one self-critique only in this LIGHT scope; risk that C1 depends on non-root uid is handled by an explicit skip, recorded as limitation. No independent critique was run for these test-only additions.
