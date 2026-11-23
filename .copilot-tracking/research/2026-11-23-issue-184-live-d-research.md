---
title: Issue 184 live research d (2026-11-23)
description: All three criteria are ticked; the one unproven element is secret absence in telemetry bodies
ms.date: 2026-11-23
---

Research disposition: reused. Planning Readiness: Ready.

Issue #184 has three criteria, all ticked. Prior notes (recheck, bodyread, child stories, chain) prove child closure, no real devices and source/log secret absence. Live Event Hubs body reads are blocked: public network access disabled, local auth disabled, and a bodyread attempt failed with CBS token errors. Enabling access changes the estate, which is not authorised.

Code-satisfiable gap: `test_iot_credential_hygiene.py` checks wire payloads only for the marker and `SharedAccess|HostName=|PRIVATE KEY`. It does not pin the body schema to an allow-list of non-secret keys nor run the repository secret PATTERNS over every emitted body. Target: add that regression.
title: Issue 184 live run d research
ms.date: 2026-11-23
---

Planning Readiness: Ready (research executed, reused earlier c/b research for the criteria state).

Issue body (REST, 2026-11-23): all three criteria are ticked. The residual unproven part is whole-source/log/telemetry secret exclusion. Runs b and c covered the publish path and the receive `decode` path.

New code angle: the simulator CLI `live_simulator.main` surfaces (stderr, stdout, log) are not covered by `test_iot_credential_hygiene.py`. Hostile operator environment values (`ZF_SIM_HUB_HOSTNAME`, `ZF_SIM_APPROVAL`, `ZF_SIM_RESOURCE_GROUP`, `ZF_SIM_CERT_DIR`) may contain a connection string and must not be echoed in "Cannot run" messages, and an unexpected exception carrying a credential must collapse to `SIM_FAILED`.
