---
title: Research for #159 dataset provenance, licence and DPIA screening register
ms.date: 2026-11-14
---

## Scope

Issue #159: every external dataset records source, licence, retrieval date and permitted use; confirm no real resident data is mixed with synthetic data.

## Evidence

* `docs/reference/research/retrofit-synthetic-data/provenance-register.json` (v1.2.1) listed 5 sources with licence, attribution, url and retrieval_date but no permitted_use and no resident-data flag.
* `privacy.source_issues` checked licence, attribution, url and retrieval_date only. No check tied dataset `sources` to registered sources.
* The ERA5 weather packet (`docs/reference/research/climate-paired-source-178/open-meteo-era5-durham-2023-2024-metadata.json`, retrieved 2026-10-27, CC BY 4.0, C3S reuse legally unverified, owner approval synthetic-demo-only) was not in the register. DS-SENSOR listed no sources.
* NASA POWER MERRA-2 sensitivity data: licence text not retrieved (HTTP 403, 2026-10-22). Kept out of the register and logged as an open item.
* Existing tests (`src/core/tests/test_synthetic_provenance.py`) cover public payload labels and source audit.

## Planning readiness

Ready. Disposition: executed.
