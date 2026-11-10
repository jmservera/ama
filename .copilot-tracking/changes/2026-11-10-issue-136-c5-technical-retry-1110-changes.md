---
title: Changes for issue-136-c5-technical-retry-1110
description: Prospective changes record, no implementation edits yet
ms.date: 2026-11-10
---

## Changed files

* `infra/tests/test_resident_demo_deploy.py`: wrapped the `CHAT_RETENTION_DAYS` assertion (line 133); added `import importlib` and `from typing import Any`; bound `DEPLOY` with `importlib.import_module("resident_demo_deploy")` after the existing path insert and dropped its `noqa`; `compiled()` returns `dict[str, Any]`; `TemplateTests` declares `template`, `resources` and `app` class attributes and `setUpClass` returns `None`. No assertion was weakened, removed, ignored or cast.
* `.copilot-tracking/changes/2026-11-10-issue-136-ci-template-c4-1110-changes.md`: FORMAT-ONLY removal of the trailing blank line (diff-check `new blank line at EOF`). Immutable original: commit `e3b74843803c94331bffb049ab6f21027e8b2256`, blob `e3d090551519ec8137dca78ad4470020d2d50b61`, sha256 `06ab9ef060836386e421a6d73b85ce5f177b44c351bec9798287b1c5636d1327`, bytes preserved at `phase136-c5-technical-retry-evidence-1110/proof/c4-changes-original-e3.bytes`. No outcome text changed; the C4 witness verify exit 1 and lost first E501 output are unchanged.

## Results (raw in `phase136-c5-technical-retry-evidence-1110/proof/g-*`)

* Resident module: Ruff check exit 0, format check exit 0, mypy exit 0 (no issues). `git diff --check` exit 0.
* Tests exit 0: CI-regression test, resident module (17), `test_bicep_policy` (60), `test_container_contract` (7), `test_resident_demo_secrets` (16).
* Offline Bicep build and lint exit 0 for main, guard, containerapps, resident-demo.
* Mutations: unmutated pass; inverted, lost-cap-4, resident, default-on each fail (detected).
* Supplemental, unwaived: mypy over `test_bicep_policy.py` exit 1, three baseline errors (2023, 2024, 2047), not touched.
* Unchanged inputs: `src`, `infra/modules`, `infra/main.bicep` and the startup test are blob/tree identical to `675986755` (`identity-src.txt`); image `sha256:d6d6fe32...` present locally and used only as historical evidence, no rebuild or startup rerun, no new startup claim.

## Retained qualifications

C4 verify exit 1 (dirty source), lost first C4 E501 output, first C5 attempt refusal (verify exit 1, files intact), original hooksPath override, C2 spike, C3 duplicate-launch refusal, three baseline mypy errors. None is healed.
