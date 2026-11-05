---
title: Local gate Chromium prerequisite ordering
description: Created issue record and adverse failed-gate evidence for the project-api Chromium ordering defect
ms.date: 2026-11-05
ms.topic: reference
---

## Created Issue

* Issue: #1208, https://github.com/jmservera/ama/issues/1208
* Created: 2026-11-05 by the coordinator after duplicate searches found no open Chromium/gate repair.
* Template: generic; labels, assignees and type: none specified.
* Severity: Medium. Scope: local gate tooling only; no application, Azure, SQL, security or policy change.
* Branch: fix/chromium-gate-prerequisite-1208 (worktree issue-1208-browser-gate), base ead177ef90d24666557708ea344848a1be43bdf8, PR target main.
* Backlog readiness: Ready. Independent focused tooling; no implementation dependency on #96. It unblocks full validation of #188, #185, #79, #80 and #96 without delivering their criteria.

## Original Adverse Evidence (preserved, not replaced)

* Failed full gate on 2026-11-05, candidate 78ecffc950e4c40a9b6ad3ccabb3dcd634c4acbf, base ead177ef90d24666557708ea344848a1be43bdf8.
* Receipt: /tmp/rpi188-full-20261105T0740/receipt.json, SHA256 72b69ac4d11d7215b3d8c583385c98c6a807d59740cc82a4287000189e399ef8, status failed.
* Source log: /tmp/rpi188-full-20261105T0740/0051-project-api.log, SHA256 27cf8c61e4251f7115f7ed4744a21e945407666854b0db24bfea476607448f1e.
* Failure: project-api reported an unexpected skip, Chromium is not available (src/api/tests/test_resident_summary_ai_ui.py:57), because the runner installed Chromium only in the later browser group. SQL and browser groups did not execute.
* The receipt and log were not modified or reused as evidence for any later head.

## Acceptance Criteria Status (at the local frozen candidate)

* [ ] Focused regression reproducing the ordering defect: met locally (red then green); see the changes record.
* [ ] Resident-summary UI regression executing with the installed browser in the native gate: not proven; native browser check pending heavy-lock admission.
* [ ] Receipt verification enforces the install: met by unit contract tests; native receipt not produced.
* [ ] Existing orchestration regressions and lint/type checks pass: met locally.
* The issue stays open; no closing keyword is justified until native evidence exists.


## Native verification update (2026-11-05 continuation; criteria text above unchanged)

* Criterion 2 now met at c2cca6b3f078a2f15078587c60265811459b0e06: test_resident_summary_ai_ui ran 1 test, OK, 0 skips, with isolated native Chromium; tools.test_rpi_checks ran 85 tests OK. Evidence: changes record and /tmp/ama-1208-native-20261105T0910. Two earlier harness path failures are preserved there.
* No full receipt, SQL or live acceptance claimed. Keep Refs until independent exact-head review, hosted CI and human approval.
