<!-- markdownlint-disable-file -->
# Plan: #440 Quality-M2 current-main qualification record

Written 2026-11-10T01:12Z (readback `date -u`). Task `440-quality-m2-record`. Research: `.copilot-tracking/research/2026-11-10-quality-m2-record-440-research.md`. Details: `.copilot-tracking/details/2026-11-10-quality-m2-record-440-details.md`. Tier: PURE DOCS (owner direction for this task): Markdown, link and Git diff review only; no runtime gate, SQL, browser, model, provider, cloud or new data. Correction budget: default 5 total review-corrections, none spent; no reset of the #1288 E counter (E11 success, E12 and E13 unused, not consumed here).

## Objective

Record the due current-main qualification of merged Quality persistence (#1331) plus the merged #891 transport-accounting correction (#1339) in the existing `docs/architecture/cutover-evidence-pack.md`, with the unchanged-source classification of the H2 observation, a document-qualified trace, evidence classes, gaps with existing owners and a continue/fix/pivot recommendation with exact resume conditions.

## Phases

* [ ] Phase 1: Prospective records. Research, this plan, details and ONE independent critique, committed before the evidence-pack edit.
* [ ] Phase 2: Evidence-pack section appended in place (no earlier section edited), `ms.date` updated, one index paragraph in `docs/reference/README.md`, one append-only entry in `docs/reference/log.md`.
* [ ] Phase 3: Pure-docs validation: link and anchor check of the new links, ASCII and em dash scan, `git diff --stat` and `git diff` confined to the allowed paths, no secret scan hits, no src/infra/tools/.github diff.
* [ ] Phase 4: Changes record, ONE independent post-implementation Review, direct fixes only for blocking or compatible findings (counted against the 5), state record, frozen LOCAL commit, handoff file.

## Critique amendments (see plans/critiques/2026-11-10-quality-m2-record-440-plan-critique.md)

* Create changes, review and state records before link validation; validate after all review fixes.
* Allowlist check covers committed, staged, unstaged and untracked paths before freezing.
* The new section links the merged H0/H1 and H2 records directly.

## Decisions fixed before the edit

* No new evidence page; no repeat of the #1234 finance checkpoint; no coordinator-artifact or HVE behavior change (so no Major HVE criterion claim).
* Classification of H2: an observation at an identical Core/API/Agents subtree (ids recorded in research). Not a new runtime, Azure or hosted observation.
* H0 and H1 remain adverse and are never relabelled. H2 does not retroactively explain them; the cross-base comparison (a8593a7a8 versus ddeebd01) is inference only.
* Errata stated in the new section, originals unchanged: #891 IS included in `ddeebd01`; no H2 peer or bytes; 29 pass plus 1 skip; chronology.
* No draft or in-review document is treated as approved; no resident, human or model authority is inferred from synthetic release and role fixtures.
* No new issue is filed (no issue writes authorized); gaps map to existing owners. Recommendation is CONTINUE with named holds and a proposed, non-binding fix route needing owner authorization.
* Raw H2 logs stay VM-local and uncommitted; the section states that explicitly and gives hashes and values so the lasting findings read from the document and merged records.

## Acceptance (this task only)

* The section holds: source and target identities, merged PRs, exclusions (1338, 149, 1341 surface qualified), drift comparison, command identities with exits and skips, document identities, requirement trace, evidence classes, gaps and owners, recommendation, resume conditions.
* Statements about what is not proven are present for: Azure, actual model, human or resident authority, OS restart, exact-head hosted CI, assistive technology.
* Whole #440, #1288, #891, #184, #136 and Major HVE criteria stay open; no checkbox is ticked.
* Handoff written with head, tree, current-main pin, commit manifest, files, checks and limitations.
