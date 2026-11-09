---
title: Issue 530 C4 API strict-mypy exposure of the core chat privacy test helper research
ms.date: 2026-11-08
---

* Disposition: executed (read-only plus an isolated Main snapshot baseline). HEAD cd7e71fa3 (tree f4a92424), Main 0f05e9aa unchanged on fetch. Refs #530 only. Original session 225166fc.

## Adverse evidence (preserved, external)

* Maintained focused gate `g530-sqlbrowser-r1` failed, exit 1 (native wrapper exit 0). Receipt `/home/azureuser/.local/share/ama/gates/g530-sqlbrowser-r1/receipt.json`, SHA-256 `15adeeff795d96375f186438b2f101759a8d6ecb8bf799383bdb6615dea104e8`, status failed, executed groups preflight, namespace, static, tooling. Failing command: venv API Python `-m mypy` in `src/api` (log `0027-project-api.log`): 73 errors in 1 file, `src/core/tests/test_chat_privacy.py`. API units in `0024-project-api.log`: 2007 tests, OK, skipped=362.
* Browser and mssql were blocked by the failed prerequisite and did not run. No 21-method SQL pass, no three-state Chromium/axe pass and no eligible receipt exists. The refused partial verification stays as recorded.

## Findings

* API mypy configuration (`src/api/pyproject.toml`): strict, `mypy_path` includes `../core/tests`, `files = src, tests, checks`. Legacy test modules are listed with `ignore_errors` plus `follow_imports = skip`; `test_chat_privacy` is not in the API lists (Core lists it only under its own `ignore_errors`).
* Candidate cause: `src/api/tests/test_mssqlstore.py` (this branch, commit 1c771189) adds `import test_chat_privacy as chatprivacy` and the class `MssqlChatPrivacy(chatprivacy.ChatPrivacyBehaviour, unittest.TestCase)`. Main has no API test import of `test_chat_privacy` (grep of the Main tree), so the strict API run never followed it.
* Isolated Main baseline: `git archive 0f05e9aa` to `/tmp/rpi-530-c4/main`, new venv `/tmp/rpi-530-c4/venv-main`, editable installs of Main core, agents and api with the api `dev` extra (`mypy==2.4.0`, `playwright==1.64.0`), package origins under the snapshot. Same command and config (`python -m mypy` in `src/api`, external cache): `Success: no issues found in 190 source files`, exit 0. The first attempt before installing the `dev` extra failed only with 45 `playwright.sync_api` import-not-found errors, none in `test_chat_privacy` (that first mypy log was overwritten by the second run in the same file; the counts here come from the console output).
* Conclusion: not a failure present on Main. It is newly exposed by the candidate import, with `test_chat_privacy.py` byte-identical to Main (`git diff 0f05e9aa HEAD` is empty for it). The 73 errors are untyped defs, untyped calls to the module-level `cp`, and the mixin `ChatPrivacyBehaviour` lacking TestCase attributes (`assertEqual`, `addCleanup`, `make_store`).
* Precedent for the smallest proper typed fixture: `src/core/tests/test_finance_match_controls.py` types a mixin with `if TYPE_CHECKING: _TestCase = unittest.TestCase else: _TestCase = object`. Core keeps `test_chat_privacy` under `ignore_errors`, so annotations do not change Core strictness.
* Rejected options: adding `test_chat_privacy` to the API `follow_imports = skip` list or `ignore_errors` (suppression, forbidden), `Any` casts, runner or workflow edits.

## Planning readiness

* Ready. Correct by annotating `src/core/tests/test_chat_privacy.py` only.
