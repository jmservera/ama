# Plan: sensor-review wave actual-main observation (2026-11-10, Refs #440 #109 #111)

Details: [details](../details/2026-11-10-sensor-actual-main-440-1110-details.md). Critique: [critique](critiques/2026-11-10-sensor-actual-main-440-1110-plan-critique.md). Research: [research](../research/2026-11-10-sensor-actual-main-440-1110-research.md).

## Objective

Append one dated, source-qualified sensor-integration section to `docs/architecture/cutover-evidence-pack.md`, index it in `docs/reference/README.md`, and append one entry to `docs/reference/log.md`. Docs only; focused tier.

## Tier classification

Focused documentation tier. Basis: Markdown and tracking files only; no workflow, dependency, Dockerfile, permission, schema, deployment, security control or gate change. Validation is link and diff review, input identities and seven-event witness verification; no runtime gate, `--changed`, suite, install, image, SQL, browser, cloud, model or private-data run. Hosted CI for the exact final head is a separate gate and is not claimed.

## Phases

* [x] Research: pin main, equivalence, blobs, lineage, raw evidence read (executed, Ready).
* [ ] Plan: this plan, details, critique (one author-executed critique, compatible findings applied directly).
* [ ] Implement: write the pack section, index entry, log entry; declare changes before `implement-start`.
* [ ] Review: one author-executed review created only after `implement-done`; then commit locally with noreply identity and Copilot trailer.

## Constraints

* No source, test, oracle, tool, workflow or gate edit; earlier pack sections, log entries and the PR 1405 aftercare section are untouched (PR 1405 is not on this branch and not described as merged).
* No new defect or refactoring claim without concrete evidence; none is established.
* No push, rebase, PR, issue or board change; return a frozen local candidate and the Root handoff.
* Plain ASCII, no em dashes, no bolded list prefixes, relative links.
