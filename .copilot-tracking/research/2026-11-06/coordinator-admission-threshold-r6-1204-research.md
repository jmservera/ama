---
title: Research, open-PR admission threshold correction r6 (issue 1204)
ms.date: 2026-11-06
---

## Disposition

Research executed (bounded, known-target reads). Planning Readiness: Ready.

## Owner authority

* Coordinator reported a blocking 16-20 PR policy conflict and requested one bounded correction; the owner replied exactly "fix 1204 and merge" (2026-11-06). This supersedes the earlier no-target-edit prohibition only for this correction and its directly coupled fixtures and evidence. No gate is waived; merge is coordinator-only after gates.

## Independent adverse finding (preserved, partial coverage)

* Source: independent partial static assessment outside the checkout (review.md, metadata.json, issue-comment.md under the f751a4dc session files, issue comment 6692489250). Verdict request_changes, 1 High, assessmentComplete false: complete instruction diff inspected, not all 207 changed files. It is not a complete review Pass and does not rewrite report 010 Pass (simulation grade) or report 009 Revise.
* Finding: target lines 116-120 say "Admit new issues only at 15 or fewer open PRs; from 16 to 20 admit no new issues".

## Canonical scope evidence

* Current main (bb3a3b03) lines 187-189: "With more than 20 open PRs, take no new issues ... repair, rebase and merge existing PRs until 10 to 15 remain, then resume new work". Issue 1204 approved scope: "the 20-PR drain rule". The target at HEAD 7ae41593 (blob acefb44a) adds an unconditional 16-20 ban at lines 117-118 and is the only place with that band.
* Eight total assignments is a separate cap and stays. Existing-PR repair, correction and review continuations stay permitted at every count.

## Fixture contracts coupled to the defect

* Sandbox 009 design H-03C (16 PRs) and H-03D (20 PRs) assert admission is barred; H-03E (21 PRs, drain) and the H-06 and H-11 notes cite the 16-20 band. These oracles encode the defect. They are historical and immutable; a new sandbox 010 supplies corrected cases.

## Required correction semantics

* Initial counts 15, 16 and 20 with no drain entered: admission allowed (subject to capacity, dependencies and every validation gate).
* Count 21: trigger drain, no new issues, merge one at a time to 10-15.
* Already-triggered drain: stays in force at 16-20 until 10 to 15 remain, then admission resumes.
* Admission is not publication: unvalidated candidates are never published.

## Unknowns

* Native Automatic fidelity, live deployment of prompts, hosted CI, human review.
