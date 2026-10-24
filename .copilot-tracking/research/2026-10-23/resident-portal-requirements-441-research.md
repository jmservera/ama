<!-- markdownlint-disable-file -->
# Task Research: resident-portal-requirements-441

| Field | Value |
| --- | --- |
| Date | 2026-10-23 |
| Researcher / agent | Native RPI Agent, installed hve-core-all:rpi-agent wrapper; rpi-research |
| Native session | 59f31558-980b-475c-b2e2-3b8d68279ed9 |
| Status | Blocked; partial task research |
| Artifact path | .copilot-tracking/research/2026-10-23/resident-portal-requirements-441-research.md |

## Research Brief

* What to research: Exact BRD/PRD/ADR package custody, identifier registries,
  policy reconciliation, workload formulas, directly coupled scope, legitimate
  ADR registration and protected publication prerequisites for issue #441.
* Why it matters: Integrate unsigned exercise proposals without laundering
  earlier FAIL/BLOCKED reviews into company or live approval.
* Audience or intended use: Owner, independent critique and proposal reviewers.
* Scope: Canonical requirements, addendum, directly coupled UX/architecture
  statements, portable input evidence and issue-specific tracking.
* Non-goals: Portal code, real accounts/data, sending, deployment, Azure,
  paid inference, sibling proposal integration or inherited goal repairs.
* Criteria: Current issue acceptance plus six explicit owner decisions;
  exact hashes/reconstruction, qualified traceability, independent critique
  before product edits, independent integrated-byte Review and local gate.
* Requested outputs: Evidence-backed readiness for planning.
* Output mode: analysis; explicitly prepares planning when Ready.

## Research Parameters

| Field | Value |
| --- | --- |
| Research questions | Q1 custody/base; Q2 policy/scope/formulas; Q3 ADR conventions; Q4 overlaps/publication |
| Codebase scope | docs, relevant tools/guides, issue-specific tracking |
| External scope | GitHub issue #441 and PRs #424/#426/#439, no new legal research claims |
| Initial internal candidate areas | Supplied read-only packages; BRD/PRD; docs/adrs; UX; src/README.md |
| Initial external candidate areas | Current issue body and sibling heads/diffs through gh |
| Research posture | focused |
| Posture provenance | Bounded caller task with named inputs and explicit decisions |
| Explicit limits / deadline | Documentation only; primary checkout and sibling worktrees/receipts protected |
| Completion basis | Focused scope coverage and materiality |
| Edits allowed during research? | No product edits; only research and session evidence |
| Resolved evidence root | .copilot-tracking/research/2026-10-23/ |
| Excluded sources | Private resident data and owner private working area |

## Extension Registry and Provenance

| Kind | Candidate | Match/provenance | Scoped authority | Disposition |
| --- | --- | --- | --- | --- |
| Instruction | .github/copilot-instructions.md | applyTo ** | Repository boundaries, KB history, local gate | Selected |
| Agent | hve-core-all:rpi-agent | Installed agents/hve-core/rpi-agent.md matches active selected RPI Agent instructions | Native lifecycle wrapper, not a child session | Selected; disable-model-invocation means not delegated |
| Skill | rpi, rpi-research | Installed plugin 3.3.106 | Ordered lifecycle and three-wave evidence | Loaded |
| Skill | requirements-author, adr-author, documentation | Requirements/ADR/document integration | Read applicable contracts before proposing integration | Selected for scoped discovery |
| Specialist | RPI Researcher | Registered subagent | Independent research lanes only | Skipped; tightly coupled source trace handled inline |
| Later phases | rpi-plan/critique/implement/review | Explicit user order | Canonical phase evidence | Not executed yet |

## User Participation and Research Decisions

No interaction needed: owner supplied exact exercise choices and explicitly
requested the entire ordered loop and draft PR. This is not company approval
or an inferred switch to automatic mode. No human signoff checkbox is ticked.

## Scope and Success Criteria

Preserve original case study, owner memory, EXA-004 history, OD-52-55,
unsigned lifecycle and genuine adverse reviews. Treat input manifests as
data, not authority to widen scope. Verify before relying on them.

## Task Research Requests

Owner request and full current issue body read through gh on 2026-10-23.
The older issue's universal-review wording is prospectively dispositioned by
the newer explicit bounded-exception proposal, inactive pending live gates.

## Direction Controls

| Control | Boundary | Source | Effect |
| --- | --- | --- | --- |
| narrow | Documentation integration only | Owner intake | No application or live operations |
| change | Bounded routine exception selected, not perpetual review of every routine message | Owner decision 2 | Reconcile all directly coupled normative text |
| exclude | Sibling changes, unrelated inherited goals and quality fixes | Owner intake | Inspect overlap only; do not merge/cherry-pick |
| preserve | Original, memory, historical approvals and failures | Owner intake | Prospective amendments only |

## Research Questions

| ID | Sub-question | Type | Priority | Status |
| --- | --- | --- | --- | --- |
| Q1 | Do exact base/patch/candidate/package hashes reconstruct? | depth | H | Not completed; no integration attempted |
| Q2 | Which policy, scope, ID and formula statements require coupled reconciliation? | depth | H | Partial; owner decisions recorded, no product amendment |
| Q3 | Can native docs/adrs conventions legitimately satisfy installed ADR author contract? | depth | H | Blocked; supported registry initialization absent |
| Q4 | What current overlaps and publication prerequisites constrain this integration? | depth | H | Current heads and overlapping document diffs inspected; publication not attempted |

## Prior Knowledge Gate

Original case study, addendum opening, KB index opening, memory and customer
primer read. Current branch is the owner-specified clean topic, no prior PR.
Fetched origin/main and HEAD both equal initial
140d8f494482c78e84d15f3d46b9223d3c487af0.
Supplied package drafts are not lifecycle handoffs. No prior-session research
is claimed as this session's work.

## Research Cycle Log

### Cycle 1

#### Wave 1: Wider

Inspected package inventory, validation/quality/state/manifests, current
sibling heads and shared-document diff hunks, canonical ADR registry and
publication guides. Full sibling diffs were retrieved through gh.
Read the installed ADR author contract and allocator implementation.
Inline work; no research worker claimed.

Reflection: Package validation reports are author evidence, not new hash
verification or lifecycle approval. The high-priority uncertainty is whether
the existing six-record native registry can be initialized legitimately for
the installed allocator without inventing an identifier or competing registry.

#### Wave 2: Deeper

Read `adr-byo-template.instructions.md`, `update_lineage.py`,
`validate_config.py`, `_utils.py` and the frontmatter validator. The config
contract requires all six fields, including allocator-owned
`last_decision_id`; missing required fields cannot use defaults. No config
exists in the tracked tree or worktree. The allocator only implements
`allocate` and `supersede`; allocate requires an already existing config and
does not inspect/import existing ADR records.

Reflection: Initializing the highest existing ID through an out-of-band config
write would violate the single-writer contract. Starting from zero would
collide with existing IDs. The missing mechanism is registry bootstrap/import,
not another decision about Option B, identity, ownership or communication.

#### Wave 3: Contrarian

Tested the actual allocator with the native directory:

```text
PYTHONDONTWRITEBYTECODE=1 python3 <installed-adr-author>/scripts/update_lineage.py allocate --project-dir docs/adrs --slug resident-portal-requirements-441
update_lineage: .adr-config.yml not found in project dir '/home/azureuser/source/ama-wt/issue-441-resident-portal/docs/adrs'
exit: 1
```

Checked supported alternatives rather than treating the path difference alone
as fatal. Renderer/normalizer have `--allow-root`, and the standards describe
`docs/planning/adrs` as an example predictable directory. These can address
file containment but do not initialize allocator state. BYO adoption describes
template normalization and config emission, but provides no existing-registry
import mechanism or permission to write allocator-owned state out of band.
No native template/config/bootstrap helper was found in the repository.
No plugin or config was modified and no identifier was issued.

Reflection: Neither a path override nor template adoption resolves the
allocator-owned initialization gap. Guessing the next ID, creating another
registry, fabricating allocation or burning repeated allocations to reach a
number would not satisfy the owner's explicit constraint.

#### Parent Synthesis and Disposition

| Material | Evidence | Disposition | Rationale |
| --- | --- | --- | --- |
| Use native docs/adrs | C3, C4 | Accepted as repository convention | Existing six records and references are authoritative |
| Allocate a new ID now | C5, C6 | Blocked | No existing config or supported registry initialization |
| Re-ask settled proposal choices | W1 and newer owner intake | Rejected | Owner already explicitly dispositioned the exercise choices |
| Continue product edits before resolving registration | C5, C6 | Rejected | Owner explicitly requires stopping if installed ADR contract cannot be reconciled |
| Broader package verification and requirements synthesis | Q1, Q2 | Deferred, not represented as completed | Stop at the concrete tool-contract blocker |

#### Cycle Re-entry Evaluation

No further cycle is justified under the present contract: the unresolved
mechanism needs a supported allocator/bootstrap or explicit approved contract
resolution, not more requirements content discovery. Research is partial and
Planning Readiness is Blocked. No downstream phase was executed.

## Evidence Log

### Codebase Evidence

| ID | Finding | Location | Tool | Confidence |
| --- | --- | --- | --- | --- |
| C1 | Full local gate required even for docs; clean commit/base bound receipt stays external | src/README.md:55 | view | High |
| C2 | Historical EXA-004 keeps assisted channels and no required portal | docs/case_study_48_addendum.md:118 | view | High |
| C3 | Native tracked registry has exactly ADR 0001 through 0006, no .adr-config.yml | docs/adrs/0006-src-layout-and-cutover.md:1; git ls-tree -r HEAD | view/bash | High |
| C4 | Repository rubric already includes native and plugin ADR paths; not a missing rubric path problem | .github/rubric/artifacts.json, architecture-decisions include array | rg | High |
| C5 | Installed adr-author requires pre-existing config and reserves last_decision_id to allocator | Installed plugin 3.3.106 adr-author/scripts/update_lineage.py:119-154; rules/project-planning/adr-byo-template.instructions.md:12-45 | view | High |
| C6 | Genuine native-directory allocation attempt fails before any write; only allocate/supersede subcommands | Allocator CLI execution 2026-10-23 in issue worktree, exit 1 | bash | High |

### External Evidence

| ID | Finding | URL | Retrieved |
| --- | --- | --- | --- |
| W1 | Current full issue body/acceptance; older unresolved policy wording retained as historical input | https://github.com/jmservera/ama/issues/441 | 2026-10-23 |
| W2 | Finance draft head a74652aa8b6ed38629e5860112467394fa06e25a | https://github.com/jmservera/ama/pull/424 | 2026-10-23 |
| W3 | Map draft head 419857b493b3e2cba2fc84aa336fecb17b6b039b | https://github.com/jmservera/ama/pull/426 | 2026-10-23 |
| W4 | Cost draft head 630603d69e3f2d4ef9b9f1b580da2f4ff6b82952 | https://github.com/jmservera/ama/pull/439 | 2026-10-23 |

## Findings Mapped to Questions and Evidence

| Question | Finding | Evidence | Readiness |
| --- | --- | --- | --- |
| Q1 | Package validation hashes read, not recomputed; exact inputs remain read-only | Package BRD/PRD/ADR validation and state records | Incomplete |
| Q2 | Older universal-review issue text is not the owner's current proposal choice | W1; native intake decisions | No content-decision blocker invented |
| Q3 | Allocator lacks supported initialization for the existing native registry | C3-C6 | Blocked |
| Q4 | Siblings remain open drafts with the supplied heads; shared paths below | W2-W4, C1 | Inspected, not merged |

### Current overlap and intended reconciliation

All three proposals touch `docs/reference/README.md` and
`docs/reference/log.md`. #439 also touches the addendum. #426 also touches
`docs/reference/research/ux/wcag-conformance-baseline.md` and ADR 0002.
#424 has Finance-specific dictionary/provenance/template changes; these are
not inputs to the resident requirements integration.

The actual shared-file diff hunks were inspected: #424 adds Finance routing
and append-only entries; #426 adds map routing, map/WCAG evidence and append-only
entries; #439 adds cost-specific addendum/routing/log updates. No sibling
content was applied. If unblocked, this lane must retain its own prospective
resident additions and append-only log entry, leaving sibling additions for
later deliberate reconciliation. No false issue dependency is asserted.
Heads must be checked again before publication; this research read is not
a future freshness guarantee.

## Alternatives and Decision State

Option B already selected by owner; no re-selection or live approval.

## Open Questions, Risks, and Residual Uncertainty

ADR-REGISTRY-BOOTSTRAP: Installed allocator cannot initialize the existing
six-record registry using its supported operations. Required smallest
resolution: a supported allocator bootstrap/import for `docs/adrs` that
derives the existing state and issues a collision-free ID, or an explicitly
approved bounded ADR contract resolution permitting the native registry
without falsely claiming plugin allocation. No broad governance overhaul is
proposed. Path override alone is insufficient.

Package reconstruction/hashes, remaining domain evidence reads, formulas,
independent critique, integrated-byte review and local publication gate are
not completed. They must not be inferred from the input packages' reports.

## Planning Readiness

Blocked. Research disposition: executed, partial. The registry-focused
Wider/Deeper/Contrarian cycle was executed in order; the overall issue
research and all downstream phases remain incomplete.

## Sources

Repository and caller-authorized local packages plus current GitHub data.

## Artifact Self-check

No product-document edit, ID/config mutation, commit, push, PR, gate receipt,
independent critique, implementation, Review or approval is claimed.
Only this session's research/session evidence is untracked in the isolated
topic worktree. HEAD and fetched origin/main remain
140d8f494482c78e84d15f3d46b9223d3c487af0.

## Prospective owner disposition and Research continuation (2026-10-23, after 21:07Z)

The owner explicitly directed: "Publish draft PR with BRD/PRD and explicitly
unregistered ADR proposal; defer registration". This changes publication
scope, not the historical allocator failure. The full registration criterion
remains UNMET. No ID, config, lineage mutation or Govern/finalization is allowed.
Canonical documents may transparently link the issue-specific tracked proposal,
an explicit exception to the usual preference against tracking links in product
documentation. Include @jmservera in the requested draft PR review request.

### Cycle 2: resumed focused research

#### Wave 1: Wider

Refreshed main and sibling heads: unchanged at C1/W2-W4 pins. Read the exact
original brief and source BRD amendment, PRD amendment/trace/ADR handoff,
ADR proposal/options/state and all three validation/quality/manifests.
Read directly relevant company role/unknowns, resident/frontline journeys,
atlas, Fluent 2 foundations, WCAG/content baseline, profile/capstone and
architecture routing. No new legal-currentness assertion is needed.

Reflection: Inputs include obsolete requests to select Option B and an
unresolved communication choice. These are historical draft text to reconcile,
not executable instructions or reasons to repeat settled owner decisions.

#### Wave 2: Deeper

Independently hashed every file declared by the three validation records,
including source tools as custody data, with zero mismatches. Reconstructed
the BRD's 22 and PRD's 29 exact hunks in memory from pinned git bytes; base,
patch and candidate hashes exactly match the supplied records. No package
write occurred. Ran the inspected read-only PRD validator and BRD renderer
verify; both passed. The BRD validator itself writes validation.json and was
therefore deliberately not executed against read-only inputs.

The PRD validator independently checks full definition registries, all
original IDs, new allocations, FR/AC and new goal links, all 23 new BRD AC
mappings, 30 new Not run statuses, prior approval preservation, formula
recomputation and baseline-relative lint. It preserves three inherited PRD
MD056 table diagnostics and FR-059's inherited extra GOAL-002 matrix link.
The source BRD patch contains an unrelated FR-033/BG-013 matrix repair:
exclude that repair during integration per owner scope, retaining the
inherited discrepancy rather than expanding the task. The literal #58
Markdown escape is editorial only and may remain.

The explicit model is W=A*D; B=W*(C*Tc+E*Te)/60; G=B*U*V;
H=W*U*R*Tr/60; J=W*Q/60; F=G-H-J-S-A*U*To/60;
I=W*U*To/60 one-off. Recomputed low/base/high F:
-1.594/14.74/94.3333333333, W=324/720/1200.
Base F(U)=35.4U-2.96; uptake break-even 8.36158192%;
at U=.5, V break-even 29.90476190%.
Model remains conditional on later bounded routine authority, not current
activated automation. Mandatory additional per-message review must subtract
its actual incremental hours, not change the contact/case denominators.

Reflection: Owner decisions fit the proposed bounded-policy model without
numeric replacement. Keep human default while gate absent and named review
always for sensitive, consequential, uncertain, safety, consent, contractual
and financial messages. Managed external identity and role allocation can
be proposed now; specific provider/people/connectors/live permissions cannot.

#### Wave 3: Contrarian

Checked potential approval laundering: package BRD FAIL/BLOCKED and PRD
FAIL/BLOCKED reports have source-access/final-byte limitations, preserved as
history rather than substituted with new approval. ADR proposal still asks
for an already confirmed decision, states a still-unresolved FR-044 conflict,
and says every future reply is reviewed. These must be prospectively
reconciled with owner choices, with no actual exception activation.

Diagram JSON has 47 elements and valid Excalidraw v2; SVG text matches its
labels and the supplied PNG was visually inspected at 1800x1160. It depicts
the current OFF/default-review state, not activated routine automation.
Retain original three matching assets, label that state and non-native
SVG/Chrome provenance, add accessible text and explicitly state that task
registration depicted is required future state, not an observed task.

Source PRD proposes artificial one/two-working-day handoff ages. These are
simulation checks, not staffing or response SLAs; identify them explicitly
as constructed test ages. Staff chat/memory and regulatory no-send remain
unchanged. Historical executive "No resident portal needed" assets must not
be silently relabelled future scope: qualify them in architecture routing and
link the separate new proposal rather than regenerate historical diagrams.

Reflection: No unresolved product choice blocks the reduced document
publication. Real resident feasibility, approvals, tests and registration
remain unmet acceptance, not waived publication gates. The complete local
gate and exact-byte independent Review are still mandatory.

### Cycle 2 parent synthesis

| Material | Evidence | Disposition |
| --- | --- | --- |
| Exact package/base/candidate custody | C7-C9 | Verified; use exact patches then explicitly record integration deltas |
| Bounded routine policy and owner choices | C8, C10, native intake | Adopt prospectively, never activate |
| Unrelated inherited goal repair | C8 | Exclude from source patch integration |
| Unregistered architecture proposal | C5-C6, owner disposition | Publish under tracking with id null; registration stays unmet |
| Assets and text equivalent | C11 | Preserve matched originals, explain current OFF state and render provenance |
| Historical adverse reviews | C9 | Retain portable original evidence and separate new review scope |

### Additional evidence

| ID | Finding | Location | Confidence |
| --- | --- | --- | --- |
| C7 | Zero declared package hash mismatches; exact reconstruction matches source candidate hashes | .copilot-tracking/research/2026-10-23/resident-portal-requirements-441-input-custody.json:1 | High |
| C8 | Policy controls and model inputs/denominators are explicit; source FR-044 contradiction needs owner-directed edit | docs/brds/agentic-retrofit-programme-brd.md:1906; source amendment.patch and draft-prd-handoff.json verified by C7 | High |
| C9 | Read-only PRD validator passes; original quality FAIL/blocked history is not final-byte signoff | docs/prds/zava-forward-retrofit-programme-demonstrator.md:1; source quality/validation files verified by C7 | High |
| C10 | Current/future resident deferral needs dated prospective reconciliation, not rewrite of EXA-004 | docs/reference/research/ux/customer-journeys/residents.md:95 | High |
| C11 | Diagram depicts default review/OFF and same-model rendering, no native export | Verified source ADR diagram assets in C7 | High |
| C12 | Fluent 2 and accessibility/plain-language standards govern proposed resident tasks; no new UI delivered | docs/reference/research/ux/design-system.md:17; wcag-conformance-baseline.md:19; content-standard.md:20 | High |

### Current decisions and residual gates

Owner choices are sufficient for unsigned proposal drafting. Programme is
accountable, Engagement communication, Housing case exceptions, Digital
technical support; specialists retain domain escalation. Phone/email/visits
without detriment and manual absent-connector capture remain.
Managed external identity with simple username/password UX is selected
as proposal shape, not a provider or custom password store. Explicit
verified case/task/representative grants, revocation and assisted recovery
are required; actual enrollment/privacy/retention remain OD-54.

Registration bootstrap, OD-52-55 operational evidence, inherited SMART
quality and governance approvals remain follow-ups. They do not become
completed by this owner scope reduction or by later independent proposal
review. No further discovery solely to populate follow-ups.

### Current Planning Readiness and closeout

Research disposition: executed. Planning Readiness: Ready for the reduced
unsigned-document publication scope. Cycle 2 Wider/Deeper/Contrarian executed
in order, inline; no research worker claimed. All material scope/custody
questions answered for that scope. No additional research cycle is needed.
Original Cycle 1 blocked evidence above remains historical and unchanged.
RPI Agent may now execute the explicitly requested Plan/details and one
independent final-candidate critique before any product edits.

Self-check: scoped research, source and owner boundaries, verified custody,
formula applicability, alternatives, unknowns and next-phase gates recorded.
Local/hosted/human acceptance has not been inferred.
