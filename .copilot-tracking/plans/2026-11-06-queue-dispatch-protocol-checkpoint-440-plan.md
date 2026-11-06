---
title: Queue dispatch protocol checkpoint 440 plan
description: Plan for the fourteenth #440 checkpoint on the proposed #144 background-dispatch safeguards
ms.date: 2026-11-06
---

## Scope and tier

Task `queue-dispatch-protocol-checkpoint-440`. Research: `.copilot-tracking/research/2026-11-06-queue-dispatch-protocol-checkpoint-440-research.md` (written before this plan). Details follow in a separate file. FOCUSED tier: documentation and evidence only. Future #144 code stays FULL. No source, test, config, Bicep, role or secret edit. No push, PR, issue write, tick, SQL, browser, heavy lock or model work.

Canonical edits (all after the Research, Plan and Details commit): one additive "Fourteenth stabilization checkpoint" section at the end of `docs/architecture/cutover-evidence-pack.md`, one sentence in the existing `docs/reference/README.md` cutover-pack paragraph, one append-only entry in `docs/reference/log.md`, plus this task's Changes, Review and state.

## Phases

* [ ] P01 Create Research, Plan, Details; commit them as the original prospective evidence before any canonical edit.
  * [ ] P01-T01 Research written. (done before this file exists; verified by file timestamps)
  * [ ] P01-T02 Plan written (this file), then Details.
  * [ ] P01-T03 Resolve `gh api user`, set repo-local email, commit only these three artifacts.
* [ ] P02 Write the fourteenth pack section: pins, source-versus-main distinction, document qualification, traceability table, safeguard trace, outcome table, evidence classification, design gaps, owner decisions, recommendation, resume conditions, gates.
* [ ] P03 README sentence and log append, both preserving older text.
* [ ] P04 Focused checks run alone: fetch and pin guard, `git diff --check`, ASCII and em dash scan on added lines, relative links and the unchanged older anchors, append-only log check (old lines unchanged), JSON parse of the state, ignored-inclusive status.
* [ ] P05 Changes and state records after the checks; then a later separate author Review; final commit.

## Decisions

* Recommendation target: FIX, implementation held for unresolved contract decisions. Not continue-unconditionally, not feature acceptance, not pivot. The owner-approved background-processing goal stays in force and is not re-asked.
* Code readiness is separated from demo and operational acceptance. An invariant under which bounded implementation could proceed independently of the operator clearing workflow: with the permit protocol, no worker path calls the provider without a permit, no unknown outcome is auto-retried, and `liability-unknown` keeps the ledger fail-closed. The operator clearing workflow can follow without weakening that invariant. This is stated as a condition for the coordinator and owner, not an approval of a new authority.
* The candidate's ADR and requirement anchors are rechecked and corrected in the pack text, not repeated. ADR 0002 and ADR 0001 are Proposed; ADR 0003 decision 1 tension is recorded unresolved.
* Evidence classes only: local observed, Azure observed, implemented-unverified, deferred, blocked, unknown. Coordinator-relayed observations are `unknown` for this author with attribution in the source column. Candidate design is `implemented-unverified` only where code exists (queue slice) and `deferred` where only a draft exists.

## Critique (one pass, no subagent, adverse findings kept)

1. Risk: reporting the r8 gaps as defects. Mitigation: label them "design gaps, no test exists"; claim no reproduction.
2. Risk: repeating the candidate's unsupported ADR 0002 decision 6 mapping. Mitigation: use the checked mapping and state the correction.
3. Risk: labelling candidate-only code as main. Mitigation: show the symbol-count comparison and say main lacks the worker route and `publish_pending`.
4. Risk: `feat/infra-hosting-integration-136` was not found on the remote. Mitigation: record the 404 and call the brief's statement supplied; do not claim the parent equals main.
5. Risk: over-claiming the 40 s analysis. Mitigation: state it as a static reading of ledger lines; no run.
6. Risk: implying owner authority for the second route or an operator. Mitigation: both stay open questions to the coordinator and owner.
7. Not applied: a separate critique worker. The change is documentation-only; this is one inline pass, recorded as such.

## Checks planned

* Fresh `git fetch`; compare governance, main and the candidate HEAD/tree to the pins.
* `git diff --check`; non-ASCII and em dash scan of added lines.
* Anchors: every older `## ... checkpoint` heading in the pack unchanged; the new heading unique; README link anchor matches the heading.
* Log: `git diff` shows additions only for `docs/reference/log.md`.
* `python3 -m json.tool` on the new state file.
* `git status --short --ignored` empty after commit.
* No test suite, because no executable file changes.

## Resume conditions (to be stated in the pack)

1. A corrected implementation-ready prospective #144 design that resolves the gaps (transaction composition, clocks, attempt state and retry, lost response, late result).
2. A role-code authority decision on the second exact AgentsWorker route (no live grant).
3. A safe unknown-liability and operator clearing disposition (no invented Finance approver, no forgiving liability, no invented usage, no budget reset, no silent retry).
4. Coordinator consumption of this checkpoint after independent exact-head assessment.
5. Original #144 tests-first implementation, a new FULL gate, and current independent review before any publication or enablement.
