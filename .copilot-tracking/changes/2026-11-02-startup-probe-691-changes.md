---
title: Startup probe changes for issue 691
description: Implemented changes and validation
ms.date: 2026-11-02
---

## Changes

* Api app probes: Startup 3 s period x 40 (120 s), Readiness 5 s, Liveness 10 s x 6, all with 3-5 s timeouts.
* Resident demo app: same three probes on 8089 `/healthz` with the allowed `Host` header.
* Web client: GET reads and the profile photo retry up to 3 times on 502/503/504 or non-JSON 500 with "The service is still starting" status; vendor script reload now 3 attempts.
* Tests updated and added (see details).

## Validation

* `az bicep build` and `az bicep lint` on both templates: clean.
* `python3 -m unittest tests.test_workspace_scripts` (src/api): 5 pass.
* `python3 -m unittest tests.test_bicep_policy` (infra): pass. `test_resident_demo_deploy` needs `zava_forward` installed in this environment (not part of change).
* No deploy performed; live re-check remains open.

## Divergences

* None. Existing exact-probe assertion in `test_bicep_policy.py` was updated to the new probe set.
