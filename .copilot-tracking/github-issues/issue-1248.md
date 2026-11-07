---
title: Issue 1248 creation record
description: Created issue record for the saved-call History browser readiness failure
ms.date: 2026-11-07
ms.topic: reference
---

## Created Issue

* Issue: #1248, https://github.com/jmservera/ama/issues/1248
* Title: Investigate saved-call History browser readiness failure
* Created: 2026-11-07T11:20:29Z. State at record time: open. Label: bug.
* Template: generic; the repository has no `.github/ISSUE_TEMPLATE` files.
* Severity: Medium. It blocks the complete local publication gate and its SQL prerequisite. It is a confirmed check failure, not yet a confirmed application defect or attributed root cause.
* Branch: fix/case-history-browser-readiness-1248 (worktree issue-1248-browser-readiness), base main 0f420dc9514db22081cb48fa733267d9d33a0d24, eventual PR target main.
* Tier: FOCUSED tooling/test unless the proven repair expands into a FULL category; reassess before implementation.
* Refs #86 and #81. Eventual `Closes #1248` only if every literal criterion below is proven; otherwise `Refs #1248` naming the unmet criteria.

## Failure Summary

* The #86 FULL r4 run (candidate 3445238e43b484a7e550aca3cbbe91c3e9f9be90, parent 7d390e13a450a5ca096501b1a2ccefcd9a517fd4, main 0f420dc9514db22081cb48fa733267d9d33a0d24) failed at `src/api/checks/case_journey_browser_check.py:750` with `AssertionError: saved call reaches actual history`.
* Failed receipt SHA-256: 7c96fb63ead9ab52c197fb5a468709fe761e2b778598ff8680dc97d07fb46091. Durable status: https://github.com/jmservera/ama/issues/86#issuecomment-6706035214.
* Preserved evidence: /mnt/ama-gates/g86-r4-1107/0102-browser.log (immutable) and /tmp/rpi-86-browser-diagnosis-1107.log.

## Acceptance Criteria (verbatim, unticked)

* [ ] Preserve R4's negative evidence and record a correlated synthetic reproduction or a clearly bounded insufficient/not-reproduced outcome.
* [ ] Prove the cause and correct save/history completion signal before implementing a fix; distinguish application behaviour from checker readiness.
* [ ] A focused regression with controlled delayed case refresh fails under the old readiness condition and proves the exact saved History content under the repair, without weakening other draft/persistence checks.
* [ ] The existing full case-journey browser check passes, retaining all strict history, unrelated-draft, keyboard and axe checks; no retry/sleep/skip workaround.
* [ ] Research, prospective plan/details/critique, implementation, changes and Review are committed with current focused browser/unit/static evidence and independent exact-head assessment.

## Planning Comments

* Criterion 5 includes independent exact-head assessment, which a local candidate cannot prove. Expect `Refs #1248` until it exists.
* No SQL, Azure, model call, private data, production authentication, human approval, consent or policy change is in scope.
