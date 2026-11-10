---
title: Research for issue-136-validation-c5-1110
description: Exact Ruff, format, mypy and diff-check diagnostics on the C4 head and their base comparison
ms.date: 2026-11-10
---

## Scope

Final admitted C5 (fifth of five) for #136 and #1288. It clears the selected validation failures that the independent C4 review reported on the already modified `infra/tests/test_resident_demo_deploy.py`, and qualifies the C4 evidence transparently. No Bicep, API, Core, Docker or runtime change.

## Evidence (head `e3b74843803c94331bffb049ab6f21027e8b2256`, base `675986755`)

Raw outputs are external under `phase136-validation-c5-evidence-1110/proof/` (`red-*`, `base675-*`).

* Ruff check (`--isolated --select E,F,I,B,UP --target-version py312 --line-length 100`): exit 1, one `E501` at line 133 (106 > 100). The same line and error exist at `675986755` (`base675-ruff-check`), blamed to an earlier commit, so C4 did not introduce it. The module is modified by C4, so the selected check fails on it and the owner does not waive it.
* Ruff format `--check`: exit 1, the same single line 133 wrap (`red-ruff-format.out`); identical at base.
* mypy `--check-untyped-defs`: exit 1, 20 errors, also 20 at base (`base675-mypy`, `red-mypy`). They are one `import-not-found` for `resident_demo_deploy` (imported through a runtime `sys.path` insert) and 19 `attr-defined` errors for `template`, `resources` and `app`, which `setUpClass` assigns without class-level declarations. With `MYPYPATH=scripts` the import resolves but mypy then reports one `import-untyped` inside `scripts/resident_demo_secrets.py`, so the cleaner fix is a runtime import that mypy treats as a module of unknown attributes.
* `git diff --check 675986755..e3b74843`: exit 2, `new blank line at EOF` at line 24 of the immutable C4 changes record (`red-diffcheck.out`). Original blob `e3d090551519ec8137dca78ad4470020d2d50b61`, sha256 `06ab9ef0...1327`, copied byte-for-byte to `proof/c4-changes-original-e3.bytes` before any change.
* The failing CI test itself passes on the C4 head (`red-target`, exit 0).
* Three further mypy errors in `infra/tests/test_bicep_policy.py` are the known baseline diagnostics, outside this module; they stay explicit and unwaived.
* The first C4 E501 output was overwritten in C4 and is lost; it is not reconstructed here. The C4 witness `verify` exit 1 (source already dirty at `implement-start`) is immutable.

## Decision

Wrap line 133, add class-level attribute annotations using the `dict[str, Any]` JSON boundary, load `resident_demo_deploy` with `importlib.import_module` after the existing path insert, and remove only the C4 changes record's trailing blank line after the original bytes are preserved. Leave the three policy-test errors alone.

## Planning Readiness

Ready. If the module does not reach zero Ruff, format and mypy diagnostics within this scope, hold; no broad fix.
