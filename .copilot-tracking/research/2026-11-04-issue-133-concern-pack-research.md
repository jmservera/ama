---
title: "Issue 133 concern pack research (2026-11-04)"
ms.date: 2026-11-04
---
Research disposition: executed. Planning Readiness: Ready.

* Merged delivery for #133: PR 869 (slice 1, `Refs #133`) delivered the store-independent `AftercareRegister` and evaluator view. Other `Refs #133` PRs (996, 841, 700, 699, 635, 631) concern #190 and #193 scenarios and consumer tests. Nothing delivered an AI concern pack. Issue is open with all six criteria unticked.
* `ai_registry.tasks()` lists registered tasks; `assistants.registry` skips disabled tasks, and a non-assistant enabled task needs a legacy binding, so a template-only task must be `enabled=False` as the chat task is.
* Slice 2 choice: criterion 6 (and the text guard for criterion 5). Persistence, API and UI, and the evaluator role (DPO position open) remain later slices.
* Environment note: the editable installs pointed at another worktree, so tests ran with `PYTHONPATH` set to this worktree's `src` trees.
