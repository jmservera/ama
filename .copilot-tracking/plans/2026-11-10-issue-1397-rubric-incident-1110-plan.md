<!-- markdownlint-disable-file -->
# Plan: issue 1397 incident documentation

Date: 2026-11-10. Task `issue-1397-rubric-incident-1110`. Research: `.copilot-tracking/research/2026-11-10-issue-1397-rubric-incident-1110-research.md`. Details: `.copilot-tracking/details/2026-11-10-issue-1397-rubric-incident-1110-details.md`. Critique: `.copilot-tracking/plans/2026-11-10-issue-1397-rubric-incident-1110-plan-critique.md`.

## Objective

Add one dated historical subsection to the existing incident section of `.github/rubric/README.md`, immediately after the #1383 subsection and before `## Files`, recording the diagnosis of run 42838857558 (Refs #1397, #1383). Documentation only. No change to the scorer, gate, adapter, workflow, lock, prompt, tests, configuration, shared knowledge base, index or log.

## Phases

* [ ] Phase 1: Implement the README subsection, source-bound to the research record.
* [ ] Phase 2: Pure-docs validation: Markdown and link review, source-binding check of every identity against git, Git diff scope check.
* [ ] Phase 3: One Review of the exact candidate, then commit with the repository-local noreply identity and Copilot trailer.

## Boundaries and gates

* Edit only `.github/rubric/README.md` for source; add only dated RPI records under `.copilot-tracking/`.
* The #1383 section is preserved byte for byte.
* No run, rerun, install, browser, SQL, image or cloud action; no workflow trigger; no push, pull request, GitHub write or issue closure.
* Unproven claims (recovery of the failing commit, fresh versus carried scoring, whether call 2 was refused or dropped, recurrence beyond two runs, cause of the placeholder) stay UNKNOWN or deduced and labelled.
* Validation tier: pure documentation. A blanket `rpi-checks` run is not required and is not claimed; hosted CI and independent exact-head readiness remain with Root.
