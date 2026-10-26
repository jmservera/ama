<!-- markdownlint-disable-file -->
---
title: Issue 349 image no-cache correction 2 review
description: Independent review return for the no-cache runner correction
ms.date: 2026-10-26
---

Executed once in native session bfe8a55b-19b6-41a6-a0c7-c6c25bc06037 on
2026-10-26 (code-review agent, read-only) against commit 709cb5c4 and the
evidence in /mnt/ama-rpi-gates/issue349-image-correction2. Return preserved
verbatim below. Bounded to this correction; not whole-issue acceptance.

## Original return (verbatim)

**Verdict: Approve. No blocking issues.**

Low:
1. Disk figure in the changes record does not match the evidence. The record says
   "Root disk fell from 6.4 to 6.0 GB free"; df-after.txt shows 5.7G available.
   Suggested fix: correct the figure to 5.7G, or say it was measured at a
   different time.
2. Negative test gap (already disclosed in the record). Nothing proves that
   verify_commands rejects a receipt whose scanned build lacks --no-cache.
   verify_commands compares argv exactly against required_checks, so rejection
   follows. The new test pins five builds, with only logo-0600 lacking the flag.
   Receipts created before this change will fail the updated verifier; this is
   intended and stated in the record.

Verified, no issue:
* Both sites call image_build_argv. Runner.image uses fresh=not stress;
  required_checks uses fresh=name != "logo-0600". The logo build keeps the old
  argv with no --no-cache.
* git show --stat lists only the tools files and the changes record; no
  Dockerfile, trivy.yaml or ignore changes.
* 14 tests pass (tools.test_rpi_checks OK); the two new tests assert on real argv
  from both call sites.
* All build-*.exit and trivy-*.exit files contain 0.
* versions-*.txt shows openssl and libssl3 3.0.22-1~deb12u2 in all four images.
* All four *-gate.json files contain 0 vulnerabilities and 0 fixable; run.sh used
  --ignore-unfixed --exit-code 1 --severity HIGH,CRITICAL.
* The apt-get upgrade step is not CACHED in any build log; only the base FROM and
  WORKDIR steps are CACHED.
* The four argv-*.json files match the helper output.
* hashes.txt covers the gate files, versions and ids; sha256sum -c was not re-run.
