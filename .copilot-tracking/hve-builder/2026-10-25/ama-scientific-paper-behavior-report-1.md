<!-- markdownlint-disable-file -->

# HVE Artifact Test Report: Scientific Paper Agent Run 1

* Tested profile: intended Medium, GPT-5.6 Terra (copilot) explicitly requested;
  dispatch accepted, resolved runtime identity/tier unverified.
* Run type: full.
* Behavior gate: Executed.
* Fidelity: simulation.
* Execution status: Complete.
* Verdict: Revise.
* Sandbox: retained at .copilot-tracking/sandbox/2026-10-25-ama-scientific-paper-1/.

## Summary

Seven simulated responses covered scoped review, mixed-result interpretation,
perspective writing, narrow revision and honest reviewer replies. Independent
grading found three coverage misses and no directly demonstrated source defect.
The original Revise outcome remains unchanged. Extend the scenario coverage
before claiming the behavior gate passed; do not rewrite the agent without
evidence of a source defect.

## Fidelity and Limitations

The registered HVE Artifact Tester read the real agent and reference and
returned literal simulated conversations. Manuscripts and evidence were inline
fictional fixtures; source acquisition, file edits and external actions were
emulated or not performed. No native activation, real policy/source checking,
file-write reliability, enforcement or scientific quality is established.
No available-model list or independent runtime-identity attestation is exposed.
The configured Medium request is not proof of actual tier or cross-profile
equivalence. A stronger simulator could repair ambiguity a lower tier exposes;
this run does not establish unambiguous behavior at lower tiers.

## Reuse Eligibility

Not applicable: full run, no prior grades reused. This report's Revise verdict
and open findings make it ineligible for the Pass-only correction-run reuse
optimization. Follow-up coverage will use a fresh full design, execution and
independent grade against the unchanged source revision.

* Design: SP-BD-001.
* SP-SC-001: R1/R3/R4/R7/R8/R9, fresh responses SP-O-001 through SP-O-003.
* SP-SC-002: R1/R2/R4/R5/R6/R7/R8/R9, fresh responses SP-O-004 through SP-O-007.
* All grades were fresh. Evidence resides in the retained sandbox's
  run-state.md, test-design.md, test-log.md and test-review.md.

## Findings

* SP-EG-001: High, miss, Evaluation hooks. Abstract-only and metadata-only
  evidence were included but not actually assessed in the response. Add
  discriminating material-claim scenarios and independent grading.
* SP-EG-002: Medium, miss, Evidence fidelity. Authorized file edits, explicit
  review-to-edit switch and supplied venue-policy behavior were not exercised.
  Add bounded simulated branch coverage.
* SP-EG-003: Medium, miss, Evaluation hooks. Non-perspective genre branches
  remain untested. Add empirical, methods/protocol and systematic-review
  boundary coverage, or narrow the claim. Parent selects added coverage.

Action counts: improvement 0, adjustment 0, deletion 0, correction 0, miss 3.
The exact independent evidence, severity, resolving action and pointers are
preserved in the retained test-review.md. No finding is marked closed here.

## Containment

Agent SHA-256 remained
df89db75f7aa60ea1cd59128bb64d34087b10da09fcf8f2ddd88012b06dd85cf;
reference SHA-256 remained
6b6057a1fd948db60056d3bdc99f0286997c41e6b92d0d2d8f459d6b394b21bf.
Executor reads were bounded to the run state, agent and reference. The lead
alone wrote sandbox evidence. Concurrent paper changes are separately recorded
in run-state.md and test-log.md and were not reverted or claimed preserved.
The trace contains no executor source or external-system mutation. Native
write enforcement and exact attribution of concurrent actors are unproven.

## Satisfied-and-Skipped

None. The new agent and loaded reference are behavior-bearing Major additions.
Index/log wiring is supporting documentation, not an independent runtime test.

## Human Review

* [ ] Reviewed and validated by a qualified human reviewer
