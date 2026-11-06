---
title: Details, open-PR admission threshold correction r6 (issue 1204)
ms.date: 2026-11-06
---

## P3 Target edit

* Replace the sentence in the admission bullet (lines 116-120) with: admit new issues at 20 or fewer open PRs unless a drain is in progress; above 20 open PRs admit no new issues and enter a drain recorded in the session ledger; while a drain is in progress admit none, even at 16 to 20, and repair, review and merge existing PRs one at a time (rebasing only under step 8) until 10 to 15 remain, then clear the drain and resume admission. Drain state: initialise on the first confirmed count above 20; persist it in the session ledger across ticks; read it before every admission; if the state or a confirmed count is unavailable, treat the run as draining and admit nothing; clear it when a confirmed count is 15 or fewer (including a jump below 10). Keep the following sentences (continuations permitted, idle slots defect) and the eight-assignment cap.
* No other edit; frontmatter untouched. Admission never relaxes validation, publication, dependency, review or human gates.

## P4 Static review

* Independent generic subagent, read-only, given the diff and issue scope; findings recorded verbatim; compatible findings applied only if inside this scope.

## P5 Behavior scenarios (sandbox 010)

* Reuse nothing as a pass. New design covers the admission regression: A initial 15 PRs, B initial 16 PRs no drain, C initial 20 PRs no drain, D 21 PRs triggers drain and merges, E drain already triggered at 16-20 then resume at 15, F 8 assignments cap with 16 PRs (cap still bars), G a multi-tick drain trajectory 21 to 20 to 16 to 15 and a separate jump below 10 with no admission until 15 or fewer; H 16 PRs ready issue with unmet dependency, H admission with unvalidated candidate not published. Preserve the 11 prior scenario families by reference: they are historical (sandbox 009, report 010) and not re-run; only the admission cases are new.
* Every fixture supplies full facts, literal outcomes, arithmetic recomputed by the lead before execution. Executor prompts carry facts and requests only.
* Designer, executor and grader are independent generic/artifact-tester agents at harness defaults; record host attribution.

## Validation

* Focused tier. Checks: blob identity, JSON parse, Markdown frontmatter/ASCII/links, git diff --check on the correction with disclosed raw-trace exclusions, one native focused gate at final HEAD.

## Constraints

* No push, PR, merge, rebase, amend, cleanup, installs, heavy gate other than the one focused gate.
