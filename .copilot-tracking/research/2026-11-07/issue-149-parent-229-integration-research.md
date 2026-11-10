---
title: Issue 149 parent integration of merged child 229 and current main, research
ms.date: 2026-11-07
---

## Research

* Original session 978d4601-9d13-4110-ac90-aea0eac18f18, successor to issue-149-parent-229-prep (light checks, atlas browser run on frozen 660716929024). Disposition: executed (read-only git inspection after fetch).
* Start state: clean, ignored-inclusive empty; HEAD 660716929024aefaee420406d0ff9ba060bb613a, tree 041790b85c78a4f71f2bdaeb9b421fb5218f103c.
* Fresh refs: origin/test/ux-evidence-149 = 4d95c1f3eec6438341b3b5298d2bf4ab58a6b2d6 (tree 26283b6126b6, child 229 PR 1264 merged), a fast-forward descendant of HEAD; origin/main = b284d0d3e8ebed24d40bf9eb1e23de1ae9101d01 (differs from 7c6d only in .github/rubric/scores/latest.json). Main is not assumed to be 7c6d.
* Dry run (read-only merge-tree): parent 4d95 then main b284 merges with no conflict; merged tree 7ba1ca7f. Expected path delta over 660716929024 from the child: data_operator_ai_state.py, data_operator_browser_check.py, test_data_operator_ai_state.py, src/api/README.md and its RPI artifacts, kept byte for byte.
* Main-relative source delta of the merged tree (non-RPI): atlas_tensions_browser_check.py, data_operator_ai_state.py, data_operator_browser_check.py, three api test files plus test_data_operator_ai_state.py, test_role_screens_conformance.py, doc_controls.py (two exception strings), src/api/README.md and four UX docs. No UI, API, model, SQL, security or schema change.
* Incoming main touched src/core test inventory pins (1263): test_needs_inventory.py and test_scenario_manifest.py must be run.
* Tier: FOCUSED manual, conditional on doc_controls.py staying message-only and no product path change after merge; any wider delta means FULL and stop.
* Not decided here: Human/Legal release, assistive-technology, usability, whole 149 and 229 acceptance, live serving model. Both issues stay Refs only.
* Planning Readiness: Ready.
