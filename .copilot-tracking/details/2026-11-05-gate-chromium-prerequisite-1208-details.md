---
title: Gate Chromium prerequisite details (#1208)
description: Phase details for the Chromium ordering repair
ms.date: 2026-11-05
ms.topic: reference
---

## Phase 1: regressions

* tools/test_rpi_checks.py: three tests. Success: they fail on base ead177e (no install in the contract or runner) and pass after Phase 2.

## Phase 2: repair

* tools/rpi-checks.py: Runner.install_chromium runs the existing playwright install under the output-scoped PLAYWRIGHT_BROWSERS_PATH; required_checks adds the same command after the api install; verify_commands then rejects receipts lacking it.
* Out of scope: SQL, security, human and closure gates, check names, EXPECTED_SKIP_REASONS.

## Phase 3: validation and native admission

* Native check, when the heavy lock is free nonqueued: isolated venv, playwright install, run test_resident_summary_ai_ui with zero skips. If held, record as unproven.

