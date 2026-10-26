<!-- markdownlint-disable-file -->
---
title: Issue 349 image no-cache correction 2 plan
description: One correction cycle: shared no-cache build argv for scanned images
ms.date: 2026-10-26
---

Research: ../../research/2026-10-26/issue349-image-no-cache-correction2-research.md
Details: ../../details/2026-10-26/issue349-image-no-cache-correction2-phase-details.md

* [x] Phase 1: Research.
* [ ] Phase 2: Independent critique before any source edit.
* [ ] Phase 3: Edit tools/rpi-checks.py (one helper, two call sites) and tools/test_rpi_checks.py.
* [ ] Phase 4: Focused tests and py_compile; fresh changed-path evidence under the non-blocking heavy lock; independent review; commit.
* [ ] Phase 5: Prospective integration plan, then normal merge of fresh origin/main; bounded integration review; commits. No full gate.

Constraints: no Trivy ignore, baseline, threshold, scanner or DB change; no
Dockerfile, dependency or CI workflow change; no prune or deletion of old
evidence; no push or PR/issue edit; one correction cycle for this finding.
