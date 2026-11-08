<!-- markdownlint-disable-file -->
# Plan: AI and employee chat current-main stabilization checkpoint (#440)

* Date: 2026-11-08; research `.copilot-tracking/research/2026-11-08-ai-main-stabilization-440-research.md`; details `.copilot-tracking/details/2026-11-08-ai-main-stabilization-440-details.md`; critique `.copilot-tracking/plans/2026-11-08-ai-main-stabilization-440-critique.md`.
* Tier: focused, docs-only. Target `main`, branch `docs/ai-main-stabilization-440`. No push, PR, merge or remote write.

## Phases

* [x] Phase 1: Focused local reproduction in `/tmp/ai-main-440-1108` (own venv, synthetic inputs, bounded). Record actual commands, exits, counts and skips.
* [x] Phase 2: Add one dated section to `docs/architecture/cutover-evidence-pack.md` after the ranking checkpoint, following its structure (source and document identities, retained history, actual commands, traceability, owners, not run, classification and recommendation).
* [x] Phase 3: Add a log entry to `docs/reference/log.md`; update the `docs/reference/README.md` index only if an existing sentence needs a link (convention: README links dated pack sections that are material). Decide after reading it.
* [x] Phase 4: Markdown and link review, diff review, scope guard (no changes outside docs and tracking).
* [x] Phase 5: Changes record, original author Review, state; resolve GitHub identity, commit with trailer, leave clean frozen candidate.

## Constraints and decisions

* Do not edit application code, tools, workflows, agents, BRD, PRD, ADR or tests; report F1 and F2 only.
* Historical observations stay source-qualified; controlled and model-unavailable answers are not real-provider evidence; PR 1278, 1243, 1240 excluded.
* Recommendation is CONTINUE or a proposed pivot only as a recommendation; nothing approved here.
* Only run focused existing selectors; skip MSSQL, browser, Docker and full suites.

## Success criteria

* Section is unambiguous about where AI is invoked, what deterministic services do and the authority ceiling.
* Every claim cites paths and document-qualified IDs; evidence classes used consistently.
* Original adverse evidence (any selector failure, skip or refusal) kept verbatim.
