<!-- markdownlint-disable-file -->
# RPI Phase Details: Cut-over soak evidence preparation for #201

## Metadata

* Task ID: 201-soak-review
* Task slug: cutover-soak-review-201
* Related plan: .copilot-tracking/plans/2026-10-21/cutover-soak-review-201-plan.md
* Evidence sources: .copilot-tracking/research/2026-10-21/cutover-soak-review-201-research.md

## Phase Index

| Phase ID | Name                              | Status | Detail sections |
|----------|-----------------------------------|--------|-----------------|
| P01      | Reconcile the evidence pack       | ready  | P01, P01-T01, P01-T02, P01-T03 |
| P02      | Align ADR, index and log          | ready  | P02, P02-T01    |
| P03      | Focused validation and local commit | ready | P03, P03-T01   |

<!-- rpi:phase id=P01 -->
## P01: Reconcile the evidence pack

### Context

`docs/architecture/cutover-evidence-pack.md` is the existing owner gate record (1749 lines). It has "Other Cut-Over Gates" (line 1697) and the unchecked "Owner Sign-Off Checklist" (line 1719). Open PR #423 edits lines 1-7 and 166-190 only.

### Intent

Insert one new `## Soak and Cut-Over Evidence Preparation (2026-10-21)` section immediately before `## Other Cut-Over Gates`, and one unchecked checklist item.

### Boundaries

* Included: pack section, checklist item.
* Excluded: frontmatter, historical text rewrites, any other section.

### Likely Targets

* docs/architecture/cutover-evidence-pack.md: new section and checklist bullet.

### Dependencies

* None

### Validation Expectations

* Anchors resolve; no checkbox ticked; no invented numbers.

### Completion Evidence

* Diff shows additions only in those two places.

### Unresolved Items

* None

<!-- rpi:task id=P01-T01 -->
### P01-T01: AC map and reconciliation

#### Context

Research AC table gives status for each AC. Stale statements: rubric "no valid comparison" (pack 1710), open PR initial inspection (pack 1700), soak "none" versus open decision.

#### Intent

Write the 11-row table (AC, source/date/revision, evidenced component, unmet component, status, human owner). Closed status vocabulary: every row is `UNMET` overall (no criterion is accepted or ticked); the evidenced component column records what is proven (for example AC1 ADR acceptance recorded 2026-10-15, AC2 `prototype/` absent after `a7e30046`) and the unmet component column names the remaining owner, evidence or candidate-commit gap, including AC3 owner agreement on retire rows and A1-A5, AC6 candidate score and dip cause/recovery record, AC7 refresh at sign-off, AC8 external full link/gate check and a short "Dated corrections" list: rubric snapshots 47 at `fa730d63` (2026-10-15) and 48 from `b1fd9042` (2026-10-16) through `332101ed` (2026-10-20), floors false, no candidate-commit score and comparability unverified; 2026-10-21 read-only PR check shows seven open PRs (420-426) with none touching `mvp/` or `prototype/`, epics still open; CI triggers are pull request and dispatch only (last main push run 2026-10-18 `612cbed7`), so candidate CI must come from PR checks and the external gate receipt; no `v*` tag exists, BRD still 0.18.0.

#### Boundaries

* Included: overall `UNMET` for all rows with explicit evidenced and unmet components; an additive blockquote `Superseded in part by` pointer directly under the `## Other Cut-Over Gates` heading naming the new section for the open-PR and rubric statements, leaving the historical text intact.
* Excluded: ticking issue boxes; claiming candidate evidence.

#### Likely Targets

* docs/architecture/cutover-evidence-pack.md

#### Dependencies

* None

#### Validation Expectations

* Each row cites a repo path, commit or URL and date.

#### Completion Evidence

* Table present with 11 rows.

#### Unresolved Items

* None

<!-- rpi:task id=P01-T02 -->
### P01-T02: Soak evidence specification proposal

#### Context

Owner direction W3 asks for a proposed soak duration and checklist for review. The only recorded owner decision is "no minimum" (2026-10-15). No duration is invented.

#### Intent

Add a "Proposed soak evidence specification (for owner review, not started)" table with these rows, every parameter labelled `OPEN (owner)`:

* (All rows are proposals; none is an existing owner rule.) Candidate revision: full 40-character git SHA on `main`, the four workload image digests, infra/Bicep commit, BRD version; frozen for the window.
* Environment: named non-production synthetic environment in `ama`; identifiers in an external mode 0600 receipt, sanitized summary committed; no private data, no resident or staff data.
* Entry (start) conditions: AC4 and AC5 evidence for the exact SHA (PR checks, external gate receipt, deploy of those digests), real staff sign-in smoke by the authorized tenant operator (#349), approved finite cost plan; start timestamp UTC recorded by the collector.
* Window: kind (none, event-count, calendar), length, consecutive or cumulative: OPEN (owner).
* Health signal: deployed `/healthz` per path under test, plus protected API 401 canary; cadence and miss tolerance OPEN.
* Parity signal: rerun `python -m zava_forward.core.synthetic.cutover_audit` with no drift; authenticated positive-role smoke; one SQL restart-persistence check on the fictional case.
* CI signal: proposed set is the four existing workflow files `src-ci.yml`, `mvp-ci.yml`, `mvp-validation.yml`, `infra-plan.yml` (required set OPEN (owner); the pack records rulesets as warn-only per #323), green via PR checks and the external gate receipt.
* Rubric signal: scorer run on the SHA compared with the committed snapshot 48 (A30 B13 C5 D0, commit `332101ed`, 2026-10-20) as the proposed comparator, comparator basis OPEN (owner), cause and recovery expectation for any dip; floors state reported not hidden.
* Old-path signal: refresh of open PR/file scan for #113, #136, #165, #157, #149 at start and end.
* Failure and reset: any src, infra or image change to the candidate, auth bypass, SQL public access enabled, data loss, or health failure beyond tolerance stops and resets the window to a new SHA; transient single miss within the OPEN tolerance is logged only. Proposed rollback keeps `ama`, deletes nothing and follows the existing public-edge recovery baseline recorded in the pack (`Return401 / NoProxy` and the seven exact public exclusions, section Issue 344 Acceptance Audit); reset triggers are proposals, OPEN (owner).
* Escalation: immediate owner notice in #201 by the coordinator for reset-class failures; cost overrun stops collection per the approved plan.
* Cost: only inside a separately approved finite plan; the USD500 total cap expiring 2026-10-25T16:02Z and the over-cap provisional forecast mean no headroom is assumed.
* Collector: named operator or agent, OPEN; reviewer: independent of the collector, OPEN; approver: @jmservera, confirmation pending (checklist item 1).
* Evidence retention: sanitized JSON beside `cutover-azure-evidence.json`; raw receipts external.

#### Boundaries

* Included: proposal text. Excluded: executing any probe or run.

#### Likely Targets

* docs/architecture/cutover-evidence-pack.md

#### Dependencies

* P01-T01

#### Validation Expectations

* Search of the new section finds no unlabelled duration, cadence or tolerance number.

#### Completion Evidence

* Table present.

#### Unresolved Items

* All OPEN parameters are owner decisions.

<!-- rpi:task id=P01-T03 -->
### P01-T03: Pending owner decisions and checklist pointer

#### Context

Decisions needed before any soak can be defined or executed.

#### Intent

Add decision table D1 to D16 (owner @jmservera unless noted; status Pending, not decided; evidence needed an owner comment in #201). If a new owner comment on #201 appears before commit, report it in the changes record rather than applying it:

* D1 Whether a soak is required: reconcile "no minimum" (2026-10-15) with the open item in the issue body and the 2026-10-20 proposal request. Options: A none, B event-count window, C calendar window.
* D2 Window length and unit if B or C.
* D3 Consecutive versus cumulative, and reset rule scope (any src change versus deployed-artifact change only).
* D4 Probe cadence, miss tolerance and per-path scope (private, public edge, both).
* D5 Entry conditions and who authorizes the start.
* D6 Collector and independent reviewer identities (assignment, not inferred).
* D7 Finite costed plan and funding beyond the USD500 cap and 2026-10-25T16:02Z expiry (separate approval; tenant operator for D5 sign-in).
* D8 Rubric treatment: accept the candidate score comparison basis and record dip cause and recovery expectation.
* D9 A1-A5 and service-role denial gap disposition.
* D10 Confirm the cut-over approver in #201.
* D11 Archive tag and release at the BRD version current at cut-over.
* D12 Private data relocation and encrypted backup: owner-only non-sensitive attestation.
* D13 Agreement on each `prototype/` retire row and the A1-A5 placements (AC3), separate from the D9 service-role gap.
* D14 Retained `ama` resources and charges: remediation, retention or ID-scoped cleanup, never deleting `ama`.
* D15 Approve the separate single-PR post-cut-over workflow/check rename plan.
* D16 Tenant registration, real staff sign-in and feature acceptance (#349, #350) and the final go/no-go in #201.

Also add a crosswalk sentence: D1 to D16 supplement, and do not replace, the existing sign-off checklist items; each checklist item is still unchecked.

Add one unchecked checklist bullet: "Review the proposed soak evidence specification and decide D1 to D16; no soak has started."

#### Boundaries

* Included: wording only. Excluded: recording any decision as made.

#### Likely Targets

* docs/architecture/cutover-evidence-pack.md

#### Dependencies

* P01-T02

#### Validation Expectations

* Checklist boxes remain `[ ]`.

#### Completion Evidence

* Table and bullet present.

#### Unresolved Items

* D1 to D16 pending.

<!-- rpi:phase id=P02 -->
## P02: Align ADR, index and log

### Context

ADR 0006 records "no minimum soak" in two places (lines 298, 366). Index row at `docs/reference/README.md:288` summarizes the pack. Log is append-only.

### Intent

Make the contradiction discoverable and append the dated entry.

### Boundaries

* Included: ADR note, row edit, log append.
* Excluded: editing earlier log entries, other index rows, matrix history.

### Likely Targets

* docs/adrs/0006-src-layout-and-cutover.md, docs/reference/README.md, docs/reference/log.md

### Dependencies

* P01

### Validation Expectations

* Log diff additions only; links resolve.

### Completion Evidence

* Diff.

### Unresolved Items

* None

<!-- rpi:task id=P02-T01 -->
### P02-T01: ADR note, index row and log entry

#### Context

Anchor name of the new pack section: `soak-and-cut-over-evidence-preparation-2026-10-21`.

#### Intent

Append a short dated "Soak reconciliation note (2026-10-21)" at the end of the ADR Owner Answers section stating the 2026-10-15 decision is unchanged and under owner review per the 2026-10-20 direction (no change to Status or gate). Extend row 288 with a link to the new section and "soak proposal pending owner decision, no soak started". Append log entry `## [2026-10-21] query | Cut-over soak evidence preparation (Refs #201)` (type `query`, a documented log type) listing every touched file and the raised contradictions (soak decision, stale rubric statement).

#### Boundaries

* Included: three files. Excluded: ADR status or gate text change.

#### Likely Targets

* the three files above

#### Dependencies

* P01-T03

#### Validation Expectations

* Anchor link resolves.

#### Completion Evidence

* Diff and link check.

#### Unresolved Items

* None

<!-- rpi:phase id=P03 -->
## P03: Focused validation and local commit

### Context

Coordinator serializes the full gate; only focused checks run locally.

### Intent

Before editing and before each commit, run `git fetch origin main` and record `origin/main` and base SHA; locate edit points by heading, not line number; if main moved to touch the same files, record it and re-anchor. Run `git diff --check`, a Python relative-link and anchor check on changed docs, `git diff --name-only` scope check, confirm checklist boxes unchecked, record unperformed checks; commit locally.

### Boundaries

* Included: local commit with Copilot trailer under GitHub privacy email (repo-local config only).
* Excluded: push, PR, amend, merge, full gate, Docker, SQL, Azure.

### Likely Targets

* .copilot-tracking/changes/2026-10-21/cutover-soak-review-201-changes.md

### Dependencies

* P02

### Validation Expectations

* Zero broken links; clean `git status --ignored --short` after final commit.

### Completion Evidence

* Command outputs in changes record.

### Unresolved Items

* Full gate and independent assessment by coordinator.

<!-- rpi:task id=P03-T01 -->
### P03-T01: Checks, changes record and commit

#### Context

State JSON and Review are committed too, per the task.

#### Intent

Commit 1: docs plus research, plan, details, critique, changes and state. Commit 2: Review and final state (no amend). Committed tracking paths: .copilot-tracking/{research,plans,details,changes}/2026-10-21/cutover-soak-review-201-*, .copilot-tracking/reviews/plans/2026-10-21/, .copilot-tracking/reviews/logs/2026-10-21/ and .copilot-tracking/rpi-sessions/2026-10-21/ only. The branch is not publishable: the coordinator owns the full external gate and independent assessment, and any later commit, rebase or base change invalidates a receipt.

#### Boundaries

* Included: local commits. Excluded: push.

#### Likely Targets

* .copilot-tracking/** dated 2026-10-21 files

#### Dependencies

* P02-T01

#### Validation Expectations

* `git status --short --ignored` empty at exit.

#### Completion Evidence

* Final HEAD SHA.

#### Unresolved Items

* None
