<!-- markdownlint-disable-file -->
---
title: Issue 349 image no-cache correction 2 research
description: Make the gate's image builds execute apt-get upgrade instead of reusing stale layers
ms.date: 2026-10-26
---

## Problem

The correction-1 handoff showed the failure comes from cached upgrade layers in
the runner's plain docker build; warming the host cache only hides it until a
prune or a new advisory. The coordinator rejected that as non-durable. Goal:
a security-validation build that always executes the existing apt-get upgrade.

## Prior art read (tools/rpi-checks.py, tools/test_rpi_checks.py)

* Runner.image() (about line 1364) builds each project and the logo stress image
  with ["docker","build","--memory=3g","--cpu-quota=200000","-f",...,"-t",tag,context].
* Receipt verification (about line 556) rebuilds the same list for the four
  project images and logo-0600 from the receipt identity, in an explicit
  expected-command list. Both sites must stay identical or verification drifts.
* Only the four project images are Trivy scanned (fixable gate, full report,
  SPDX). The logo-0600 build is a non-scanned api image with a 0600 logo mode;
  the loop skips scanning for it. No Dockerfile or CI workflow reuse: hosted
  src-ci.yml builds on clean runners and is not changed.
* test_rpi_checks.py has GateTests with a fixture Runner and patch.object on
  Runner.command; no existing assertion pins the docker build argv.
* No ruff or mypy installed in the system python; the runner is validated by its
  own unittest and py_compile. The gate environments (/venvs) hold their own
  tools; no installs here.

## Options

1. Add --no-cache to all four scanned project builds only, through one shared
   helper used by both the build and the verification sites. Narrowest reliable
   change. Cost: each gate rebuilds all layers (pip wheels, apt) and re-downloads
   them; longer gate, more network.
2. --no-cache also for the logo build: unscanned, so it gains nothing for
   security validation and costs time. Not changed.
3. --pull: changes only base freshness; the base is digest-pinned by design, so
   it would not help and could contradict the pin. Rejected.
4. Cache-busting ARG in each Dockerfile (date or version): hidden state or a
   fixed-date bypass, four source files. Rejected.
5. Pruning the host cache before the gate: shared mutable state, outside the
   runner's contract. Rejected.

Chosen: option 1. Pinned base, scan flags and non-root checks are unchanged.
Docker build cache entries from the gate use --no-cache: BuildKit then ignores
cached layers for that build (it still writes new ones, so root disk use per
gate rises; root has 6.4 GB free, monitored).

## Evidence plan

Capture to files under /mnt/ama-rpi-gates/issue349-image-correction2 (private):
commands, exit codes, image identity, dpkg-query for libssl3 and openssl in all
four images, hashes of the retained and new gate JSON reports. Retained gate1 and
correction1 reports stay as is; their missing versions and exit codes are not
reconstructed. Fresh evidence comes from one changed-runner path exercise
(Runner.image for the four projects) under the non-blocking heavy lock, not a
full gate.

## Readiness

Ready. Tests: add focused cases pinning --no-cache for scanned builds, absence
for the logo stress build, equality of the build and verification argv, and the
pre-existing memory and cpu flags.
