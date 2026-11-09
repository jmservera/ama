<!-- markdownlint-disable-file -->
# Research: issue 1294 validation policy, correction C3

## Brief

* Topic: bounded correction C3 (one of four owner-authorized cycles) for #1294 at HEAD bd63b22c0b5405ae00f7cbe4d511db30446ab556 (tree e2e237d18922d13addd15df735bdff69b22713da), base fa7ae0c9770e890f82482456bfcb8e97f1e05429.
* Questions: Q1 direct employee_acceptance_check command lacks PYTHONPATH and three-test contract; Q2 log C2 entry overstates tested revision; Q3 complete the behavior loop on the actual candidate wording.
* Posture: focused (named files, supplied failure evidence); inline waves, no delegation needed; no interaction needed. Output mode: convergence.
* Scope limits: guide/log wording only; no workflow, source, tool, install, Docker, SQL, Azure or deletion; no filesystem-root search. Python runs read-only with PYTHONDONTWRITEBYTECODE=1.
* Source review: /home/azureuser/.copilot/session-state/f751a4dc-045d-479c-8035-8588858e3b08/files/review-1294-bd63-independent.md (findings 1-3).
* Extensions: repository instructions (.github/copilot-instructions.md) selected; skills hve-builder-tester (behavior stage) selected; no specialist subagents.

## Wave 1 wider
Inline (no worker). Evidence IDs:
* C1 src/README.md:189 lists `python -m checks.employee_acceptance_check` with no path; src/README.md:430-436 already documents the runner path and three-test, zero-skip contract.
* C2 tools/rpi-checks.py:131-133 EMPLOYEE_ACCEPTANCE_BROWSER_PATHS = ".:src:tests:../core/src:../agents/src:../core/tests:../agents/tests"; used at :1133-1135 and :2332-2334; expected_count 3 at :1408 and :1876.
* C3 src/api/checks/employee_acceptance_check.py:498-510 loads three named tests from `test_employee_acceptance_check`, exits non-zero unless successful, testsRun == 3 and no skips.
* C4 .github/workflows/src-ci.yml:102-107 runs the command with PYTHONPATH=.:src:tests:../core/src:../agents/src:../core/tests:../agents/tests.
* C5 Probe (read-only, exits 0, from src/api): find_spec('test_employee_acceptance_check') is None with PYTHONPATH unset; resolves to src/api/tests with `tests:../core/tests:../agents/tests`; resolves with the full runner path. The runner path is the reference; no browser was run.
* C6 docs/reference/log.md:10948-10950 C2 entry says "repeated as a fresh full run on the final wording"; behavior report 3 records four post-grade edits not re-simulated (verdict Revise; tested state = HEAD 7260826 plus the pre-grade C2 diff, patch in sandbox 3 target-diff-vs-7260826.patch). Final committed wording differs by post-grade-final-diff-readme.patch.
* C7 Report 3 is Revise, so HVE tester correction-reuse preconditions (prior Pass, no open finding) do not hold; a full run is required after the source fixes.

## Wave 2 deeper

The runner path (C2) is the reference. Using the full runner path in the guide matches CI (C4) and the guide's own line 431; the shorter `tests:...` path suffices for discovery (C5) but would diverge from the runner, so use the runner path. The log fix must be a new appended entry, not a rewrite (repo rule); it identifies the tested state (C6) and the actual result (Revise, nine Pass and three Revise, four post-grade edits untested).

## Wave 3 contrarian

* Alternative: use the shorter `tests:...` path (works, C5). Rejected: it differs from the runner and CI.
* Alternative: edit the earlier log entry. Rejected: append-only.
* Alternative: skip a new behavior run because edits are small. Rejected: report 3 is Revise; owner and HVE rules require a fresh full run on the actual candidate; honest cap of bounded attempts with Deferred/Revise if no genuine pass.
* Risk: another Revise from cosmetic observations. Mitigation: grader confined to the issue contract and must label cosmetic items nonblocking; at most two further full attempts after this correction batch (bounded), else report blocker.

## Synthesis and decisions

* Accepted: add the runner PYTHONPATH and three-test zero-skip contract to the direct acceptance command; append C3 log correction; fresh full behavior run(s) on the committed-state wording with proxy label and retain-sandbox.
* Research disposition: executed. Planning Readiness: Ready. No re-entry needed.
* Unresolved: host cannot bind subagent models (proxy).

## Next Steps

Plan phase (parent-owned).
