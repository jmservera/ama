<!-- markdownlint-disable-file -->

# Task Research: rai-release-218

| Field | Value |
| --- | --- |
| Date | 2026-10-27 |
| Researcher / agent | RPI Agent / rpi-research |
| Status | Complete |
| Artifact path | .copilot-tracking/research/2026-10-27/rai-release-218-research.md |

## Research Brief

* Research #218 and listed children #219, #222, #223, #221 and #220 against current source and linked requirements.
* Purpose/audience: an evidence-qualified engineering PR for the owner.
* Scope: existing src RAI controls, evaluations and regression tests; dated RPI evidence.
* Non-goals: invented human appointments, manifest/threshold approval, participants, paid inference, private data, Azure or #224 implementation.
* Criteria: prove independent engineering behavior and explicitly retain unmet approval-dependent acceptance.
* Output mode: convergence, preparing planning.

## Research Parameters

* Posture: focused (default for named internal issues).
* Internal candidates: src/core, src/agents, src/api, evaluation review pack and linked ADR/PRD/BRD.
* External candidates: named GitHub issues and their decisions only.
* Limits: local tests only; at most one scoped changed gate for large changes under the nonblocking heavy lock; no full gate.
* Research writes: this research root and required workflow state only.
* Resolved evidence root: .copilot-tracking/research/2026-10-27.

## Extension Registry and Provenance

| Kind | Candidate | Authority and disposition |
| --- | --- | --- |
| Instructions | Repository guidance and explicit caller constraints | Selected; src-only, preserve original evidence and human gates; caller disallows full gate |
| Skill | rpi-research | Selected; three ordered evidence waves |
| Skill | rai-standards | Relevant domain reference; use only if existing requirements leave a technical uncertainty |
| Specialist | RPI Researcher | Skipped; one continuous existing-control trace is handled directly |

## User Participation and Research Decisions

Explicit request authorizes the ordered full loop and push/PR, not invented OQ-017 authority or approved manifest. Interaction is unavailable. Execute independent work; record human decisions without guessing.

## Direction Controls

Keep the pre-created clean topic branch feat/rai-release-218. One PR to main. #222's recorded manifest-before-evaluator approval restriction remains active; epic approval alone is not manifest approval. No acceptance criterion is ticked without full evidence.

## Research Questions

| ID | Question | Type | State |
| --- | --- | --- | --- |
| Q1 | What release/change-binding behavior is already present, and what independent correction is needed? | depth | Open |
| Q2 | Which cohort/reviewer engineering work is possible without manifest approval or participants? | depth | Open |
| Q3 | What suspension/challenge gaps remain independent of named authority? | depth | Open |

## Prior Knowledge Gate

Read all six named issues and comments, knowledge-base index opening, memory and original/addendum. Existing merged #315/#418/#419 evidence is historical and not whole-issue approval. Current branch has no PR and no uncommitted changes at intake.

## Research Cycle Log

### Cycle 1

#### Wave 1: Wider

Issue decisions show #222 requires actual manifest approval before evaluator implementation. #221 already retains constructed restart mechanics but human appointments/drill acceptance remain unknown. Inspect current source before choosing independent changes.

#### Wave 2: Deeper

Inspected the registry, release selector, actual assistant lifecycle, retained
priority dispatch, incident writer/restart checks and resident challenge tests.
Existing #219 tests cover stored binding mismatch and renewal; they do not
change the actual ranking/checklist definitions. The assistant binding hashes
its eligibility predicate and output schema but omits those dependent policies.
The retained priority binding similarly includes only a constant output policy.
The cohort proposal is in still-open PR #421, not on this main-based branch.
No actual manifest approval was found.

#### Wave 3: Contrarian

Challenged the hypothesis that source staleness alone solves policy release:
stock snapshots include ranking policy, and quality snapshots include checklists,
so existing proposals can become stale, but a fresh invocation still passes the
unchanged release binding. That is not renewed policy evaluation. Also
`capture` calls `ranking.describe()` whose default captures the original CURRENT
object: switching the current policy object can leave the stock explanation old.
Other assistant capabilities must remain independent of these policy changes.
Existing human verification is an explicit attestation, not semantic entailment:
valid citations with plausible wrong text can still be attested by a script.
Therefore do not claim #223 human effectiveness from service regression tests.

Parent disposition: accept the dependent-policy release gap as independent
engineering work; retain human/manifest gates as blocked, not discretionary
deferrals. Reject a parallel cohort evaluator or merging the unapproved proposal
pack into this branch. Existing incident/challenge machinery should be tested,
not duplicated or assigned fictitious owners.

## Evidence Log

* W1: https://github.com/jmservera/ama/issues/218, retrieved 2026-10-27: owner epic approval; #440 stabilization and #224 remain outside the selected child list.
* W2: https://github.com/jmservera/ama/issues/222, retrieved 2026-10-27: manifest approval required before evaluator implementation; no participants authorized.
* W3: https://github.com/jmservera/ama/issues/221, retrieved 2026-10-27: constructed engineering slice merged, actual authority and human-witnessed acceptance remain open.
* W4: https://github.com/jmservera/ama/issues/220, retrieved 2026-10-27: retained-priority challenge slice merged; other assistant/form coverage remains unproved.
* W5: https://github.com/jmservera/ama/issues/219, retrieved 2026-10-27: negative release controls evidenced, matching approved evaluation and broader material-change proof remain.
* W6: https://github.com/jmservera/ama/issues/223, retrieved 2026-10-27: real reviewer effectiveness is not yet demonstrated.
* C1: `src/core/src/zava_forward/core/assistants.py:296`: runtime policy binding omits ranking/checklist content.
* C2: `src/core/src/zava_forward/core/assistants.py:101`: stock capture uses a default-bound ranking policy, unlike explicit CURRENT at Store ranking reads.
* C3: `src/core/src/zava_forward/core/ai_registry.py:74`: retained priority release policy omits deterministic policy content.
* C4: `src/core/src/zava_forward/core/ranking.py:22`: existing canonical policy_hash permits reuse without another fingerprint algorithm; `ranking.py:168` confirms the default-bound describe behavior.
* C5: `src/core/src/zava_forward/core/quality.py:32`: CHECKLISTS and keyword dispatch are the dependent quality policy.
* C6: `src/core/src/zava_forward/core/assistants.py:996`: verification, review and audit retain actor/source signature/reason; no semantic adjudication is implemented or claimed.
* C7: `src/api/tests/test_operator_suspension.py:696`: existing restart denial and manual/hazard drill coverage; actual authority remains held.
* C8: `src/core/tests/test_resident_decisions.py:232`: existing digital/phone/letter/in-person retained-priority challenge coverage preserves unrelated case state.
* C9: `docs/prds/zava-forward-retrofit-programme-demonstrator.md:2165`: AC-069 to AC-073 remain Not run at whole-feature scope; OQ-017/018 at 2941/2942.
* C10: `docs/adrs/0002-pilot-readiness-architecture.md:326`: dependent policy invalidation, atomic reliance checks, manual continuity and distinct live approval boundaries.

## Findings, Alternatives and Decision State

Select dependent-policy fingerprints in the existing #219 release bindings,
with failing-first lifecycle regressions. Add bounded #223 oversight mechanics
regressions using explicit scripted dispositions and an automation-bias negative
control, never an actual reviewer study. Run existing #220/#221 checks and
document the acceptance matrix and missing decisions. No ranking behavior,
permission, resident consent or workflow approval changes.

## Open Questions, Risks and Residual Uncertainty

Named OQ-017/OQ-018 holders, actual manifest approval and competent review remain unavailable.

## Planning Readiness

Ready for the independent engineering slice only. Research disposition:
executed. Human effectiveness, #222 evaluator and whole-epic acceptance remain
blocked by named decisions/evidence. One complete ordered cycle answered Q1-Q3;
additional source research cannot supply human approval. Self-check: ordered
waves, provenance, source locations, alternatives, constraints and gaps recorded.
