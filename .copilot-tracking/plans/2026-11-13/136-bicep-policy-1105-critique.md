---
title: Issue 136 plan critique
ms.date: 2026-11-13
---

Independent critique by rubber-duck subagent (single pass), verdict: revise.

## Findings and direct dispositions

* Offline install not enforced: system setuptools 68.1.2 is below the required >=77. Disposition: accepted in part. Upgrading setuptools/wheel inside the venv from the package index is explicitly authorised by the brief; afterwards install with `--no-deps --no-build-isolation` so no further index access is needed. Any other network use stays prohibited.
* Tracking-only writes not guaranteed: accepted. Run with PYTHONDONTWRITEBYTECODE=1. Verified no egg-info exists under src/ beforehand; remove only newly created egg-info directories after the run and confirm `git status --short --ignored` shows nothing new.
* Bicep offline behaviour assumed: accepted. Set AZURE_BICEP_USE_BINARY_FROM_PATH=true and AZURE_BICEP_CHECK_VERSION=false so az uses the PATH bicep 0.48.1 without a version check; no az login or what-if. The real Azure profile is read-only and not used for any resource call.
* Skipped policy suite could look successful: accepted. Set REQUIRE_AZ_BICEP=1 and treat any skip as incomplete.

VERDICT: revise applied; proceed.
