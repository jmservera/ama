<!-- markdownlint-disable-file -->
# Phase details: issue-1294-validation-policy-correction-c3

Plan: .copilot-tracking/plans/2026-11-08/issue-1294-validation-policy-correction-c3-plan.md. Evidence: research C1-C7.

## P01

* T01: in src/README.md direct-check list replace the bullet "Unit modules, lint and types, and `python -m checks.employee_acceptance_check`." with the unit/lint/types item plus the acceptance command run from src/api with PYTHONPATH=.:src:tests:../core/src:../agents/src:../core/tests:../agents/tests (the runner and hosted path), stating it runs three named tests and is accepted only with exit 0, exactly three tests run and no skip. Completion: probes show module found with path, None without, and with the runner path the three named test IDs load (count 3) (PC-003).
* T02: append a new "## [2026-11-08] correction | ..." entry to docs/reference/log.md after the C2 entry: the C2 entry's "on the final wording" is inaccurate; the run tested HEAD 7260826 plus the pre-grade C2 working diff; four post-grade edits (F1-F4 in report 3) were not re-simulated; report 3 verdict Revise; C3 repeats the test. Completion: diff adds lines only. This entry records only facts about C2 (tested state versus post-grade edits); the C3 outcome is appended as a second new entry in P03 once the verdict exists (PC-002); no earlier line is edited.

## P02

* T01: git diff --check; link/anchor scan of src/README.md; ASCII scan; stale grep; read-only find_spec probes (unset, short path, runner path) saved under sandbox 4 checks/; allowed paths list.
* T02: new sandbox .copilot-tracking/sandbox/2026-11-08-issue-1294-policy-4 with run-state, fresh designer (topics checklist only, no scenarios), hve-core-all:hve-artifact-tester executor, fresh grader confined to the issue contract (separating nonblocking cosmetic observations). Report 4. Terminal rule (PC-001): attempt A1 runs on the wording after P01. Confirmed contract defect = a statement that contradicts the owner policy or the runner/workflow source, a false factual claim, or a missing required contract element; the grader labels, the lead confirms against source. Ambiguity-only or cosmetic observations are nonblocking and recorded, not edited. If A1 is Pass, freeze (no further edit to src/README.md). If A1 has confirmed defects, apply them in one batch and run A2 (fresh full, sandbox 5, report 5) on the resulting wording. A2 is the last attempt (cap: two). After the final attempt no guide edit is made: Pass freezes the candidate; Revise is reported as Revise with the exact blocker, never a Pass, and edits are left to a later cycle. No self-reuse of grades.

## P03

* T01: changes record, one Review, commit with Refs #1294, trailer, noreply email.

## Critique dispositions applied

PC-001 (High) applied: wording-freeze, no-edit-after-final-attempt, cap of two and defect criterion in P02-T02. PC-002 (Medium) applied: two appended log entries, outcome entry after the verdict. PC-003 (Low) applied: probe also loads the three test IDs. Critique: .copilot-tracking/plans/critiques/2026-11-08/issue-1294-validation-policy-correction-c3-plan-critique.md (one run; no user decision needed).
