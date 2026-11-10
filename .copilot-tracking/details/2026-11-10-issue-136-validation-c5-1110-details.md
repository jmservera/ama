---
title: Details for issue-136-validation-c5-1110
description: Exact edits for the resident test module
ms.date: 2026-11-10
---

## Edit set (infra/tests/test_resident_demo_deploy.py only)

1. Imports: add `from typing import Any` and `import importlib`; replace `import resident_demo_deploy as DEPLOY  # noqa: E402` with `DEPLOY = importlib.import_module("resident_demo_deploy")` after the existing `sys.path.insert`. Behavior is identical at runtime; mypy treats the attributes as dynamic, so no `type: ignore` is needed. Remove the now unneeded `noqa`.
2. `compiled()` returns `dict[str, Any]`.
3. `TemplateTests` declares class attributes `template: dict[str, Any]`, `resources: list[dict[str, Any]]`, `app: dict[str, Any]`, and `setUpClass` returns `-> None`.
4. Line 133: wrap the `CHAT_RETENTION_DAYS` assertion exactly as `ruff format` would.

## Changes record

Remove the final empty line of `.copilot-tracking/changes/2026-11-10-issue-136-ci-template-c4-1110-changes.md` only, after the original bytes (`proof/c4-changes-original-e3.bytes`, sha256 `06ab9ef0...1327`, commit `e3b7484`) are preserved; the C5 changes record states this is a format-only correction.

## Validation

See plan. Mutations reuse `/tmp/c4mutate.py` unchanged; it must still report each of the four mutants as detected and the unmutated template as passing.
