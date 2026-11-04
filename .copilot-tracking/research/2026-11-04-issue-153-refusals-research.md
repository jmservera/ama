---
title: Research, issue 153 refusal wording slice
ms.date: 2026-11-04
---

## Findings

* Merged delivery: PRs #242 (standard, glossary, guard), #402 (chat copy), #501 (content audit), #668 (core-flow copy, generic error), #805 (finance decision label). Criteria 1 and 4 are met; 2, 3 and 5 are open.
* Disposition: Research executed; Planning Readiness Ready.
* Gap found: server refusal strings in `finance.py` ("already on hold", "Release the hold first") and `ai_tasks.py` ("on hold for a fresh review") still use banned vocabulary and omit the next action. No test asserts the old strings.
* Other typed errors (`workflows.py`, `hazard.py`, `doc_controls.py`, `gates.py`, synthetic modules, `signoffs.py`) remain, and are routed later.
* Human blocker: criterion 5 needs named human review of resident wording.
