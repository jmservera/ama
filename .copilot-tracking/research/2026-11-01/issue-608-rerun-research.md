---
title: Issue 608 rerun research
ms.date: 2026-11-01
---

* Disposition: reused. Planning Readiness: Ready.
* Main at b9ac50935 already contains the preflight from PR #610: `admit_browser_output` in `tools/rpi-checks.py` rejects an output path whose owned `<out>/tmp` plus the Chromium singleton suffix exceeds 107 bytes, before any check runs.
* Regression test `test_chromium_output_byte_boundary_matches_linux_socket` binds a real AF_UNIX socket at the 107-byte boundary and fails at 108.
* Criterion 3 needs an actual full gate on a stable head; this task is barred from `--all`, so it cannot be proven here.
* Prior evidence: issue-608-remaining-* artifacts (criterion 3 open, RV-001).
