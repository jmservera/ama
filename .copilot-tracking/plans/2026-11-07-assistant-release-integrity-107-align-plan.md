# Plan: align #107 candidate onto final main

Research: [research](../research/2026-11-07-assistant-release-integrity-107-align-research.md). Details: [details](../details/2026-11-07-assistant-release-integrity-107-align-details.md).

## Decisions

* Preserve the exact test and all original artifacts; original history is not rewritten, no commit is dropped.
* Keep a backup ref of 4aa717009 before any rebase; rebase only if main moved and conflicts are trivially safe.
* Format only the added block if the configured formatter objects to it; if config excludes the file, record the invariant.
* No full gate, SQL, images, scanners, heavy lock or push. FULL publication NOT READY.

## Phases

* [x] Phase 1: bounded wait for rubric run 42361331168, fetch final base.
* [x] Phase 2: determine configured formatter scope and baseline versus candidate diagnostic.
* [x] Phase 3: backup ref, rebase onto final base, run focused checks and the 46-test selector.
* [x] Phase 4: critique once, review once, commit records, freeze.
