<!-- markdownlint-disable-file -->
---
title: Issue 349 image no-cache correction 2 changes
description: Runner builds scanned images with --no-cache; focused evidence
ms.date: 2026-10-26
---

Chronology (2026-10-26): review-return preservation commit eb41a6b4; research,
plan and details written and critiqued (once, rubber-duck: Revise, no blocking)
before any source edit; prospective artifacts committed as 19b6feb1; source edit
and evidence run afterwards.

## Source changes

* tools/rpi-checks.py: new image_build_argv(dockerfile, tag, context, fresh) used
  by Runner.image (fresh unless the logo stress build) and by the receipt
  verification command list (fresh unless logo-0600). Scanned project builds now
  run docker build --no-cache with the unchanged memory, cpu, -f, -t and context.
* tools/test_rpi_checks.py: two tests: helper argv (flag position, other args
  unchanged, absent when not fresh) with required_checks yielding five builds where
  only logo-0600 lacks the flag; Runner.image builds with and without the flag.
* Dockerfiles, trivy.yaml, scanner version, CI workflow: unchanged. No ignore,
  baseline or threshold.

## Critique dispositions

* Add negative receipt-mutation test: partly accepted. verify_commands compares
  argv exactly to required_checks, which the new test pins, so no separate
  mutation test was added; this is a disclosed gap, not a verified rejection run.
* State receipt compatibility: accepted. Receipts created before this change,
  whose scanned build argv lacks --no-cache, will fail the updated verifier by
  design (security-contract change). Historical receipts remain historical.

## Validation

* PYTHONDONTWRITEBYTECODE=1 python3 -m unittest tools.test_rpi_checks: 14 tests OK.
* Heavy lock acquired non-blocking (lock.txt: acquired). Evidence directory
  /mnt/ama-rpi-gates/issue349-image-correction2 (private): argv-*.json, build-*.log
  and .exit (all 0), trivy-*.log and .exit (all 0, retained fixable gate flags,
  scanner 0.76.0, DB copied from correction 1), *-gate.json (zero findings each),
  versions-*.txt (openssl and libssl3 3.0.22-1~deb12u2 in all four), id-*.txt,
  hashes.txt, df-after.txt. Own temporary tags removed afterwards; nothing pruned.
* Build logs: the Dockerfile upgrade step (stage-1 2/6) was not CACHED; only the
  pinned base FROM and the build-stage WORKDIR (metadata) were CACHED.
* Not done: full gate; whole-image-set run via Runner.gate end to end (the
  exercise used the helper's literal argv outside the runner); ruff and mypy (not
  installed, no installs permitted).

## Limits

Focused evidence of the changed build path, not a gate, not whole-issue or
live-tenant acceptance. Root free space was 6.4 GB before the run, 5.7 GB in df-after.txt (taken before own tags were removed) and 6.0 GB after removal.

## Independent review dispositions (original return preserved in reviews/)

* Low, disk figure mismatch: accepted and corrected above.
* Low, negative-test gap: already disclosed; unchanged.
* Verdict Approve, no blocking issue; bounded to this correction, not whole-issue.
