---
title: Plan for #159 provenance and DPIA screening validator
ms.date: 2026-11-14
---

## Phases

* [x] Register: add `permitted_use` and `contains_real_resident_data: false` to every source; add `SRC-OPEN-METEO-ERA5`; cite it from DS-SENSOR; add the NASA POWER open item; bump to 1.3.0.
* [x] Validator: `source_issues` requires permitted_use and `contains_real_resident_data is False`; new `dataset_source_issues` rejects unregistered or duplicate sources, sources carrying resident data and missing personal_data statements; wired into `public_issues(check_sources=True)`.
* [x] Tests: weather source, flag mutation (True, None, "false", missing) and dataset cross-checks in `test_synthetic_provenance.py`.
* [x] Validate: ruff check, ruff format (line length 100), focused unittest, CLI `--sources`.

## Critique

One pass, self-critique: strict `is False` avoids truthy strings; NASA POWER excluded rather than recorded with unverified licence. No conflicts with decisions.
