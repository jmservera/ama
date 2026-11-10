---
title: Plan for #188 live-sim handover omission correction
ms.date: 2026-11-05
---

* Tests first: reproduce the misleading pass, then split lossless raw replay (direct ingestion, unchanged) from the statistical handover claim.
* `sensor_handover_verify.run` reads `retained_envelopes` once. If any row is `live-sim-reading-v1` it raises `ValueError("HANDOVER_SCHEMA_UNSUPPORTED")` before report and before any replay write. Otherwise the rows equal the `observed_series` projection, so legacy-only handover is unchanged.
* Keep `retained_envelopes` lossless and the indoor-analysis exclusion. No new API, flag, UI, threshold, consent or schema change.
* Docs: api README describes the refusal and the separate future weather-to-weather contract.
* Critique (executed once inline): compatible finding applied (refuse before replay writes so a refused run leaves the store unchanged). Nothing conflicts with confirmed decisions. Verdict: proceed.
* Validation: sensor api and core tests, ruff, mypy with external caches and PYTHONDONTWRITEBYTECODE=1. Tier FULL; the complete gate stays pending, not run here.
* [ ] Human review required and left unchecked.
