<!-- markdownlint-disable-file -->
---
title: Issue 349 image-scan correction 1 research
description: Root-cause research for the four failed image scans of gate1 on 0fe8c3be
ms.date: 2026-10-26
---

## Failure (retained evidence, read-only)

Gate /mnt/ama-rpi-gates/issue349-0fe8c3be-gate1 on 0fe8c3be (base c8d16059)
failed image-api, image-agents, image-orchestrator and image-importer. The
retained *-gate.json reports show one finding family in all four: Debian
CVE-2026-84782, HIGH, packages libssl3 and openssl, installed 3.0.22-1~deb12u1,
fixed 3.0.22-1~deb12u2. Scan config src/trivy.yaml has no ignore file or
baseline; the fixable gate uses --ignore-unfixed.

## Source and runner facts

* All four Dockerfiles use the same digest-pinned python base in both stages and
  the final stage already runs apt-get update && apt-get upgrade -y before
  adding the app user. So the source already requests in-image security upgrades.
* The runner (tools/rpi-checks.py image()) calls plain docker build with no
  --no-cache and no --pull. Docker therefore reuses cached layers.
* The gate log for image-api shows the stage-1 apt-get upgrade step as CACHED
  (the layer text is unchanged, so its cache key is unchanged). A cached upgrade
  layer freezes the package versions at the day it was first built, so a
  later Debian advisory is not picked up. Host Docker has a large retained build
  cache (about 770 entries).
* The vulnerable installed version equals the pre-fix version, consistent with a
  layer built before the fixed openssl was published.

## Hypothesis (to be tested, not yet proven)

Stale cached apt layer, not a missing upgrade. Test: one fresh build with the
apt layer rebuilt, scanned with the exact configured fixable-gate command, with
installed openssl version shown. Same cause is shared by all four images since
they share the identical cached upgrade step pattern; only api is rebuilt for
the demonstration to limit root disk use (6.8 GB free).

## Options

1. No source change; refresh the stale cache (rebuild without cache). Simplest,
   matches the rule not to change source gratuitously if the cache is the cause.
2. Add a cache-busting build ARG to Dockerfiles: shared source change in four
   files, new pattern; rejected unless option 1 cannot be made reliable.
3. Change the runner to --no-cache/--pull: tooling change that alters every
   gate and receipt semantics; rejected for this bounded task.
4. Any Trivy ignore, baseline, threshold, scanner or DB downgrade: forbidden.

## Readiness

Ready to test the hypothesis with option 1. Operational note: the next full
gate uses plain docker build, so cache staleness must also be cleared on the
host before admission (cache-only prune), a Docker-state step to be decided.
