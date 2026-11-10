---
title: Details for issue-136-c5-technical-retry-1110
description: Exact edits for the resident test module
ms.date: 2026-11-10
---

## Edit set (infra/tests/test_resident_demo_deploy.py only)

1. Add `import importlib` and `from typing import Any`; replace `import resident_demo_deploy as DEPLOY  # noqa: E402` with `DEPLOY = importlib.import_module("resident_demo_deploy")` after the existing `sys.path.insert`.
2. `compiled()` returns `dict[str, Any]`.
3. `TemplateTests` gets class attributes `template: dict[str, Any]`, `resources: list[dict[str, Any]]`, `app: dict[str, Any]`; `setUpClass` returns `-> None`.
4. Wrap line 133 as `ruff format` does.

## Changes record

Remove only the final empty line of the C4 changes record; original bytes and sha256 `06ab9ef0...1327` are preserved at `proof/c4-changes-original-e3.bytes`.

## Validation

As in the plan; `/tmp/c4mutate.py` is reused unchanged for the four mutations.
