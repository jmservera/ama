---
title: Issue 530 chat local-unit critique
ms.date: 2026-11-08
---

* Executed: once, final candidate, rubber-duck agent. Verdict: proceed with changes.
* Finding 1 (blocking): `tools/rpi-checks.py` line 935 region includes Docker and Trivy preflight even for `--changed`. Disposition: accepted; Phase 4 is now conditional on trusted runner inspection and stops before any heavy work.
* Finding 2 (blocking): pip installs can fetch build dependencies over the network. Disposition: accepted; install only offline from verified local artifacts, otherwise stop.
* Finding 3: JSON-store methods in `StoredQuestionTests` add bounded coverage. Disposition: accepted; selected by method, SQL methods excluded.
* Finding 4: origin proof must be in-process. Disposition: accepted; wrapper asserts module paths and records counts.
* No conflict with confirmed user decisions; no user decision required.
