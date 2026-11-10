---
title: Issue 1384 workspace exhaustion oracles review
description: Single post-implementation review of the checker-only change
ms.date: 2026-11-10
ms.topic: reference
---

## Execution

* One Review, executed after `implement-done`, by an independent read-only code-review agent over the working-tree diff and `src/api/checks/script_retry.py`. No second review is run in this task.
* Assessed boundary: base `477d7b7a91639e072ab17d0fbad8142e8b3cb4fe` plus the uncommitted source in the four files listed in the changes record.

## Outcome

* Reviewer: no significant issues, nothing blocking. No production file touched; oracles derive from the declaration and are checked against the real loader in the Node VM test; controls require the exact `expected X, observed Y` message; the parser fails loudly.
* Reviewer did not run the browser checks. Author evidence: `employee_workspace_browser_check.py` exit 0 (evidence `04-after-employee_workspace.*`); `workspace_scripts_browser_check.py` exit 1 after its exhaustion, missing-global and all four control checks passed (evidence `04-after-workspace_scripts.*`, `05-rerun-workspace_scripts.*`).
* Outcome: conformant for the checker oracle scope; scripts check not observed green overall because of the held finding below.

## Routing

* Held distinct finding: pre-existing race in `delayed_companion` (`assert len(pending) == 1`), 1 of 16 failures on the unmodified function (evidence `06-baseline-delayed-companion-probe.*`), outside the owner-permitted oracle scope. Route to a later Research or Plan task.
* Follow-up: align the lenient `loading_briefing_browser_check.script_attempts` with the strict helper.
