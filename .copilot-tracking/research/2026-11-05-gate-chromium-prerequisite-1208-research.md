---
title: Gate Chromium prerequisite ordering research (#1208)
description: Evidence for the project-api versus Chromium install ordering defect in tools/rpi-checks.py
ms.date: 2026-11-05
ms.topic: reference
---

* Task: #1208, slug gate-chromium-prerequisite-1208. Research disposition: executed (focused code reading plus unit reproduction). Planning Readiness: Ready.
* Sources read: AMA repository instructions, case documents and knowledge base index, tools/rpi-checks.py, tools/test_rpi_checks.py, src/api/tests/test_resident_summary_ai_ui.py, the failed #188 receipt and log (read only).

## Findings

* Runner.run installs each project venv up front, then Runner.schedule runs project-api tests; Chromium was installed only by Runner.browser, which depends on project-api. The runner env sets PLAYWRIGHT_BROWSERS_PATH to out/chromium for every command, so the browser store is already isolated.
* test_resident_summary_ai_ui.py:57 skips with "Chromium is not available: ..." on launch Error. That reason is deliberately not in EXPECTED_SKIP_REASONS, so check_skips raises: the gate fails correctly but the prerequisite is ordered wrongly. This confirms the #188 adverse evidence.
* required_checks is the trusted replay contract used by verify_commands; it matched the runner order, so both must change together.
* playwright is in the api dev extra (src/api/pyproject.toml), so the installed venv can run the existing install helper.
* Other tests that skip with "Chromium is installed by the later browser-check step" remain whitelisted exact skips; not widened or narrowed here.

## Decision

* Install Chromium once, in the project-api group, after the api pip install and before schedule. Keep the browser-group install (idempotent) so its replay contract is unchanged. No skip whitelist, mock or check-name change.
* Heavy admission: /tmp/ama-rpi-heavy.lock held by #96 PID 1232396 at 2026-11-05; only lightweight tests may run now.

