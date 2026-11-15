---
title: Epic 165 journey-needs coverage research
ms.date: 2026-11-14
---

Research disposition: executed. Planning Readiness: Ready.

## Findings

* `needs_inventory.py` does not exist; the inventory is `needs-inventory.json` (SN-01..SN-13), bound by `scenario-manifest.json` `inventory.reviewed_rows` and checked by `validate_manifest`.
* Manifest entries (11 profiles, 9 workflows) carry no direct SN references; they resolve through `evidence_index` into `src/api/checks/workbench-manifest.json`, `profile_defaults` and `fixture_contract` case IDs (ZF-1, ZF-4, ZF-5 in `src/core/tests/dataset.py`).
* Seeds: `property-register.csv` and `resident-journey.csv` (property_ref) plus `scale_fixture` homes, households and events.
* Tier: focused (tests only). Stacked on `test/demo-165-cohort-provenance-0432`; `Refs #165`.
