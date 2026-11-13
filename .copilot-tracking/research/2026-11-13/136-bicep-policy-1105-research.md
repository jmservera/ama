---
title: Issue 136 Bicep policy test environment research
ms.date: 2026-11-13
---

## Scope

Resolve four Wave-1 environmental infra/tests gaps (Refs #136, #137, #360, #110, #142) at base 3b05143179f83235c5b4e80e70aad99bdc44d83f. Research disposition: executed. Planning Readiness: Ready.

## Findings

* test_bicep_policy.py compiles main.bicep, modules/guard.bicep and staff-initializer-rbac.bicep via `az bicep build --file ... --stdout` (subprocess, no login). Cached Bicep exists at ~/.azure/bin/bicep and `bicep` 0.48.1 is on PATH, so compilation is offline. The class skips when `az` is absent unless REQUIRE_AZ_BICEP=1. The Wave-1 failure was a 400s timeout under CPU contention, not a code defect.
* test_staff_azure.py imports scripts credential_arm, staff_azure, staff_blob plus sibling fixtures test_initialize_workbench_staff and test_setup_entra; mocks via unittest.mock; Wave-1 failure was a missing cryptography/azure import.
* test_identity_rbac.py reads role-assignments.json and Bicep text only (static); listed as failing in Wave 1 and expected to pass or fail on its fixture imports.
* test_private_cutover_proof.py loads scripts/private-cutover-proof.py by path, uses MagicMock and a local ThreadingHTTPServer on loopback and patched socket.getaddrinfo; no external network.
* System python3 imports azure, cryptography and aiohttp, so a --system-site-packages venv supplies them offline.
* No test requires Docker, MSSQL, browsers, az login or what-if.

## Unknowns

Whether the scripts import src/* packages (zava_forward.*); resolved by editable installs with --no-deps and a path check.
