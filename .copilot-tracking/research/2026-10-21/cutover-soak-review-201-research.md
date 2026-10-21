<!-- markdownlint-disable-file -->

# Task Research: cutover-soak-review-201

| Field              | Value                                                                  |
|--------------------|------------------------------------------------------------------------|
| Date               | 2026-10-21                                                             |
| Researcher / agent | rpi-research via RPI Agent (Claude Sonnet 5.5), inline waves           |
| Status             | Complete                                                               |
| Artifact path      | .copilot-tracking/research/2026-10-21/cutover-soak-review-201-research.md |

## Research Brief

* What to research: the current evidence state of all 11 original #201 acceptance criteria (AC), and what a reviewable soak evidence specification plus exact pending owner decisions would contain.
* Why it matters: the owner direction of 2026-10-20 asks to "propose soak duration and cut-over evidence checklist for review; no sign-off or legacy deletion" (C1). The actual cut-over gate stays blocked; this is preparation only.
* Audience or intended use: owner/Legal-Compliance-DPO Juan Manuel Servera (@jmservera), coordinator, later independent reviewer.
* Scope: `docs/architecture/cutover-evidence-pack.md`, `mvp-to-src-parity-matrix.md`, `cutover-parity-audit.tsv`, `cutover-reference-inventory.tsv`, `cutover-azure-evidence.json`, ADR 0006, rubric state, workflows, read-only GitHub state, index and log.
* Non-goals: Azure or paid calls, tenant writes, private files or data, backup attestation, archive tag, legacy deletion, issue or PR writes, AC ticking, completed soak, sign-off, a chosen minimum duration.
* Criteria: every claim has source, date and revision; missing, stale or unverified evidence stays UNMET; no owner decision is inferred.
* Requested outputs: AC mapping, soak specification proposal, pending owner decision list, reconciliation inside existing docs.
* Output mode: audit (decision state recorded, no forced recommendation on the open duration).

## Research Parameters

| Field                          | Value                                                                                   |
|--------------------------------|-----------------------------------------------------------------------------------------|
| Research question(s)           | Q1 to Q6 below                                                                          |
| Codebase scope                 | docs/, .github/, src/README.md, infra/README.md (read only); no private paths           |
| External scope                 | read-only GitHub issues, PRs, workflow runs for jmservera/ama                           |
| Research posture               | focused                                                                                 |
| Posture provenance             | default for a bounded internal task with named source targets                           |
| Explicit limits / deadline     | no Azure or paid calls; disk about 7.6 GB; USD500 total cap expires 2026-10-25T16:02Z   |
| Completion basis               | each AC mapped to dated evidence or UNMET; contrarian checks recorded                   |
| Edits allowed during research? | no, research-only (tracking writes only)                                                |
| Resolved evidence root         | .copilot-tracking/ (default)                                                            |
| Known constraints              | tenant/private data/backup attestation excluded; shared index/log append-only; no other worker's files |

## Extension Registry and Provenance

| Extension                                       | Provenance                | Disposition                                                  |
|-------------------------------------------------|---------------------------|--------------------------------------------------------------|
| Repository instructions (custom instruction)    | host-supplied             | Selected: docs conventions, evidence, branch, gate rules     |
| `rpi-research` skill                            | activated this run        | Selected                                                     |
| `github-backlog-manager` narrow-preparation review | task prompt (reviewed independently) | Noted: preparation independent of the blocked actual gate |
| Web design guidelines / design skills           | repo instruction          | Skipped: no web files change                                 |
| Specialist research subagents                   | host list                 | Skipped: low-volume, tightly coupled; inline fallback recorded |

## User Participation and Research Decisions

No interactive questions: non-interactive run; inputs sufficient. Owner direction is read from C1 and the task prompt. No owner decision is made or inferred.

## Scope and Success Criteria

Success: Q1 to Q6 answered from dated evidence; contradictions flagged; Planning Readiness recorded.

## Task Research Requests

Read #201, repo instructions, original/addendum/index/memory, pack, parity audit, inventory and Azure evidence; map all 11 AC; propose soak specification; list exact pending decisions; reconcile in existing docs.

## Direction Controls

* Active: preparation only; minimum soak duration remains OPEN; no invention of durations; USD500 cap overdrawn so no paid soak; keep other open files (#151 contrast web, #223, #97, #420) untouched.
* Excluded: private datasets, backups, Azure, tags, deletion, issue/PR writes.

## Research Questions

1. Q1 What is the current evidence and gap for each of the 11 AC?
2. Q2 Which existing statements are stale or contradictory?
3. Q3 What soak evidence specification can be proposed without inventing a duration?
4. Q4 Which decisions are exactly pending and who owns them?
5. Q5 Which existing docs should carry the reconciliation?
6. Q6 What constraints (budget, dependencies, other workers) bound the work?

## Prior Knowledge Gate

Existing pack, matrix and ADR are starting points; each claim re-verified against files, git and read-only GitHub on 2026-10-21 at base `993a7b88c03f5240f1e7a4c7c7afa7c064281622`.

## Research Cycle Log

### Cycle 1

Posture focused; inline execution (no delegation: small, tightly coupled sources).

#### Wave 1: Wider

Surveyed: issue body and comments (C1, W1 to W3), pack sections (C2 to C9), ADR 0006 (C10), matrix (C11), rubric artifacts and snapshots (C12, C13), workflows (C14), BRD version (C15), open PRs and epics (W4, W5), log and index (C16, C17), prior state/artifact naming conventions.

#### Wave 2: Deeper

Verified: prototype removal commit (C18), mvp tracked files (C19), parity counts and A1-A5 caveat (C4), test counts versus baseline (C5), rubric history 47 then 48 (C13), CI trigger change to PR-only (C14, W6), epic and open PR file overlap (W4, W5), pack edit overlap with open PR #423 (W7).

#### Wave 3: Contrarian

* Counter 1: the 2026-10-15 owner decision "no minimum soak" (W2, C10) means a soak may be unnecessary. Not resolved: the issue body still lists the soak as open and the 2026-10-20 direction asks for a proposal (C1). Treated as an unresolved contradiction; duration stays OPEN.
* Counter 2: rubric snapshots now show 48 versus 47 (C13); the pack statement "no valid post-migration numeric comparison" (C2) is stale. Not a clean before/after: baseline `fa730d63` registry state versus candidate unscored; floors false.
* Counter 3: "healthy src deployment" evidence exists (C6), so AC5 may look met. Rejected: the proof is 2026-10-16 historical, one fictional case, private only; later 2026-10-19 sections record failed publication and unmet real sign-in (C7).
* Counter 4: "no open PR on old paths" may be satisfied by an empty PR list. Refreshed 2026-10-21: seven open PRs, none touch `mvp/` or `prototype/` (W4); epics remain open, which is not completion evidence.

#### Parent Synthesis and Disposition

* Accepted: AC table below; soak specification as proposal; contradiction flagged.
* Rejected: treating the 2026-10-15 "no soak" as superseded or confirmed; inferring a duration; treating historical health 200 as current.
* Deferred: all human, tenant, backup and budget items to named owners.

#### Cycle Re-entry Evaluation

No second cycle needed: remaining gaps need owner or tenant action, not further reading. Smallest evidence to re-enter: an owner decision on D1 to D3 or a fresh deployed candidate.

## Evidence Log

### Codebase Evidence

| ID  | Path:line                                                                 | Finding                                                                                                                          |
|-----|---------------------------------------------------------------------------|----------------------------------------------------------------------------------------------------------------------------------|
| C1  | docs/architecture/cutover-evidence-pack.md:31                             | Owner 2026-10-15: no minimum soak; healthy deployment and sign-off precede deletion                                              |
| C2  | docs/architecture/cutover-evidence-pack.md:1697-1717                      | Epics open; rubric 47 at `fa730d63` stale; "no valid post-migration numeric comparison"; BRD 0.18.0, tag `v0.18.0` prospective    |
| C3  | docs/architecture/cutover-evidence-pack.md:1719-1749                      | Owner sign-off checklist, all boxes unchecked                                                                                    |
| C4  | docs/architecture/cutover-evidence-pack.md:1100-1134                      | 130 rows (116 migrate, 1 partial rebuild, 12 retire, 1 archive); 578 historical paths mapped; A1-A5 ratification not claimed    |
| C5  | docs/architecture/cutover-evidence-pack.md:1195-1202                      | Baseline 719/92 skips; later runs 1,164/104; equal-or-greater count supported, measured coverage not established                 |
| C6  | docs/architecture/cutover-evidence-pack.md:781-896                        | 2026-10-16 private health 200, native API 401, edge proof; real-user smoke Blocked (#349), feature acceptance Blocked (#350)     |
| C7  | docs/architecture/cutover-evidence-pack.md:36-83                          | 2026-10-19: direct probes 403, Graph read failed, VM capacity failed; d/e UNMET; initializer and API on old proof digests         |
| C8  | docs/architecture/cutover-evidence-pack.md:1100                           | Matrix is migration record, not acceptance                                                                                       |
| C9  | docs/architecture/cutover-reference-inventory.tsv                         | Generated reference locations for `mvp/`, `prototype/`, `mvp-ci.yml`, `mvp-validation.yml`; routing not approval                 |
| C10 | docs/adrs/0006-src-layout-and-cutover.md:9, :298, :366                    | ADR Accepted 2026-10-15; no soak decision; gate list                                                                             |
| C11 | docs/architecture/mvp-to-src-parity-matrix.md:451, :592, :600             | Service-role denial gap; soak None; open owner decisions                                                                         |
| C12 | .github/rubric/artifacts.json:33-34                                       | Registry includes `src/**/*`; excludes `mvp/data/**` and src data/vendor                                                         |
| C13 | .github/rubric/scores/latest.json                                         | 48 (A30 B13 C5 D0), floors false, "Incomplete (thought leadership artifact not submitted)", commit `332101ed`, 2026-10-20; history 47 at `fa730d63` 2026-10-15, 48 from `b1fd9042` 2026-10-16; rubric_version 2 throughout |
| C14 | .github/workflows/src-ci.yml:3-5                                          | Triggers are `pull_request` (path filtered) and `workflow_dispatch` only; no push trigger                                        |
| C15 | docs/brds/agentic-retrofit-programme-brd.md:9                             | BRD version `0.18.0` on 2026-10-21; no `v*` tag exists (git tag list empty; `git ls-remote` empty)                              |
| C16 | docs/reference/log.md (tail)                                              | Append-only log, last entry 2026-10-20                                                                                           |
| C17 | docs/reference/README.md:288                                              | Existing index row for "Review cut-over evidence and owner gates (#200/#201)"                                                    |
| C18 | git commit a7e30046 (2026-10-15, #295)                                    | `prototype/` retired; `ls prototype` absent                                                                                      |
| C19 | git ls-files mvp                                                          | Only `mvp/README.md` tracked                                                                                                     |

### External Evidence

| ID | Source                                                                  | Finding                                                                                                                            |
|----|-------------------------------------------------------------------------|------------------------------------------------------------------------------------------------------------------------------------|
| W1 | gh issue view 201 (2026-10-21)                                          | Eleven unchecked AC; "Open decisions for the owner: Minimum soak period on the src/ build before deletion"                         |
| W2 | #201 comment 6196800819 (2026-10-15)                                    | Owner: no minimum soak period; deletion follows sign-off and healthy deployment                                                    |
| W3 | #126 comment 6290697705 (2026-10-20)                                    | Preparation direction for #201/#202: propose soak duration and evidence checklist for review; no sign-off or deletion              |
| W4 | gh pr list / gh pr view (2026-10-21)                                    | Open PRs 420 to 426; none changes `mvp/` or `prototype/` paths; #423 edits the evidence pack; all touch index/log                  |
| W5 | gh issue view 113,136,165,157,149,200,202,203 (2026-10-21)             | All OPEN; last updates 2026-10-14 to 2026-10-16                                                                                    |
| W6 | gh run list (2026-10-21)                                                | Runs on `993a7b88` are rubric, dependency graph and infra what-if; no src-ci push run; last main src-ci push run 2026-10-18 `612cbed7` success |
| W7 | gh pr diff 423 (2026-10-21)                                             | #423 hunks at pack lines 1-7 and 166-190, not near "Other Cut-Over Gates"                                                          |

### Contradictions / Conflicts

* Soak: W1 (open decision, body unchanged) and W3 (propose) versus W2, C1, C10, C11 ("no minimum soak"). Unresolved; escalated as decision D1.
* Rubric: C2 ("no valid post-migration comparison") versus C13 (48 versus 47 snapshots). Resolved as reconciliation note: pair exists, comparability and candidate score not established.
* Health: C6 (200) versus C7 (later failures, old digests). Health proof is dated 2026-10-16 only.

## Findings Mapped to Questions and Evidence

* Q1: AC table below (all 11, none fully met by current evidence).
* Q2: three conflicts above; also pack "initial inspection open PR list" refreshed by W4.
* Q3: soak specification in the plan and the reconciled pack section; no duration is proposed.
* Q4: decisions D1 to D12 listed in the plan.
* Q5: reconcile in the existing pack (new dated section and checklist note), the index row, the log, ADR 0006 and matrix by pointer only if needed; no new competing document.
* Q6: budget cap overdrawn, other workers own README/web/contrast files, #423 overlaps the pack.

### Original 11 AC mapping (as of 2026-10-21, base `993a7b88`)

| # | AC | Source, date, revision | What it proves | Gap | Status | Human owner |
|---|----|------------------------|----------------|-----|--------|-------------|
| 1 | Layout ADR accepted | C10; ADR 0006 Accepted 2026-10-15; owner comment 6196711316 | Acceptance recorded | A1-A5 placement exceptions not ratified (C4) | MET for ADR acceptance; A1-A5 disposition open | @jmservera |
| 2 | `prototype/` retired | C18 `a7e30046` 2026-10-15; C19 | Directory absent, content mapped | Service-role denial gap unresolved (C11) | MET for removal; mapping caveat open | @jmservera |
| 3 | Parity matrix complete | C4, C8; audit TSV regenerated at pack revision | 130 rows each migrated, mapped or retired; zero unmapped names | Matrix is not acceptance; partial assistant rebuild; owner agreement on retire rows not recorded; audit not rerun at base | PARTIAL (UNMET for owner agreement) | @jmservera |
| 4 | Tests migrated, passing, equal or greater coverage | C5, C14, W6 | Count 1,164 vs baseline 719 on named runs; CI green historically | Measured coverage not established; no CI on candidate commit; CI is PR-only | UNMET (count supported only) | Coordinator, @jmservera |
| 5 | CI/Docker/Bicep/scripts repointed; src build deployed and healthy | C6, C7, C14 | Repointing evidenced; private health 200 on 2026-10-16 for one fictional case | Historical only; later failures; no real staff sign-in; initializer and API on old digests; no candidate deploy | UNMET (repoint evidenced; deploy and health stale) | Tenant operator, @jmservera |
| 6 | Rubric tracks `src/`; before/after recorded; dip cause and recovery recorded | C12, C13, C2 | Registry tracks `src/`; snapshots 47 then 48; no dip observed | No candidate-commit score; baseline comparability unverified; floors false; cause/recovery statement not recorded at sign-off | PARTIAL (UNMET until candidate scored and recorded) | @jmservera |
| 7 | Dependent epics have no open work on old paths | W4, W5 | 2026-10-21: no open PR touches `mvp/` or `prototype/`; epics OPEN | Epic open state is not acceptance; refresh at sign-off | PARTIAL; refresh required | @jmservera |
| 8 | Docs, ADRs, index, log, live instructions updated; links checked | C9, C16, C17; this task | Inventory exists; this task adds reconciliation and focused link check | Live workflow names retained until rename PR; full link gate is external | PARTIAL | Coordinator |
| 9 | Archive tag `v<BRD version>` confirmed | C15 | BRD `0.18.0` today; prospective `v0.18.0` | Not confirmed at cut-over; no tag created | UNMET | @jmservera |
| 10 | Private `mvp/data/` relocated and backed up outside git | C3 | Nothing agent-verifiable | Owner-only attestation; no agent read | UNMET | @jmservera |
| 11 | Owner signs off in issue | C3, W1 | None | No sign-off exists or is inferred | UNMET | @jmservera |

## Key Discoveries

* The soak is an open decision in the issue body yet "none" in ADR 0006; the owner asked on 2026-10-20 for a proposal, so a recorded reconciliation is needed (D1).
* The rubric snapshot pair undercuts the pack's stale "no comparison" sentence.
* CI is PR-only, so "CI green on candidate" must cite PR checks and the external gate receipt, not a push run.
* Budget: USD500 total cap expires 2026-10-25T16:02Z; forecast already over cap; any soak needing running resources has no approved headroom.

## Alternatives and Decision State

### Decision State (audit mode)

No selection is forced on D1 (soak required or not) or the duration. Proposal alternatives for the owner:

* Alternative A: no minimum soak (existing 2026-10-15 decision restated); deletion follows sign-off and a healthy deployment.
* Alternative B: event-based window (owner-set count of consecutive healthy checks on a frozen candidate), no calendar minimum.
* Alternative C: calendar window (owner-set duration) with the reset rules in the specification.
* Rejected for invention risk: any proposed number of days or checks.

## Open Questions, Risks, and Residual Uncertainty

* Whether `fa730d63` registry state is comparable to the candidate.
* Whether the owner wants the soak to cover the public edge, private path or both.
* Risk: pack edits collide with #423 (mitigated by distinct hunks).
* Risk: new commits to `src/` reset a frozen candidate.

## Current Decisions

* Preparation only; owner authorization W3. Status confirmed; owner: @jmservera; evidence W3.
* Minimum soak duration OPEN by task instruction.

## Unresolved Decisions

* D1 to D12 (see plan). Owner: @jmservera unless noted. Smallest missing evidence: an owner comment in #201.

## Potential Next Research

None before owner decisions; after D1, fresh deployed-candidate evidence.

## Planning Readiness

* Status: Ready
* Decision state: audit; no recommendation on duration
* Evidence basis: C1 to C19, W1 to W7
* Preconditions met: AC mapping, contradictions, constraints recorded
* Blockers: none for preparation; actual gate blocked by owner, tenant, budget
* Smallest action to change readiness: none

## Closeout Record

| Field                            | Record                                                  |
|----------------------------------|---------------------------------------------------------|
| Research execution status        | Complete                                                |
| Completed waves                  | Wider, Deeper, Contrarian (cycle 1)                     |
| Lane evidence or inline fallback | Inline; no delegation, low-volume coupled sources       |
| Research disposition             | executed                                                |
| Planning Readiness               | Ready (C1 to C19, W1 to W7)                             |
| Blockers                         | none                                                    |
| Continuation owner and state     | confirmed automatic RPI Agent, continuing to Plan       |

## Advisory Next Step

| Field                            | Record                                                         |
|----------------------------------|----------------------------------------------------------------|
| Research disposition             | executed                                                       |
| Planning Readiness               | Ready                                                          |
| Output mode and planning support | audit; yes, planning supported by evidence                     |
| Acting owner                     | confirmed automatic RPI Agent                                  |
| Required gates or confirmations  | none pending                                                   |
| Continuation result              | automatic continuation to Plan                                 |
| Primary evidence file            | .copilot-tracking/research/2026-10-21/cutover-soak-review-201-research.md |

* Advisory only: rpi-research does not invoke `/rpi-plan`.
* Completion basis: remaining gaps require owner, tenant or budget action, not further reading.

## Sources

* W1 - Issue #201 - https://github.com/jmservera/ama/issues/201 (retrieved 2026-10-21)
* W2 - #201 comment 6196800819 - https://github.com/jmservera/ama/issues/201#issuecomment-6196800819 (retrieved 2026-10-21)
* W3 - #126 comment 6290697705 - https://github.com/jmservera/ama/issues/126#issuecomment-6290697705 (retrieved 2026-10-21)
* W4 - Open pull requests 420 to 426 - https://github.com/jmservera/ama/pulls (retrieved 2026-10-21)
* W5 - Epics and #200, #202, #203 - https://github.com/jmservera/ama/issues (retrieved 2026-10-21)
* W6 - Workflow runs - https://github.com/jmservera/ama/actions (retrieved 2026-10-21)
* W7 - PR 423 diff - https://github.com/jmservera/ama/pull/423 (retrieved 2026-10-21)

## Artifact Self-Check

* [x] Every research question is answered or marked with missing evidence.
* [x] Cycle 1 includes Wider, Deeper, Contrarian in order.
* [x] Posture, provenance, limits and completion basis recorded.
* [x] Codebase findings carry C# and path:line; external findings carry W# with URL and date.
* [x] Every W# resolves in Sources.
* [x] Extension Registry and User Participation recorded.
* [x] Parent synthesis dispositions and re-entry evaluation recorded.
* [x] Audit mode keeps decision state without forced selection.
