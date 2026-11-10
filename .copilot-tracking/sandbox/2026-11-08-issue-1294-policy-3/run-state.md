# Run state: issue-1294 policy behavior run 3 (C2)

* Run type: full (report 2 verdict Revise; post-grade edits not re-simulated; reuse preconditions do not hold)
* Targets (instruction/guide, behavior-bearing): src/README.md (section "Hosted CI versus local gate coverage (issue #1294)"), .github/copilot-instructions.md (validation tiers), .github/agents/ama-backlog-delivery-coordinator.agent.md (validation policy section)
* Target revision: HEAD 7260826bcc4ba8688baccf75b651780ccd0b0d11 plus uncommitted C2 edits (see target-diff-vs-7260826.patch)
* Profile: inferred Medium (semantic policy guidance); host task tool has no model parameter, so the model of every stage is not selectable: unresolved, PROXY run. No intended-profile or native claim.
* Fidelity: simulation (read-only executor); retain-sandbox requested
* Purpose: owner policy for #1294: targeted checks for small/doc changes plus applicable hosted CI, no blanket --changed; full exact-head gate and verified external full receipt for major, SQL, infra, deployment, security-sensitive and release; mixed changes take the strictest applicable tier (two focused stay focused; any full component makes it full; doubt takes full); absent/path-filtered CI is not a pass; direct employee-chat check keeps the runner contract (axe digest, ordered states, positive integer passes, PASS marker, no skips, no violations, named selector, exactly one test); coverage labels (shared vs hosted-only); direct --out has no evidenced 58-byte limit.
* Containment: executor read-only, synthetic scenarios, no workspace writes, no Docker/SQL/Azure/network; lead writes all sandbox files.
* Prior reports 1 and 2 and sandbox 2: preserved, not given to designer or graders.
* Mapping: topics checklist in the dispatch (not scenarios).
