<!-- markdownlint-disable-file -->
---
title: Issue 349 image-scan correction 1 phase details
description: Steps, commands and acceptance for the focused demonstration
ms.date: 2026-10-26
---

* Step 3.1: non-blocking flock probe of /tmp/ama-rpi-heavy.lock; hold the lock for the duration via flock -n; if busy stop. Check root free space first.
* Step 3.2: from the clean frozen candidate /mnt/ama-rpi-gates/issue349-candidate-0fe8c3be: docker build --no-cache --memory=3g --cpu-quota=200000 -f src/api/Dockerfile -t zava-forward-api:i349-correction1 src. Record installed openssl/libssl3 versions with dpkg-query in the image.
* Step 3.3: run src/check-container.py api <image id> using the existing namespace environment; run trivy exactly as the runner (same config, severity HIGH,CRITICAL, --ignore-unfixed, --exit-code 1) with cache under the /mnt output dir.
* Step 3.4: remove only the tag created for this demonstration; keep outputs.
* Step 4.1: if clean, no Dockerfile change. If not clean, inspect which layer holds the finding before any edit.
* Step 4.2: run existing focused image tests (infra tests referencing Dockerfiles) in the existing environment; no installs.
