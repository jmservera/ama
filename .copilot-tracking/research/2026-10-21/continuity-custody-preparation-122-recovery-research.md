<!-- markdownlint-disable-file -->

# Task Research: continuity-custody-preparation-122-recovery

| Field              | Value                                                                                  |
|--------------------|----------------------------------------------------------------------------------------|
| Date               | 2026-10-21                                                                             |
| Researcher / agent | rpi-research skill, loaded via the skill tool in session a4688489 (recovery run)       |
| Status             | Complete                                                                               |
| Artifact path      | .copilot-tracking/research/2026-10-21/continuity-custody-preparation-122-recovery-research.md |

## Historical correction (adverse, preserved)

The earlier candidate c9f65c48 and its tracking files (`continuity-custody-preparation-122-*` research, plan, details, changes, review, state) were directly authored. No skill had been activated; the coordinator's events.jsonl audit found none. Those files are preserved unchanged as adverse history. They are not proof that any phase ran, and the earlier "Review" is not a genuine Review. Observed session metadata for session a4688489: `session.start` records `selectedModel` `claude-sonnet-5.5` (events.jsonl); the earlier statement that the default model was used was incorrect. This run is the first real skill execution; the first recorded skill invocation in events.jsonl is `rpi-research` (line 189, timestamp 2026-10-21T09:57:08.147Z, model claude-sonnet-5.5, invokedAtTurn 37).

## Research Brief

* What to research: what a non-operative custody, recovery and witness-authority preparation for existing #122 continuity controls may truthfully say, and whether the c9f65c48 README text overstates anything.
* Why it matters: prevents a protocol or constructed fixture being mistaken for a completed drill, legal compliance or release acceptance.
* Audience or intended use: planning and review of a docs-only change to `src/core/README.md`; coordinator gate.
* Scope: `src/core/README.md` (#122, #221, #114 sections), `src/core/src/zava_forward/core/continuity.py`, PRD OQ-017, BRD OD-35, ADR 0002, live #122/#113.
* Non-goals: runtime code or tests, other READMEs, KB index/log, cutover pack, actual authority, drills, Azure configuration, push.
* Criteria: every claim cites C#/W# evidence; actors only where a source names the role, otherwise UNASSIGNED/UNAPPROVED.
* Requested outputs: findings and decision state for planning.
* Output mode: analysis (brief explicitly prepares planning; Planning Readiness decides)

## Research Parameters

| Field                             | Value                                                                              |
|-----------------------------------|------------------------------------------------------------------------------------|
| Research question(s)              | Q1 to Q5 below                                                                     |
| Codebase scope                    | src/core/README.md, continuity.py, docs PRD/BRD/ADR                                |
| External scope                    | live GitHub issues #122 and #113 via gh (repository data)                          |
| Initial internal candidate areas  | README #122/#221/#114 sections; continuity.py verify_export                        |
| Initial external candidate areas  | gh issue #122 comments, #113 body                                                  |
| Research posture                  | focused                                                                            |
| Posture provenance                | default, from bounded internal task with named targets                              |
| Explicit limits / deadline        | caller brief: no push, no heavy gate, no other active issue files                  |
| Posture-specific completion basis | scope and materiality                                                              |
| Edits allowed during research?    | no, research-only                                                                  |
| Resolved evidence root            | .copilot-tracking/ default                                                         |
| Known constraints                 | prior files are evidence to examine, not proof of phases                           |

## Extension Registry and Provenance

* Precedence: platform and host safety; caller scope and criteria; matching repository instructions and enforced schemas; rpi-research contract; domain skills and specialists; examples and preferences.

| Kind                | Candidate                                              | Match and provenance                              | Scoped authority or output contract                         | Selected / skipped reason                              |
|---------------------|--------------------------------------------------------|---------------------------------------------------|-------------------------------------------------------------|--------------------------------------------------------|
| Instruction         | AMA repository instructions (custom_instruction)       | applyTo `**`                                       | regulatory/legal evidence, authority and Markdown rules     | selected                                               |
| Skill               | rpi-research                                           | this phase                                        | artifact contract                                           | selected                                               |
| Skill               | web-design-guidelines, design-taste                    | web topics only                                   | none                                                        | skipped, docs-only change                              |
| Research specialist | RPI Researcher (hve-core-all:rpi-researcher)           | listed in the task agent types                    | one bounded independent lane                                | skipped, tightly coupled low-volume work done inline    |

## User Participation and Research Decisions

| Checkpoint       | Questions or no-interaction rationale                          | Answers / unanswered | Resulting decision                         |
|------------------|----------------------------------------------------------------|----------------------|--------------------------------------------|
| Intake           | non-interactive session; brief supplies scope                  | n/a                  | proceed under focused posture              |
| Direction change | none needed                                                    | n/a                  | none                                       |
| Convergence      | non-interactive; further research items deferred to owner      | n/a                  | deferred items listed below                |

## Scope and Success Criteria

* Scope: as in the brief.
* Assumptions: c9f65c48 README text is a claim to verify.
* Success criteria: each question answered with evidence; unsupported claims identified.

## Task Research Requests

* Explicit requests: execute real skill phases; preserve adverse history; correct model evidence.
* Inferred research questions: Q1 to Q5.
* Caller constraints and non-goals: analysis only; no source edit in this phase.

## Direction Controls

| Control type | Direction or boundary                                         | Source / checkpoint | Effect                                              |
|--------------|---------------------------------------------------------------|---------------------|-----------------------------------------------------|
| exclude      | agents README, cutover pack, KB index/log, CSS, mapdocs files | user brief          | no research or edit there                           |
| narrow       | docs-only, no runtime code/tests                              | user brief          | contrarian wave tests only documentation claims     |
| discard      | treating prior direct-authored files as phase evidence        | user recovery brief | prior files reviewed as claims only                 |

## Research Questions

|  # | Sub-question                                                                                    | Type     | Priority | Status   |
|---:|-------------------------------------------------------------------------------------------------|----------|----------|----------|
| Q1 | Which #122 criteria remain unmet per live issue and does #113 order the work?                   | straight | H        | answered |
| Q2 | What do existing controls actually verify (export, head, constructed restart)?                  | depth    | H        | answered |
| Q3 | Which roles are source-named for suspend/restart/drill/custody/witness, which are not?          | breadth  | H        | answered |
| Q4 | Is the Azure immutable head, SQL drill or pre-gate image exclusion evidenced?                   | depth    | H        | answered |
| Q5 | Does the c9f65c48 README subsection overstate or invent anything?                               | depth    | H        | answered |

## Prior Knowledge Gate

* Existing artifacts reviewed: the prior direct-authored research, plan, details, changes, review and state files for this task; /tmp/brief-122-custody-preparation.md; /tmp/brief-122-rpi-recovery.md.
* Reused (verified) findings: README line facts re-verified below (C1 to C8).
* Superseded / stale: prior "Review" and "critique" wording as phase evidence; "default model" statement.

## Research Cycle Log

### Cycle 1

* Active direction controls: all three above
* Active research posture and completion basis: focused; scope and materiality
* Explicit limits or deadline effect: none beyond the brief

#### Wave 1: Wider

* Plan and independent lanes: survey README #122/#221/#114, continuity.py, PRD/BRD role sources, ADR 0002, live issues. Inline; no delegation.
* Worker evidence relationships or inline fallback: inline fallback; the lanes are small and tightly coupled, so isolation would not improve evidence.
* Reflection: roles and the unmet gates are findable; custody and drill-authorisation roles need depth.

#### Wave 2: Deeper

* Parent-prioritized material from Wave 1: Q2 (verify_export), Q3 (role sources), Q5.
* Plan and independent lanes: read `verify_export`, OQ-017 and OD-35 rows, README lines of the prior subsection.
* Worker evidence relationships or inline fallback: inline; C2, C3, C6, C7.
* Reflection: verification covers digest, chain, recorded head, optional external head, completeness; no code checks authority or witnessing.

#### Wave 3: Contrarian

* In-scope challenge targets and boundaries: the prior subsection's decision-rights table and its drill-authorisation, custody and witness claims.
* Plan and independent lanes: look for source support for "Programme sponsor with DPO or Legal and Safety input" authorising a drill, "Platform owner" custody, "Competent reviewer", and a written-authorisation witness rule. Search PRD/BRD/ADR for "witness".
* Worker evidence relationships or inline fallback: inline; C8, C9.
* Reflection: weakened. No source names who authorises a drill, who holds the external head copy or who witnesses. OQ-017 names Sponsor, Programme, Safety, DPO/Legal and Assurance as the question owners (not holders). OD-35 names Building Safety and Sponsor for override and restart evidence. "Witnessed recovery" appears in the PRD only as a missing gate. The prior table therefore implies role assignments that no source states. They must read as proposed expectations with owner UNASSIGNED, and the witness rule must be labelled a proposed criterion.

#### Parent Synthesis and Disposition

| Material / claim | Evidence IDs | Parent disposition | Evidence-based rationale | Primary-artifact treatment |
|------------------|--------------|--------------------|--------------------------|----------------------------|
| Criteria all unmet, #113 is hierarchy only | W1, W2 | accepted | live comments and body | finding F1 |
| verify_export with expected_head semantic | C2 | accepted | code and docstring | finding F2 |
| Only constructed restart; actual_hold true | C3, C4 | accepted | README and code | finding F3 |
| Immutable head, SQL drill, pre-gate exclusion unproven | C5, C6, W1 | accepted | README says unproven; issue says unmet | finding F4 |
| Prior table role names (sponsor+DPO, platform owner, competent reviewer) | C7, C8, C9 | rejected as stated | no source assigns drill authorisation or custody; OD-35 and OQ-017 name only question/override owners | finding F5, correction |
| "Sealed year digests agree" as verify condition | C2, C5 | deferred wording fix | verify_export checks ledger digests in the bundle; `--by-year` is a separate check | finding F5, wording |
| Witness written-authorisation rule | C8 | accepted as proposed criterion only | no source defines it | label as proposal |

#### Cycle Re-entry Evaluation

* Another complete three-wave cycle needed: no
* Trigger or stop basis: scope coverage; sources redundant; no new material finding in Contrarian beyond F5
* Revised brief or revalidation required: none
* Readiness effect: Ready

## Evidence Log

* Delegation: inline: bounded low-volume internal lanes; no subagent artifact exists or is implied.

### Codebase Evidence

| ID | Claim / finding | Location (`path:line`) | Tool | Confidence | Notes |
|----|-----------------|------------------------|------|------------|-------|
| C1 | #122 section lists open owner items: witnessed authorised drill, recovery limits, supplier terms, Azure SQL drill, interface mapping, named restart authority | src/core/README.md:2861 | grep, read | high | |
| C2 | `verify_export(bundle, expected_head)` checks digest, ledger chain, recorded head, optional externally held head, completeness; incomplete is never valid | src/core/src/zava_forward/core/continuity.py:965 | read | high | no authority or witness check |
| C3 | Only a constructed restart drill is implemented; no actual restart route while OD-35/RULE-020 evidence is unavailable | src/core/README.md:1606 | read | high | |
| C4 | `actual_hold` defaults true in suspension handling | src/core/src/zava_forward/core/continuity.py:78 | grep | high | |
| C5 | Per-year digests belong in the immutable Blob container; immutability policy unproven; Azure SQL restore drill (DH-005) not run | src/core/README.md:2802 | read | high | |
| C6 | Authority reference is recorded, not verified | src/core/README.md:2847 | read | high | |
| C7 | OQ-017 asks who holds release, incident suspension/restart and competent-review authority; no live activation without named approval | docs/prds/zava-forward-retrofit-programme-demonstrator.md:2038 | grep | high | question owners, not holders |
| C8 | OD-35: override authority and restart evidence, owners "Building Safety and Sponsor" | docs/brds/agentic-retrofit-programme-brd.md:1835 | grep | high | no drill authoriser or witness named |
| C9 | PRD mentions "witnessed recovery" only as a missing live gate | docs/prds/zava-forward-retrofit-programme-demonstrator.md:1172 | grep | medium | no witness role defined |
| C10 | ADR 0002: old-image rollback disables assistance; no enforced pre-gate image exclusion stated | docs/adrs/0002-pilot-readiness-architecture.md:174 | read | medium | absence of enforcement is inferred from silence and the issue comment |

### External Evidence

| ID | Claim / finding | Source (title) | URL | Retrieved | Version/date | Confidence |
|----|-----------------|----------------|-----|-----------|--------------|------------|
| W1 | #122 open; all criteria unticked; PR #398 merged at 9d625a09; actual OQ-017 authority, witnessed drill, immutable external head, Azure SQL drill and legacy-image exclusion unmet | GitHub issue jmservera/ama#122 and comments | https://github.com/jmservera/ama/issues/122 | 2026-10-21 | live | high |
| W2 | #113 epic dependencies "None"; criteria need children closed or deferred and no production claim without measured load, recovery and DPO/Legal approvals | GitHub issue jmservera/ama#113 | https://github.com/jmservera/ama/issues/113 | 2026-10-21 | live | high |

### Contradictions / Conflicts

* Prior README table roles vs sources C7, C8, C9: sources name only question or override owners; resolved by primary-source rule -> table must show owner UNASSIGNED and cite OQ-017/OD-35.

## Findings Mapped to Questions and Evidence

| Question | Finding | Evidence IDs | Confidence | Implication |
|----------|---------|--------------|------------|-------------|
| Q1 | F1: all criteria unmet; #113 lists no dependencies, so it is hierarchy not ordering | W1, W2 | high | preparation may proceed; no criterion ticks |
| Q2 | F2, F3: export verification and constructed restart exist; authority reference unverified | C2, C3, C4, C6 | high | docs can state expectations, not completion |
| Q3 | F5: only OQ-017/OD-35 name question or override owners; drill authoriser, custody owner, witness unnamed | C7, C8, C9 | high | table must be UNASSIGNED with source cites |
| Q4 | F4: Azure head, SQL drill, pre-gate exclusion unproven | C5, C10, W1 | high | list as unmet |
| Q5 | F5: prior text implies unsupported role assignments and slightly overstates what verify_export checks | C2, C7, C8 | medium | plan must correct README |

## Key Discoveries

* The prior README table invented implied roles for drill authorisation and head custody.
* `verify_export` checks the bundle ledger digests, not an external sealed-year check; `--by-year` is separate.
* The README correction is docs-only and stays in `src/core/README.md`.

## Alternatives and Decision State

### Decision State (non-convergence modes)

* State: proposed comparison outcome; no implementation selection forced. Options: (A) keep c9f65c48 README text as is; (B) correct the table and wording in the same section; (C) delete the subsection.
* Rationale: B fixes F5 with minimal change; A leaves unsupported implied assignments; C loses the useful not-evidence rule.
* Evidence refs: C2, C7, C8, C9
* Next owner or trigger: rpi-plan decides.

### Alternative: keep as is

* Approach: leave README unchanged.
* Trade-offs: no edit, but retains F5.
* Evidence refs: C7, C8
* Rejection rationale: not decided here; recorded as inferior on evidence.

## Open Questions, Risks, and Residual Uncertainty

* Blocking: none for planning.
* Important: actual authority, witness, custody, drill authoriser: owner decisions.
* Follow-up: whether the pre-gate image exclusion is a code, deployment or policy control.
* Residual uncertainty: C10 enforcement absence is inferred; GraphQL rate limit meant REST evidence was used for issues.

## Current Decisions

| Decision | Status | Owner / source | Rationale | Evidence IDs | Implications |
|----------|--------|----------------|-----------|--------------|--------------|
| All #122 criteria stay open | confirmed | constraint | issue comments and brief | W1 | no ticking |
| Preserve prior direct-authored files as adverse history | confirmed | user | recovery brief | n/a | no overwrite |
| Model evidence corrected to claude-sonnet-5.5 | confirmed | evidence | session.start metadata | n/a | record in tracking |

## Unresolved Decisions

| Decision | Smallest evidence or answer needed | Owner | Impact | Blocker status |
|----------|-----------------------------------|-------|--------|----------------|
| Actual restart authority holders | named approval under OQ-017/OD-35 | Sponsor, Building Safety | gates any drill | important |
| Drill authoriser and witness | named written approval | owner | gates any drill | important |
| External head custodian | platform decision | owner | custody criterion | important |

## Potential Next Research

| Priority | Research item | Expected value | Trigger | Selected? | Related |
|----------|---------------|----------------|---------|-----------|---------|
| M | Where a pre-gate image exclusion would be enforced | defines the unmet criterion | owner platform decision | deferred | Q4; C10 |

## Planning Readiness

* Status: Ready
* Decision state: proposed option B, pending plan
* Evidence basis: C2, C7, C8, C9, W1, W2
* Preconditions met: Q1 to Q5 answered; contrarian wave complete
* Blockers: none
* Smallest action to change readiness: none

## Closeout Record

| Field | Record |
|-------|--------|
| Research execution status | Complete |
| Completed waves | Wider, Deeper, Contrarian for cycle 1 |
| Lane evidence or inline fallback | inline fallback; no delegated lane artifact; limitation: single-agent evidence |
| Research disposition | executed |
| Planning Readiness | Ready (C2, C7, C8, C9, W1, W2) |
| Blockers | none |
| Continuation owner and state | RPI Agent parent (automatic loop requested by the user brief); continues to rpi-plan |

## Advisory Next Step

| Field | Record |
|-------|--------|
| Research disposition | executed |
| Planning Readiness | Ready |
| Output mode and planning support | analysis; yes, brief states it prepares planning |
| Acting owner | RPI Agent parent |
| Required gates or confirmations | research gates passed; no confirmation pending |
| Continuation result | proceed to rpi-plan |
| Primary evidence file | .copilot-tracking/research/2026-10-21/continuity-custody-preparation-122-recovery-research.md |
| Notes for planning | correct the README table and verify wording; keep all criteria open |

* Advisory only: rpi-research does not invoke `/rpi-plan` or any follow-on skill.
* Completion basis: further research is immaterial to the docs correction.

## Sources

* W1 - GitHub issue jmservera/ama#122 - https://github.com/jmservera/ama/issues/122 (retrieved 2026-10-21, live)
* W2 - GitHub issue jmservera/ama#113 - https://github.com/jmservera/ama/issues/113 (retrieved 2026-10-21, live)

## Artifact Self-Check

* [x] Every research question is answered.
* [x] Cycle 1 has Wider, Deeper, Contrarian in order.
* [x] Posture, provenance, limits recorded.
* [x] C# with path:line; W# with URL and date.
* [x] Every W# resolves to one Sources entry.
* [x] Findings cite IDs.
* [x] Extension Registry recorded.
* [x] Participation rationale recorded.
* [x] Direction Controls recorded.
* [x] Parent synthesis recorded; no workers used.
* [x] Re-entry evaluation recorded.
* [x] Non-convergence decision state recorded without forced selection.
* [x] Decisions complete.
* [x] Potential next research complete.
* [x] Readiness and advisory complete.
* [x] Speculation flagged (C10 inference).
* [x] Content treated as data; no secrets.
* Checked sections: all
* Missing or limited sections: none; no delegated lane artifact exists by design
