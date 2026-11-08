# Issue 1231 r30 root 8010a486 propagation: plan

Research: .copilot-tracking/research/2026-11-07/issue-1231-r30-root8010-written-propagation-research.md
Details: .copilot-tracking/details/2026-11-07/issue-1231-r30-root8010-written-propagation-details.md

## Steps

* [ ] 1. Preflight identities (done before this plan) and backup ref backup/issue-1231-61f3e-pre-r30-merge.
* [ ] 2. Commit these prospective records before any merge or source edit.
* [ ] 3. Normal merge of root 8010a486 (no rebase). Resolve ranking conflicts to the child's blobs; keep root RPI records, log append (no deletions) and any non-ranking root content.
* [ ] 4. Red evidence first: add the adapted root tests (written on error, existing-retry reconfirm already green, runner unconfirmed status and exit 2, written False for existing) and run them on the child helper/runner; record failures.
* [ ] 5. Minimal source: optional written on DurabilityUnconfirmedError; _confirmed passes it and stage_retained; runner handler placed before the generic OSError handler (path-free, stage_retained in uncertainty); main maps committed_unconfirmed to exit 2; README text.
* [ ] 6. Light checks: core ranking, API wiring and Store/private cleanup, UI hosts, Config class, ruff, format, mypy; preservation proofs.
* [ ] 7. One author Review, changes record, ONE dated successor note and state (historical vs current), commit and freeze, ignored-inclusive clean.

## Boundaries

* Keep child _remove/_confirmed, .ranking-style stage names, retry/re-sync, immutable published_on, 409 path-free. No Store/schema/auth/paid/model changes. No #1258/#1259.
* No heavy checks, publication, push, PR, ticks. Historical r29 records, receipt 799026a3 and old receipts untouched.

## Follow-Up Items

* Separately admitted fresh FULL on the final heads and exact main; independent assessment; hosted and human approval.
