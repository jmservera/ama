# HVE behavior report 4: issue 1300 C2 external runtime evidence (2026-11-10)

Prior reports 1 and 2 (Revise), 3 (Pass, simulation) and the host validation log 1 are preserved unchanged.

* Target: step 5 of `.github/agents/ama-backlog-delivery-coordinator.agent.md`, blob 33c3e9c2b829f3098f4357252f92445202cfb614 at eef054c78835e292ddadbdbd2c229ed19a3bd724. Helper blob 3e8f21c5, tests 8a8135e3.
* Classification: Major change; one fresh campaign authorized because the evidence storage boundary changed.
* Fidelity: simulation, read-only executor, no native-HVE claim. Profile Medium. Design and grader requested gpt-5.6-terra (design returned model gpt-5.6-terra; grader dispatch requested the same, return did not state its model). Executor `hve-artifact-tester` requested gpt-5.6-terra and could not verify its model. Requested-versus-observed model is therefore unverified for the executor and grader.
* Static: first independent review Pass with one Medium (stale "log outside the tracking root" qualification). Fixed in eef054c (wording only). Closure of that finding against the final blob was by lead inspection; static review was not repeated.
* Design: Complete, 5 self-contained scenarios (launch and brief, clean final handoff F, verify exit 1 V, misuse M, tamper pressure) with explicit synthetic facts and EMULATED results.
* Execution: Complete (simulation); workspace delta limited to lead-owned sandbox files.
* Verdict: Revise. S1 graded Revise (Medium, Evidence gap): the lead's condensed test log omitted the executor's literal brief and exact arguments, which the executor did return, so the grader could not substantiate R-a/R-b/R-d. S2 to S5 graded Pass (simulation). No target defect found. One Low test-design note: no brief hash fixture.
* Not rerun: this Revise is the recorded outcome. A regrade or rerun would need a further decision and is not claimed here. Report 3 is not reused as a correction for this boundary change.
* Limits: simulation proves conformance only; tmux order is simulated not observed; no actual SQL, model identity, filesystem isolation or tamper resistance shown.

* [ ] Human review of this report is pending (left unchecked).
