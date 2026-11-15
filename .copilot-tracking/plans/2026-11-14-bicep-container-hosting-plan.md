---
title: Bicep container hosting test plan
ms.date: 2026-11-14
---

* Add DeployedImageAndProbeInvariants to infra/tests/test_container_hosting_completeness.py.
* Validate: ruff isolated line-length 100, az bicep build, unittest discover infra/tests, ruff/mypy per CI.
* Critique: tests are source-text contracts only; no deployed-evidence claim.
