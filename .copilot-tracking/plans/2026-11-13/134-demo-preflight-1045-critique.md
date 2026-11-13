---
title: Issue 134 demo preflight plan critique
ms.date: 2026-11-13
---

Independent rubber-duck critique, verdict: Proceed with changes. Executed once.

Applied (compatible with brief):

* Use `--no-index`/no build isolation where local setuptools exists; disable bytecode writes (`PYTHONDONTWRITEBYTECODE=1`); verify origins via concrete submodules.
* Set `ZF_DATA` to an explicit temp JSON path in a `/tmp` working dir rather than the default; `ZF_DOC_STORE=local`; fresh temp live/audit paths for `Store`.
* Run tests by explicit paths/discovery with `PYTHONPATH` limited to `src/core/tests` and `src/agents/tests` (never `mvp`), as the repo guidance shows.
* Archetype and damp count come from the generator simulation (`prop.archetype`, `prop.damp_reports`) or are marked unverified; sensors are separate backfill data, reported Not run if no consent fields.
* Call `home_case_view` with a staff record from `store.data["staff"]`; capture exit codes immediately.

Disposition of one item: `test_case_journey` uses a loopback HTTP server (no external network); the brief requires it, so it runs and loopback use is recorded. Any skip is reported.
