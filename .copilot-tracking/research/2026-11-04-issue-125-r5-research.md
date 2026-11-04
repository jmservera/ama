---
title: Issue 125 round 5 research
ms.date: 2026-11-04
---

Research disposition: executed (brief, merged PR evidence, source inspection). Planning Readiness: Ready.

## Evidence

* Brief `docs/brds/retrofit-flow-discovery-brief.md`: Readiness Before Writing the Agent (ten items), Authority and Safety Boundary, Evaluation Criteria (ten measures vs manual analysis, conventional BI, deterministic workflow reporting).
* Merged PR #894 delivered `discovery_assistant_boundary` (readiness gate, default-deny allowlist, read-only toolbox). Its round 1 artifacts record criteria 1 to 3 unmet.
* PR #928 checkpoint lists #125 as open. Main at 6bee46d9d has no evaluation or comparison code.

## Acceptance criteria status before this slice

* 1 Readiness satisfied before connection: unmet (no human evidence exists; gate code only).
* 2 No write access: unmet (code guard only, no runtime denial evidence).
* 3 Compared against manual analysis and conventional reporting: unmet (nothing exists).

## Smallest coherent slice

Criterion 3 scaffold: a pure comparison record holding the ten measures across four methods from human-supplied result pointers, plus a repeatability check for the deterministic-calculation measure. Not security, infrastructure, SQL or deployment; focused tier. Criteria 1 and 2 need owner evidence or a deployed assistant and are out of scope.

## Risks

* Pointers are not verified. The record must not rank or approve; the human owner judges.
* Branch note: the worktree branch is feat/issue-125-r5; the named feat/agent-chat-skills-530 is an unrelated existing branch and was not reused.
