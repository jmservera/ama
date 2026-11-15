---
title: Everything but the Software Coaching Session
description: Workflow tracking for the author-requested read-only statistical assessment
ms.date: 2026-11-14
---

## Session State

```yaml
schema_version: data-workstream-session-v1
project:
  name: Everything but the Software
  slug: everything-but-the-software
  created_at: "2026-11-14T14:21:52Z"
  customer_output_root: null
current:
  job: experiment
  class: episodic
  phase: null
  disclaimerShownAt: "2026-11-14T14:21:52Z"
jobs:
  catalog:
    class: continuous
    status: never
    artifact: null
    last_enriched_at: null
  model-diagram:
    class: episodic
    status: never
    invocations: []
  problem-framing:
    class: episodic
    status: never
    invocations: []
  feasibility:
    class: bounded
    status: never
    phase: null
    phase_gates: {}
    artifact: null
  pipeline:
    class: episodic
    status: never
    invocations: []
  analysis:
    class: episodic
    status: never
    invocations: []
  evaluation:
    class: episodic
    status: never
    invocations: []
  experiment:
    class: episodic
    status: complete
    invocations:
      - id: experiment-assessment-2026-11-14-01
        started_at: "2026-11-14T14:21:52Z"
        completed_at: "2026-11-14T14:38:31Z"
        status: complete
        artifact: conversation-assessment
        summary: Read-only statistical assessment completed without scientific approval
  testing:
    class: episodic
    status: never
    invocations: []
  observability:
    class: episodic
    status: never
    invocations: []
job_log:
  - at: "2026-11-14T14:21:52Z"
    event: selection
    job: experiment
    class: episodic
    confirmation: Explicit caller selection in the retry request
    owner: experiment-design
  - at: "2026-11-14T14:38:31Z"
    event: completion
    job: experiment
    class: episodic
    disposition: completed
    artifact: conversation-assessment
    scientific_approval: not established
session_log:
  - at: "2026-11-14T14:21:52Z"
    event: reconstruction
    confirmation: Caller confirmed project identity, job and the sole tracking path
    basis: Named manuscript and public experiment records identify the existing project
    uncertainty: No prior Coach state or scientific approval is inferred
    prior_state: absent
artifacts:
  - id: manuscript
    path: docs/capstone/thought-leadership/everything-but-the-software/main.tex
    role: existing read-only evidence
  - id: experiment-protocol
    path: docs/capstone/thought-leadership/everything-but-the-software/anc/experiment-protocol.tex
    role: existing read-only evidence
  - id: paper-history
    paths:
      - docs/capstone/thought-leadership/everything-but-the-software/README.md
      - docs/capstone/thought-leadership/everything-but-the-software/anc/revision-report.md
    role: existing read-only history
  - id: public-experiment
    repository: /home/jmservera/source/ama-thought-mve
    commit: bd75c1c2104d001d62f9fb2bb4feab438b86f763
    paths:
      - results/pilot-estimation-judging/extracted-contrasts.json
      - results/pilot-estimation/provenance.json
    role: caller-confirmed committed public evidence
  - id: conversation-assessment
    delivery: Current conversation
    role: Completed episodic assessment evidence
    durable_customer_write: false
cross_agent_refs: []
authorization:
  sole_write_path: /home/jmservera/source/ama/.copilot-tracking/ds/everything-but-the-software/session-state.md
  deliverable: Assessment in the conversation only
  exclusions:
    - All manuscript, bibliography, figures and experiment inputs remain read-only
    - No raw evidence vault, private datasets, credentials or unrelated code access
    - No VM, paid calls, reruns, allocation or registration changes
    - No commit, push or publication
assessment:
  status: completed
  question: Whether scheduling, execution-epoch and outcome linkage supports accepted inference
  frozen_analysis: preserved
  sensitivity_work: Proposed only, post-collection and approval-dependent
  scientific_approval: not established
  completed_at: "2026-11-14T14:38:31Z"
  disposition: Inference TODO remains open for dependence justification and actual amendment timing
  manuscript_locator: docs/capstone/thought-leadership/everything-but-the-software/anc/experiment-protocol.tex#L511
  source_locators:
    schedule: a9d76bb6dbb118c43315fb2a13b7bcdb732d946d:harness/study.py:271
    dispatch: a9d76bb6dbb118c43315fb2a13b7bcdb732d946d:harness/study.py:2091
    bootstrap: bd75c1c2104d001d62f9fb2bb4feab438b86f763:harness/analyze.py:285
    whole_frame_gate: bd75c1c2104d001d62f9fb2bb4feab438b86f763:harness/pilot_analysis.py:401
    primary_eligibility: bd75c1c2104d001d62f9fb2bb4feab438b86f763:harness/pilot_analysis.py:485
    retained_attempt_start: a9d76bb6dbb118c43315fb2a13b7bcdb732d946d:harness/study.py:1847
    public_attempt_projection: bd75c1c2104d001d62f9fb2bb4feab438b86f763:harness/study_report.py:465
    judging_summary: bd75c1c2104d001d62f9fb2bb4feab438b86f763:judging/judge.py:855
  checks:
    - Companion clean at the supplied exact commit; existing staged paper edits untouched
    - State data-mode scan, content hash and YAML registry/lifecycle checks
    - Seed-2027 schedule order reproduced in memory for all 315 allocated runs
    - 63 complete five-arm model/replicate groups and 5357 unique attempt joins verified
    - 630 unique judging endpoint joins agree with public run model and arm identities
    - Schedule-function AST identical across all fourteen execution source epochs
    - 77 trajectories span epochs; B-D and B-A counterparts differ in epoch sets in 17 and 19 of 63 groups
    - Published independent bootstrap B-D 1.1874 [0.1000, 2.2247] and B-A 1.4123 [0.3250, 2.4497] reproduced to four decimals
    - Independent variance coefficient 2/63 and conditional normal planning minima 12, 21, 33 and 131 checked with stdlib
    - Observed-only pooled SD 3.1119 with 298 degrees of freedom; not a power or independence claim
    - Primary availability remains false; 313 completed unassisted and two incomplete unknown trajectories retained
    - Strict complete-scenario judging contrasts available for 8 of 32; observed-scenario estimands remain distinct
  linkage_limit: Public identifiers join blocks, source epochs and reported outcomes, but actual attempt overlap and independent errors are not established
  historical_acceptance_limit: The 30 October owner decision applies to older source 90e393e, not blanket acceptance of later five-arm inference
  remaining_inputs:
    - Actual dated source-bound dependence decision and amendment timing, without backdating registration
    - Researcher-only redacted export of retained attempt start times, durations, boot or launch labels and source/runtime bindings if required
    - Unrounded judging means and missingness masks only for separately authorized exact reproduction or sensitivity work
  private_mapping_required_for_current_joins: false
  new_sensitivity_analysis_performed: false
  cross_cutting:
    privacy: Sanitized public evidence only; no private data or new customer artifact persisted
    responsible_ai: rai-standards framing retained; AI API ratings are not human usability or independent scientific approval
    rai_planner: No standalone scoped assessment selected
    telemetry: Missing attempt-level temporal joins identified; no instrumentation or telemetry collection changed
  unperformed:
    - SymPy execution, because no installed runtime was available; its skill was loaded and exact arithmetic used stdlib
    - Raw-vault inspection, candidate or judge reruns, paid calls and new sensitivity inference
    - Independent human scientific review, OSF verification, publication checks and publication
  next_action: Caller choice required; no next job or export automatically started
write_scan:
  owner: adr-author
  mode: data
  input: Exact proposed content via stdin, bound to the sole authorized path
  last_checked_at: "2026-11-14T14:38:31Z"
  status: completed
  high: 0
  warn: 0
```
