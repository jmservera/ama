---
title: Issue 80 capacity C5 case-journey test failure, research
description: Root cause of the test_case_journey capacityView TypeError after the new export anchors
ms.date: 2026-11-10
---

## Scope and disposition

* Task `issue-80-capacity-c5-1110`, parent `issue-80-c4-validation-1110`. Source pin HEAD `e98453042d05` (tree `469dbba1`), source files identical to `2cc34027`; main `6d4cd624`, no fetch. Research disposition `executed`.
* Root admits C5/5 (final default correction, no C6): reproduce, find the actual cause, smallest root-cause fix, no app fallback for invalid data, no assertion weakening. C4 pass, adverse and process qualifications are preserved. Child 37828a41 reproduced the failure on unmodified HEAD; that is not proof of a pre-existing baseline failure and none is claimed.

## Reproduction (actual)

* `unittest tests.test_case_journey.CaseJourney.test_priority_invocation_and_procurement_preserve_history_barriers` from `src/api`, owned venv, `PYTHONPATH` only the allowed test-helper paths: exit 1, `TypeError: Cannot read properties of null (reading 'nodeType')` at `Node.append` via `Node.replaceChildren`, `show`, `capacityView` (`repro1.log`, `repro1.exit`). A first attempt with a wrong class name (`CaseJourneyTests`) errored on selector only and is preserved as `repro0-wrong-selector.*`.

## Cause

* `capacityView` (`ops.js` lines 489-494) passes `pkgPage.total ? exportLink(...) : null` and the same for work orders as children to `show(...)` and `h(...)`. In this test both totals are 0, so the children are `null`.
* Production contract: `h` skips `null` and `false` children (`app.js` 21-34) and production `show` flattens and filters with `n && n.nodeType` before `replaceChildren` (`app.js` 99-106). Existing app code relies on this (for example `w.state === "Completed" && h(...)`, `extra?.queue ? ... : null`). Rendering `null` children is therefore valid production behaviour.
* The test (`test_case_journey.py` line 435) stubs `show` as `(...nodes) => app.replaceChildren(...nodes)` with no filter, and its mock `Node.append` reads `k.nodeType` on each child. The stub does not honour the production `show` contract, so the new conditional anchors expose the fixture gap. Verdict: fixture drift, not an app defect. The app change that introduced the `null` children is valid; no app edit is needed.

## Decision

* Align only the stub at line 435 to the production filter: `app.replaceChildren(...nodes.flat().filter(n => n && n.nodeType))`. This is the production semantics, adds no fallback to app code, and weakens no assertion. Other stubs that already pass are untouched.
* App UI behaviour does not change, so a new heavy browser run is not required; the source-unchanged whole-run PASS (about 84 s, checker and `web/` hashes unchanged) is carried with hash qualification.
* Scenario manifest binding: not affected (no recipe or manifest touched); an integrity test is run only if the targeted suites show one.
