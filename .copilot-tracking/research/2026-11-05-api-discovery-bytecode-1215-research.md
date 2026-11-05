---
title: Research - API discovery source bytecode producer (#1215)
description: Producer, order and environment identities for source bytecode written during project-api discovery in the local gate
ms.date: 2026-11-05
ms.topic: reference
---

## Task

* Issue: #1215. Branch fix/api-discovery-bytecode-1215. Base c6d5a8f3c3a35892322300be27b9747f7b11362d (equals origin/main at start).
* Research disposition: executed. Read-only inspection of the retained failed receipt `/tmp/g96-c6-1105a` (receipt SHA-256 fcd2ba1e47c3c320921790387e4e1f2964cc0395e51fc78e411bb384f5e602e6, status failed, resume_eligible false, head 38dc133f..., base c6d5a8f3...). Nothing in it was modified.
* Sources read: issue text (as data), repository instructions, knowledge-base memory, case-study original (addendum not needed: no product behaviour changes), `tools/rpi-checks.py`, `tools/test_rpi_checks.py`, `src/api/checks/design_system_browser_check.py`, `src/api/checks/chat_widget_browser_check.py`, `src/api/tests/test_chat_widget_layout.py`.

## Observed evidence

* Runner child environment (`Runner.env`, tools/rpi-checks.py lines ~1600-1601) sets PYTHONDONTWRITEBYTECODE=1 and PYTHONPYCACHEPREFIX=<out>/bytecode. `Runner.command` merges it into every child, so the unittest discovery process itself does not write bytecode.
* Receipt row 52 is the project-api `unittest discover -s tests -v` (venv `<out>/venvs/api/bin/python`, PYTHONPATH `<checkout>/src/core/tests:<checkout>/src/agents/tests`), started 2026-11-05T10:20:53.8Z, finished 10:34:17.6Z, exit 0.
* Row 22 (`playwright install chromium`, 10:09:19Z) ran before row 52, so Playwright and Chromium were present during discovery.
* Log 0052-project-api.log line 882: `test_chat_widget_layout.ChatWidgetLayout.test_employee_send_stays_in_panel_at_short_viewports ... ok`. It was run, not skipped. The test skips only when Playwright is missing or Chromium is absent.
* The retained `checkout/` has 68 `*.pyc` files (core, agents and api `__pycache__`), all with mtimes 10:23:53.062 to 10:23:53.401 (about 0.34 s), inside row 52's window. `server.cpython-312.pyc` is the earliest.
* `logo-snapshot/` was created at 10:47:49.79Z by the logo-0600 image group, `shutil.copytree(self.snapshot / "src", ...)`. It holds the same 68 `*.pyc` with the same preserved mtimes. So it is a downstream copy of the already dirty checkout, not a second producer.
* The `api` venv at that point contained `00-rpi-bytecode.pth` (written later by the browser group at row ~156+), so the policy existed only after discovery.

## Producer (code-established, with one inference)

* `test_chat_widget_layout.test_employee_send_stays_in_panel_at_short_viewports` runs `checks/chat_widget_browser_check.py --employee-layout` with `{**os.environ, PYTHONPATH...}`. That child inherits the no-bytecode flags.
* That check calls `design_system_browser_check.main`, which starts `sys.executable -m zava_forward.api.server`. Its env is built from only `PATH`, `HOME`, `LANG`, plus `PYTHONPATH=<ROOT>/src/{core,agents,api}/src`, where ROOT is `Path(__file__).parents[3]`, the snapshot. The no-bytecode flags are dropped, so this server writes `__pycache__` beside the snapshot source it imports. Its `sys.executable` is the api venv python.
* Observed: order, venv, timing, source tree and imported packages (core, agents, api) match. Inferred: that this specific server process wrote the 68 files. The only other candidates, other children in discovery, either inherit `os.environ` or do not import the server tree; no exact PID or audit trace was retained by the failed run.

## Hypothesis assessment

* The issue hypothesis (scrubbed child server drops the flags; the venv `.pth` policy is installed only before the later browser harness) is consistent with the code. The `.pth` install (`tools/rpi-checks.py`, browser group, writes `<out>/browser-bytecode-policy.pth` and `<api venv>/lib/python3.12/site-packages/00-rpi-bytecode.pth`) runs after row 52. Its own comment says the unchanged harness scrubs the server environment.

## Options

| Option | Result |
| --- | --- |
| A. Move the existing `.pth` install to the api venv install step (`Runner._install` for `api`) | Policy exists before discovery. No new mechanism, harness unchanged, scrubbing unchanged, no cleanup or receipt-acceptance change. Selected. |
| B. Add flags to the producer's PATH/HOME/LANG allowlist | Edits application check source and weakens its deliberate env scrubbing. Rejected. |
| C. Exempt dirty snapshot or clean it | Forbidden. Rejected. |

## Risks

* `environment_identity` hashes `.pth` files in `api-startup`. It is computed at finalisation after all installs, so earlier installation does not change the verification model; non-browser api runs now also include the `.pth` in the startup hash. A resume of an older receipt would compare against a venv it never built, which already cannot be reused.
* The receipt requires `browser-bytecode-policy.pth` only when `browser` executed. It must still be written whenever the browser group executes, including `setup-api` only runs that reuse the venv. Writing it in the shared install step satisfies this.

## Planning Readiness

Ready. Tier: FOCUSED (gate tooling, no SQL/security/infra/deploy).
