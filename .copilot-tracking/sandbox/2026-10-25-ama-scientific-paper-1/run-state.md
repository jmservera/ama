<!-- markdownlint-disable-file -->

# Scientific Paper Agent Behavior Run 1

## Scope and Provenance

* Date: 2026-10-25.
* Caller: HVE Builder create-mode run; parent is also the hve-builder-tester lead.
* Run type: full. No prior design, grades or report is reused.
* Change classification: Major, a new behavioral agent and its loaded reference.
* Target type: agent, .github/agents/ama-scientific-paper-writer-reviewer.agent.md.
* Target SHA-256: df89db75f7aa60ea1cd59128bb64d34087b10da09fcf8f2ddd88012b06dd85cf.
* Loaded reference: docs/reference/method/scientific-paper-writing-and-review.md.
* Reference SHA-256: 6b6057a1fd948db60056d3bdc99f0286997c41e6b92d0d2d8f459d6b394b21bf.
* Isolation set: the selectable agent, including its documented reference-loading action.
* Together set: the agent and its compact method reference during writing, revision and critique.
* Behavior gate: execution required, not satisfied-and-skipped.
* Requested fidelity: simulation. Native activation and write containment are not established.
* Intended profile: Medium, inferred from semantic writing and calibrated review responsibility.
* Declared target model: omitted intentionally; the selectable agent uses the session selection.
* Model availability: host exposes no available-model list. The design invocation explicitly requested GPT-5.6 Terra (copilot), the first canonical Medium model, and was accepted. Actual runtime resolution remains unexposed; no independent model-identity or fallback-availability claim is made.
* Authoring and static review inherited the session model; their canonical tiers remain unverified.
* Static result: Pass. Original Low finding SP-SR-001 closed before behavior testing.
* Targeted closure: mechanical assertion verified every table pipe position and every original cell string; scoped whitespace check passed. Editor diagnostics for the corrected agent reported no errors.

## Purpose and Acceptance

Exercise useful scientific writing and assisted review without fabricated research,
unapproved edits or an empirical template imposed on every genre.

* R1: Write, revise and review have explicit, respected edit boundaries; report-path authority is separate.
* R2: Resolve material inputs and actual venue/policy requirements proportionately; disclose generic guidance and scope limits.
* R3: Distinguish full-text, partial/abstract-only, metadata-only, supplied-unchecked, conflicting and unavailable evidence; never invent citations or claim exhaustive checking from a sample.
* R4: Preserve methods, chronology, uncertainty and null/contradictory findings; distinguish proposed work from observed results and approvals.
* R5: Human intellectual ownership, authorship and approval remain explicit; AI/confidentiality/disclosure depend on actual policies.
* R6: Structure fits empirical, conceptual/perspective, method, review or protocol work; no invented systematic search or evaluation.
* R7: Review is fair, prioritized, located and actionable; separate scientific defects, evidence gaps, clarity and preferences.
* R8: Reviewer replies map actual comments to actual or explicitly proposed changes; no upload, submission, communication, research execution or repository/remote mutation is authorized by selecting the agent.
* R9: Assisted critique is not independent human peer review or scientific certification; configuration selection is outside this run.

## Containment and Ownership

* Executor: registered HVE Artifact Tester in read-only contained simulation.
* The lead alone creates or writes sandbox evidence; designer, executor and grader return content only.
* Fictional manuscript/evidence fixtures are inline scenario data. No real manuscript, private dataset, journal account, credential or external system is used.
* No source edit, installation, network access, research execution, staging, commit, push, branch or PR action is allowed during scenarios. Any such action is emulated and labelled, not executed.
* Use only known target, dependency, design and canonical criteria reads. Opaque user-managed tool configuration is not inspected, evaluated or selected.
* Retain this small current-run sandbox at the parent's explicit request to preserve grading evidence and avoid cleanup of repository evidence without retention review. No historical output is deleted.
* Durable report path: .copilot-tracking/hve-builder/2026-10-25/ama-scientific-paper-behavior-report-1.md.
* Design: Complete, SP-BD-001, persisted in test-design.md before execution. SP-SC-001 covers isolated review and response; SP-SC-002 covers the agent plus reference through writing, narrow revision, critique and response. The design records the full R1-R9 coverage map and intentionally untested branches.
* Changed-surface impact: all requirements and scenarios are fresh because this is a new agent; no unaffected/reused grades.

## Pre-Run Workspace Observation

Branch: jmservera/capstone-presentation-review, matching open PR 460. No branch change.

Observed modified files before sandbox creation:

* docs/capstone/thought-leadership/everything-but-the-software/README.md
* docs/capstone/thought-leadership/everything-but-the-software/main.pdf
* docs/capstone/thought-leadership/everything-but-the-software/main.tex
* docs/capstone/thought-leadership/everything-but-the-software/references.bib
* docs/reference/README.md
* docs/reference/log.md

Observed untracked paths:

* .copilot-tracking/hve-builder/2026-10-25/
* .copilot-tracking/research/2026-10-25/scientific-paper-agent-research.md
* .github/agents/ama-scientific-paper-writer-reviewer.agent.md
* docs/reference/method/scientific-paper-writing-and-review.md

The index, append-only log and named new agent/reference/evidence are this run's
approved work. The thought-leadership files changed concurrently outside the
assistant's write boundary. Their existence is not attributed to the simulator.
No paper source or PDF was written by this run.

Initial dirty PDF SHA-256 was
18a919029ed2debe5adb2e0ee86cbd36163730cbf4d09d51e253bf94419adabd;
latest pre-behavior SHA-256 is
2b74bb865d1a0deb09f1cb434b4cd318ac08fcbf7826a793feabfc9581a45d76.
The original checksum is therefore not claimed to be preserved. Post-run status
must distinguish lead-owned evidence from any further concurrent paper changes.
