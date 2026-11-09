---
title: Research for #185 truthful action report (corrective)
ms.date: 2026-11-06
---

* Disposition: executed. Forward corrective cycle on frozen head `117d58c17f3a53c8c957f4c2a4969c054096b387` (tree `d7eff9232beb4c814bac010d4c34db99ff25e9f3`); original records are preserved unchanged.
* Confirmed original chronology failure: `/tmp/rpi-185.log` creates `device_provision.py` at line 678 and `test_device_provision.py` at line 681, but writes RPI artifacts only from line 710. The initial implementation was not prospective. This is recorded, not waived or backdated; this cycle writes research and plan before any test or source edit.
* Root independent assessment of 117d: REVISE. `report()` always returns `credentials = "none created or stored; references only after a live run"`, which is false after an applied provision with injected adapters (3 references stored, mode `applied`).
* Contract reviewed (whole bounded CLI): dry run is the default and touches no adapter; `--apply` needs a named owner, then both adapters, else fixed-code refusal exit 2; the CLI supplies no adapters so it cannot write; errors are fixed codes; declined or unknown-consent homes get no identity; the version, field names and types are unchanged. The existing test pins the false string at `test_device_provision.py:43` for the dry run only.
* Teardown with the original unissued manifest works because `run_references` discovers owned references; no missing-manifest defect exists and none is invented.
* Module docstring claims the module cannot write; true only for the CLI, not for injected trusted adapters. Clarify.
* Out of scope: adapters, credentials, schema, owner decision, cloud. Tier FULL; this continuation runs source and light checks only. The receipt `/tmp/g185-full-r7-1105/receipt.json` applies only to 117d.
* Planning Readiness: Ready.
