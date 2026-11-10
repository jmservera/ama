# Issue 1231 r32 root 9dad2aba propagation: plan

Research: .copilot-tracking/research/2026-11-07/issue-1231-r32-root9dad-propagation-research.md
Details: .copilot-tracking/details/2026-11-07/issue-1231-r32-root9dad-propagation-details.md

## Steps

* [ ] 1. Backup ref backup/issue-1231-c18-pre-r32-merge at c18f45f2.
* [ ] 2. Commit these prospective records before the merge.
* [ ] 3. Normal merge of exact 9dad2aba; ranking source and tests resolve to the child blobs; adopt root checker, tests, manifest, RPI and log.
* [ ] 4. Prove preservation: ranking blobs equal c18f45f2, non-ranking source equals root, log has 0 deletions, no existing tracking path changed (root state-file removals are not adopted if the merge shows them), ancestry.
* [ ] 5. Light checks: core ranking, API wiring, live-default, register screens, Config, ruff, format, mypy, source provenance.
* [ ] 6. Changes, one author Review, state, commit, freeze.

## Boundaries

No browser/SQL/Docker/scan/--all/--changed, no push/PR, no main merge, no old-receipt mutation.

## Follow-Up Items

Coordinator: rebaseline on the eventual main, fresh FULL, independent assessment, hosted and human approval.
