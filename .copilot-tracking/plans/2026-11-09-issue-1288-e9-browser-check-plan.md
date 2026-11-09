---
title: Issue 1288 E9 Quality browser check expectation plan
ms.date: 2026-11-09
---

# Issue 1288 E9 browser check plan (prospective)

* Research: O1 (observed in the 440 checkpoint, raw in session files `observed-440-bq-2055/`) exited 1 at `quality_sensors_browser_check.py` line 280: expected "Proposal stored as unapproved", actual "Not sent (real-provider-route-unavailable). Use the ordinary quality check and the manual route; nothing was sent to a model." The check predates E7, which deliberately disables the real-provider route (`Ai.send_fence_supported=False`). Axe was not reached. To be reproduced here with a native run before editing.
* Plan: in the check only, assert the guarded-off refusal and manual path after the simulation request, assert no proposal is stored and no accept control, then seed a clearly synthetic stored proposal directly (existing `seed` helper, model "seed") so the remaining supplied-versus-cited assertions still run. No production change, no `send_fence_supported` enablement, no weakened or removed assertion.
* Validation: one non-queued `flock -n /tmp/ama-rpi-heavy.lock` admission; run the existing check with axe if available locally; ruff check/format and the existing API mypy profile on the check file. No Core/API/SQL/Agents reruns.
* Counters: E9 productive, from the E6-E10 grant; E10 remains. Real-provider simulation stays OFF.
