---
title: Ranking current-main stabilization checkpoint 440 plan critique
description: Independent read-only critique of the issue 440 ranking current-main stabilization plan and details
ms.date: 2026-11-08
---

## Inputs and boundary

* Plan: .copilot-tracking/plans/2026-11-08-ranking-main-stabilization-440-plan.md
* Details: .copilot-tracking/details/2026-11-08-ranking-main-stabilization-440-details.md
* Research: .copilot-tracking/research/2026-11-08-ranking-main-stabilization-440-research.md
* Repository reads only (test file and class names, tools/rpi-checks.py base and ignored-input rules, pack tail heading, disk figure). No test, install, network or git write was run.
* Criterion boundary: requirements, selectors, evidence honesty, approval claims, resource risk, commit and gate ordering, and the caller's named obligations.

Critique execution: Complete. Verdict: Revise.

## Verified as sound

* Core files test_ranking_publication.py and test_ranking_publication_runner.py exist and every planned class (PublicationTests, ConcurrentWriterTests, SignoffTests, PublishTests through AssessmentCycle1Tests) is present, so the core pattern test_ranking_publication*.py is real.
* API files test_ranking_policy.py, test_ranking_publication_wiring.py and test_ranking_scale.py exist; agents test_cohort_ranking_eval.py exists.
* The pack ends at the 2026-11-07 parent 73 section (line 2961), so an append is valid. tools/rpi-checks.py requires the base to equal current origin/main (line 226) and allows only partial receipts to survive a move (line 2834).
* Evidence classification is honest: the receipt is labelled historical and source-qualified at ac0f29f9, not fresh at a80acada. No closure or approval is claimed.
* /mnt shows 5.5 GB free, matching research; the 2 GB stop floor is reasonable.

## Findings

### PC-001 (High) Non-editable pip install can dirty the checkout and invalidate the gate

* Related: plan 1.1, 4.3; details Phase 1.
* Evidence: tools/rpi-checks.py lines 220 to 223 refuse any untracked or ignored input ("move all scratch outside the checkout"). `pip install src/core src/agents src/api` builds in tree by default and can leave build/ and *.egg-info directories under src/<project>. The plan only guards scratch for pip cache and TMPDIR.
* Impact: the focused gate would refuse, or the ignored-inclusive status check in 4.1 would fail, after the tests ran.
* Fix (planner, direct): install from a copy or use a scratch build (for example `pip wheel --no-deps -w $S/wheels` with a scratch tmp, or `--no-build-isolation` is not enough); alternatively run the three installs from a `git archive` export under $S. Add a post-install check that `git status --short --ignored` is empty before 4.3, and record that result.

### PC-002 (High) Missing explicit retention of the socket-path preflight refusal and prior R35 and adverse records

* Related: caller requirement; plan 3.1 and 5.
* Evidence: grep of plan, details and research finds no mention of the socket-path preflight refusal, R35 or the adverse records. Plan 3.1 lists pack contents without them.
* Impact: the appended section may omit or soften an earlier refusal, or imply the sequence is clean.
* Fix (planner, direct): add to 3.1 and the stop conditions: carry the original socket-path preflight refusal verbatim in outcome (reported as a refusal, not retried into a pass), and cite the prior R35 and adverse records by path as retained, unedited history. Name the paths in details Phase 3.

### PC-003 (Medium) Failed gh pr diff and coordinator-reported facts need explicit non-claim wording

* Related: research coordinator files; plan 2.5, 3.1.
* Evidence: the research reads PR 1239 facts as coordinator reports, but neither plan nor details states that a failed `gh pr diff` must be recorded as failed, nor that no equivalent was substituted silently.
* Impact: risk of implying PR diff verification succeeded.
* Fix (planner, direct): add a rule in Phase 2 and 3: record the failed `gh pr diff` command, its exit and error as observed, state that the 308-path equivalence is a coordinator report and not re-run, and add a classification row "not observed" for PR diff.

### PC-004 (Medium) API test run can touch private or default ZF_DATA

* Related: caller requirement no private ZF_DATA read; plan 1.4; details API command.
* Evidence: the API command sets only PYTHONPATH. The default data path is ~/.zava-forward/data/zavaforward.json (repository instructions), and the plan never sets ZF_DATA.
* Impact: an unscoped run could read the owner private dataset, which is prohibited.
* Fix (planner, direct): set `ZF_DATA=$S/data/zavaforward.json` (absent or empty under scratch) and HOME under $S for all three selectors; record that no private dataset was read, and stop if any selector reads a path outside $S and the worktree.

### PC-005 (Medium) Receipt validity versus commit sequence is ambiguous

* Related: plan Commit sequence, 4.3, 5.3.
* Evidence: the gate runs on commit 2, then commit 3 adds Changes, Review, state. The plan says "the receipt is verified at the actual final head or reported as historical", but verification needs a clean tree and exact head, and --required-scope partial still fails on a later head.
* Impact: the final record could cite a receipt that the tool will refuse at the pushed head.
* Fix (planner, direct): state the decision now: the gate receipt is bound to the commit 2 head and recorded as such; the final commit contains only records. Alternatively make Changes and Review untracked-free and run the gate last at the final head, with Changes citing the receipt path and sha rather than embedding it. Record that a head that differs from the receipt is historical, and that the final push head needs its own verify run.

### PC-006 (Medium) "Refs only" and no-approval guard not stated as acceptance checks

* Related: plan 3.1, 4.1.
* Evidence: plan 3.1 says no closing keyword, but 4.1 has no check; commit message, pack text and index paragraph are not scanned.
* Impact: an accidental "Closes" or "Fixes" or an approval-sounding phrase could land.
* Fix (planner, direct): add to 4.1 a grep of added lines and the commit message for closing keywords (including negated forms) and for "approved", "accepted" or "closes" applied to 79, 1231 or 440. Also add that the Review record states execution separate from outcome and is not independent assessment (already in 5.2; keep).

### PC-007 (Low) Resource risk for the API scale test and pytest availability

* Related: plan 1.4, 4.2.
* Evidence: test_ranking_scale.py name implies larger data; the venv plus three installs consume part of the 5.5 GB. 4.2 depends on pytest in the scratch venv, which the plan does not install.
* Impact: avoidable disk pressure or an inconclusive 4.2.
* Fix (planner, direct): add a df check before and after the venv install and API run with a stop at 2 GB; use the system python3 unittest for tools/test_tracking_retention.py if pytest is absent, or record not applicable.

## Severity summary

* High: 2 (PC-001, PC-002)
* Medium: 4 (PC-003 to PC-006)
* Low: 1 (PC-007)

## Closeout

* Highest-impact finding: PC-001 (the install step can make the later gate refuse). Action owner: planning parent. Smallest next action: change the install method to an out-of-tree build and add an ignored-inclusive status check after it.
* All fixes are direct planner corrections with no significant or divergent user decision. No user response is required.

## Next Steps

* Return the Revise verdict to the planning parent, which applies PC-001 to PC-007 to the plan and details, records dispositions in the plan Critique Disposition section, and then commits the planning records. No further critique pass is requested.
