---
title: Local full-gate Chromium output-path failure
description: Created bug and exact failed full-gate evidence, separate from deployed app observations
ms.date: 2026-10-31
ms.topic: reference
---

## Created Issue

* Issue: #608, https://github.com/jmservera/ama/issues/608
* Created: 2026-10-31, after the 16:27:48Z browser failure.
* Template: generic; .github/ISSUE_TEMPLATE absent.
* Labels/assignees/type: none specified.
* Title: fix(gate): long external output paths crash Chromium process-singleton socket
* Scope: local tooling, not a deployed Azure defect or an application fix.

## Reproduction and Evidence

* Unchanged full gate at candidate 37cc1fed15a95f1bc84e82135b0c496862867e85,
  base 7136be9778b17e495b1941e6eb93f50d32de8a2b; long external session-files
  output path.
* checks.case_journey_browser_check launched persistent Chromium with profile/
  extension and TMPDIR inside that output. Chromium process-singleton socket
  pathname exceeded the platform limit; FATAL Socket path too long, SIGABRT.
* Failure command window: 2026-10-31T16:26:24.224183Z to 16:27:48.426292Z.
* External receipt:
  /home/azureuser/.copilot/session-state/3a44be57-db3a-46d1-b9e4-fe82bd7c74e7/files/rpi-live-full-main-integrated/receipt.json.
* Browser log 0157-browser.log SHA256:
  24620a9b6a4c69b8e8c6bc68ece24d7d6fa876a3f35095a4ebb17fbbef9e5a2e.
* Full receipt failed; SQL blocked by browser prerequisite. Project/static/
  infra/migration and image groups passed, not a substitute for full acceptance.
* Expected: clear early path admission or owned short browser scratch, preserving
  privacy/cleanup/receipt and required browser/SQL execution.
* Open criteria: path behavior, regression/ownership contracts and actual full
  browser/SQL zero-skip evidence.
* A short-output recovery is planned; no source repair or successful retry is
  inferred. Original full failure and original RPI Review remain immutable.
