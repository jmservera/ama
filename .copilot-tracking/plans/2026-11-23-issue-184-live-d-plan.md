---
title: Issue 184 live plan d (2026-11-23)
description: Plan and one-pass critique for a wire-body secret allow-list regression
ms.date: 2026-11-23
---

Tier: focused (test-only, no src change). Plan: add one test in `src/api/tests/test_iot_credential_hygiene.py` asserting every published body is a JSON object with no secret-named key and no repository secret pattern in any field. Run that module, ruff format and check.

Critique (executed once): the key-name regex could false-positive on legitimate fields; the test runs on actual payloads, so a failure is informative. Proceed. No live Azure change; live body proof stays unproven (network blocked, see bodyread note).
title: Issue 184 live run d plan and critique
ms.date: 2026-11-23
---

Plan: add `CliLeakTests` to `src/api/tests/test_iot_credential_hygiene.py` driving `live_simulator.main` with hostile env values and an exception carrying a credential; assert stderr, stdout and captured logs never contain the marker, `SharedAccess` or `HostName=`, and exit codes are the stable 2 or 4. Test only; focused tier.

Critique (executed once): verdict proceed. Probe showed current behaviour already clean, so the test is a regression guard, not a fix. Risk: patching `store_home_ids` couples to a module attribute already patched in `test_live_simulator.py`; accepted. Details: `.copilot-tracking/details/2026-11-23-issue-184-live-d-details.md`.
