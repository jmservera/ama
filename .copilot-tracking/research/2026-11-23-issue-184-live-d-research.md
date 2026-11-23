---
title: Issue 184 live research d (2026-11-23)
description: All three criteria are ticked; the one unproven element is secret absence in telemetry bodies
ms.date: 2026-11-23
---

Research disposition: reused. Planning Readiness: Ready.

Issue #184 has three criteria, all ticked. Prior notes (recheck, bodyread, child stories, chain) prove child closure, no real devices and source/log secret absence. Live Event Hubs body reads are blocked: public network access disabled, local auth disabled, and a bodyread attempt failed with CBS token errors. Enabling access changes the estate, which is not authorised.

Code-satisfiable gap: `test_iot_credential_hygiene.py` checks wire payloads only for the marker and `SharedAccess|HostName=|PRIVATE KEY`. It does not pin the body schema to an allow-list of non-secret keys nor run the repository secret PATTERNS over every emitted body. Target: add that regression.
