---
title: Issue 86 light propagation of local parent e888a49 details
description: Commands and checks (Refs #86)
ms.date: 2026-11-08
---

Scratch `/home/azureuser/.local/share/ama/gates/g86-e888-light-1108` (new, root disk); `PYTHONDONTWRITEBYTECODE=1`; synthetic `ZF_DATA` under scratch; import-origin printed for `zava_forward.core.store`; installs only after real missing-import failure. Selectors: core `tests.test_resident_decisions`, `tests.test_ranking_publication`, `tests.test_ranking_publication_runner`; API `tests.test_ranking_publication_wiring`-style modules changed by the parent (`test_exception_register_screen`, `test_data_operator_screen`, `test_ranking_publication_wiring`, `test_workbench_live_defaults`); core strict mypy; ruff check and format.
