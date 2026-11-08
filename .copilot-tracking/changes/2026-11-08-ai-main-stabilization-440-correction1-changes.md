---
title: AI and employee chat main stabilization 440 correction1 changes
ms.date: 2026-11-08
---

## Changes (docs only, on candidate c96a3231)

* `docs/architecture/cutover-evidence-pack.md`: in-place qualifications in the c96a section (Excluded row scoped to the 608c pin, #1275 AWF bullet, "this main" scope, assistants and proposal rows, F1 status, excluded-from-main line, classification and resume wording), each keeping the superseded wording as dated history, plus one appended subsection "Correction 1 and currency" with a superseded-statement table, current identities, source-equivalence proof and remaining gates. 49 lines changed (about 40 added).
* `docs/reference/README.md`: one added index paragraph (8 lines).
* `docs/reference/log.md`: one appended dated entry; earlier entries unchanged.
* New records: correction1 research, plan, details, critique, changes, review and state. Original c96a records unchanged.
* Not changed: application, tools, tests, workflows, agents, BRD, PRD, ADR, issues, boards, remotes.

## Mapping to findings

* F1 (AWF): recovery vs remediation, dated and source-qualified (run `42472167065`, head `4db31928`, 2026-11-08T10:38Z).
* F2 (currency): main `3c57a02d` / `3ed3dec0`; #1278 `e73d4210` / `feff48a4`; #1243 `6ef6dc36` / `0006f193` on the parent branch; PR 1240 open at `6ef6dc36`; exclusions scoped to 608c.
* F3 (reading): amended in new research only; honest ranges, including unread addendum ranges.
* F4 (review row): action-specific enforced checks; no general requester separation.
* F5 (F1): unowned, unfiled, pending triage, not a deferral.

## Actual commands and results (2026-11-08T11:48Z to 11:56Z)

* `git fetch origin main` (three times, last 11:56:15Z): `3c57a02d`, unchanged in the last two; `git diff --name-only 608c98e6 origin/main` = 11 files, none in audited modules or selected tests (0 for those paths).
* `sha256sum` of installed venv modules against `git show origin/main:` and `608c98e63:` for seven modules: all equal.
* `gh pr view` for 1278, 1243, 1275, 1271, 1273, 1240 and `gh issue view 1274`: states as recorded.
* `git diff --check`: exit 0. Added lines: no non-ASCII, no em dash, no spaced double hyphen. Both pack anchors resolve.
* No test suite, Docker, SQL, browser, `tools/rpi-checks.py`, real provider or Azure action was run. Original 124/46/217, 59 skips, 328 non-skipped, exits 0 are unchanged historical results, SQLite and fixtures only.

## Divergences

* The first draft of the research recorded addendum range 1-240; corrected to 1-207 and 241-448 after noticing the viewer truncated 208-240. Recorded in the research file.
