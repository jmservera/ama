<!-- markdownlint-disable-file -->
---
title: Issue 349 image-scan correction 1 changes
description: Root cause and cache-refresh evidence; no source change
ms.date: 2026-10-26
---

## Root cause

All four final-stage Dockerfiles already run apt-get update and apt-get upgrade
on the digest-pinned base. The failed gate's plain docker build reused a cached
upgrade layer (logged CACHED) frozen before Debian published openssl and
libssl3 3.0.22-1~deb12u2, so installed 3.0.22-1~deb12u1 (CVE-2026-84782, HIGH)
remained. Stale cache, not a missing upgrade. The old resident PASS predates the
advisory and does not show current images are clean.

## Evidence (external, private; /mnt/ama-rpi-gates/issue349-image-correction1)

Run from the frozen clean candidate 0fe8c3be under the heavy lock (non-blocking
flock), with the unchanged src/trivy.yaml and the runner's fixable-gate flags
(severity HIGH,CRITICAL, --ignore-unfixed, exit code 1):

* docker build --no-cache of api, importer, orchestrator, agents: all built
  with libssl3 and openssl 3.0.22-1~deb12u2 installed (apt-cache policy shows
  installed equals candidate, so the fixed package was available, not mirror lag).
* Trivy fixable-gate exit 0 for all four fresh images.
* Plain (cached) builds afterwards: api and importer reused the refreshed layer
  (deb12u2). Before refreshing, orchestrator and agents plain builds still gave
  deb12u1 (CACHED), so their cache entries are separate; after their own
  refresh, plain builds gave deb12u2. All four plain builds now yield the fixed version.
* Files: build-*.log, plainbuild*-*.log, trivy-*.log, *-gate.json, versions-*.txt, run*.sh.

The gate1 output /mnt/ama-rpi-gates/issue349-0fe8c3be-gate1 and its failed
receipt, and all older receipts, environments and candidates, were not touched.
Only image tags created here were removed; the build cache was not pruned.

## Changes

No Dockerfile, runner, scanner config, dependency or test change. No Trivy
ignore, baseline, threshold, scanner or database change. Only dated tracking
artifacts are committed.

## Residual and limits

* The host cache now holds refreshed layers, so a plain-build gate should
  scan clean. A new advisory or a cache prune would change that; staleness is a
  recurring property of the runner's cached builds, left unchanged here.
* Focused checks: 35 tenant-preflight tests and 7 container-contract tests pass.
  This is not a full gate: no fresh complete gate exists for the current head,
  and old receipts stay historical. Not whole-issue or live-tenant acceptance.
