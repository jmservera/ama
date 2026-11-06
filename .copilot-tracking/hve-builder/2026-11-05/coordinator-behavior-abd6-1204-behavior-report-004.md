<!-- markdownlint-disable-file -->
# Behavior report 004: coordinator agent at blob acefb44a (issue 1204)

* Target: .github/agents/ama-backlog-delivery-coordinator.agent.md, blob acefb44a4d254ede6d86413343127b763dec42cb (unchanged), commit abd6b3f5f; evidence HEAD at run 6a83e42235e489de228fcc285ec543248b430363.
* Run type: full and fresh. Report 003 (Revise) and the 11cfb run were not reused. They remain unchanged, with their original findings.
* Fidelity: native activation of the registered agent in isolated opaque-named cwds, read-only tools, no built-in MCPs, text-only; shell, merge, cleanup and Graph actions emulated text. Procedural identity: per-run `strace -P` shows the intended copy's own agent path opened once; this is loading evidence only, not tool workflow or native-host acceptance.
* Profile: requested `--model auto` (owner-approved Automatic profile). Actual selected: GPT-6.1 Sol in most runs and GPT-6 Luna for F-12 and F-14 (share transcripts; the run-index model column is truncated to 'GPT-6' for 20 runs, a recorded Low defect in a generated file). autoTier unknown. No canonical High, Medium or Low label applied. Design and grading by harness-default generic subagents; canonical-profile resolution unresolved and disclosed.
* Execution status: Complete (22 native runs, all exit 0: 18 real-source, 4 mutant controls; the controls batch started first, M1/M2 pairs at concurrency 4, then the F-P2b and F-09 pairs, then the remaining real runs).
* Verdict (independent grader, content only): real-source Pass with stated limits; control discrimination Pass (P1, P2, P3 directions as frozen before execution).
* Findings: B4 Low, F-P2b frozen expectation too narrow (output hedged, consistent with the contract). B5 Low, F-08 weak blind test. B6 Low, F-12 does not state non-applicability in words. B7 Medium-limit, R3 expiry and R8 proof-supplied are partial. Earlier B1 (negative control did not discriminate) is addressed for P1 to P3 by coherent mutants; the old 001 controls remain adverse historical evidence.
* Limits: one run per scenario, router-chosen models, text-only, single grader, schedules/rebase/tmux/approval expiry untested; live schedules not read; raw outputs in external scratch (/tmp/h1204-r3/run), pending durable promotion.
* Evidence: .copilot-tracking/sandbox/2026-11-05-coordinator-behavior-002/ (run-state, test-design, test-log, run-index, test-review, mutants/, new-run-raw-manifest.md, raw-storage-manifest.md).
* Not claimed: whole HVE Pass, issue Pass, native-host acceptance, publication readiness.

- [ ] Human reviewer has accepted or rejected this report.
