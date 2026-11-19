---
title: Issue 126 research, frozen protocol, benefits register and release gates
ms.date: 2026-11-17
---

# Issue 126 research (opening)

* Base: origin/main eb51af5c9ab0b1353ac380fc8960ee8dd96d17c4; branch docs/frozen-protocol-126; tier FOCUSED.
* Scope: assess, evidence only; demo-first, desktop-only. Measure/reproduce first, then smallest fix plus regression test.
* Excluded: #1818/#1641 scope (core mssqlstore, chat grounding). No push, no PR, no heavy gate.
* Research disposition: executing (findings appended below).

## Evidence (measured 2026-11-17 on the worktree at base eb51af5c9)

Worktree validation used `PYTHONPATH=src/core/src:src/agents/src:src/api/src` because the editable installs point at the main checkout.

| Check | Result |
| --- | --- |
| `src/core` `python3 -m unittest discover -s tests -p test_governance.py -q` | 75 tests OK, 16 skipped (opt-in task-owned loopback SQL, not run) |
| `src/core` `-p "test_rai_*.py"` | 27 OK |
| `src/api` `-p "test_*gov*.py"` | 10 OK |

## Criterion assessment (issue body as of this date)

* Unchecked and human/cloud gated, not provable by code: protocol/DPIA/lawful-basis approval before Phase 0 capture; tracked residual/unassessed dispositions with qualified owners; fresh current-source assessment; qualified owner acceptance; real AI/SQL/Azure build contract. None is newly supported; no tick is proposed.
* Checked: release decisions, breach pause, BG-011/MDE, benefits-register AI cost line, booked destination, economics in releases. Code and tests exist for each (`governance.py`, `test_governance.py`).

## Defect found by inspection (to reproduce)

RULE-024 and AC-078 require a breach to pause the affected home, work package, archetype or workstream. `breach_record` accepts all four scope kinds and reports them as Paused, but `guard_case_event` checks only home (case id, address) and archetype (home type). A work-package breach therefore pauses nothing: case workflows continue while the register shows Paused. A workstream has no data-model mapping to a case, so it cannot be enforced without inventing one.

Planned smallest fix: also check `work package` scopes against the case's active work orders (`procurement.work_orders`, case_id match, ISSUED/APPOINTED/COMPLETED). Workstream stays recorded-only and is documented as such in `src/core/README.md`.

Planning Readiness: Ready.
