<!-- markdownlint-disable-file -->
---
title: Issue 349 image no-cache correction 2 phase details
description: Steps, files and acceptance
ms.date: 2026-10-26
---

* Step 3.1: tools/rpi-checks.py: add a module-level helper image_build_argv(dockerfile, tag, context, *, fresh) returning docker build, then --no-cache when fresh, then the existing --memory=3g and --cpu-quota=200000, -f, -t and context. Use it in Runner.image (fresh = not stress) and in the receipt-verification command list (fresh = name != "logo-0600").
* Step 3.2: tools/test_rpi_checks.py: tests that (a) fresh builds contain --no-cache and keep the memory and cpu flags, (b) the stress build has none, (c) Runner.image issues the helper's argv for a project (patching command) and not for stress.
* Step 4.1: PYTHONDONTWRITEBYTECODE=1 python3 -m unittest tools/test_rpi_checks.py; python3 -m py_compile (bytecode to /tmp).
* Step 4.2: flock -n /tmp/ama-rpi-heavy.lock; for each of four projects run the changed build argv from the frozen candidate source (helper output used literally), dpkg-query openssl and libssl3, run trivy fixable gate with the runner's flags, record exit codes, image ids and report SHA256 to files. Root space checked before and after.
* Acceptance: all four images show openssl and libssl3 deb12u2 or later, exit 0, zero fixable findings; Dockerfiles unchanged.
