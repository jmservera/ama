<!-- markdownlint-disable-file -->
# Plan: PR 1295 C4 current-main source freshness (2026-11-09)

* Task: `pr-1295-c4-current-main-freshness`; research: [.copilot-tracking/research/2026-11-09/pr-1295-c4-current-main-freshness-research.md](../../research/2026-11-09/pr-1295-c4-current-main-freshness-research.md); details: [.copilot-tracking/details/2026-11-09/pr-1295-c4-current-main-freshness-phase-details.md](../../details/2026-11-09/pr-1295-c4-current-main-freshness-phase-details.md)
* Start: HEAD `5c13be8029216613a5652f48e9d9fb7a69ed65ff`; owner remote `0bcf55da1` and ancestor `292d0091a` preserved; pinned target `23e944c1fccf0c4578e7beb0740ddd55c3f935b2` merged normally (no rebase, force or push).
* Test tier: owner-selected demo-targeted checks. No `rpi-checks --all`, no private `ZF_DATA`, no global installs. Correction budget: cycle 4 of 5 (C1 to C3 retained; one remains).

## Scope

* Integrate the pinned current main, preserving both append-only histories if a real conflict appears.
* Run the bounded architecture `build-architecture.mjs --check`, `update-architecture.mjs --check` and resident journey `--check`, node architecture and geometry tests, and `Test-SourceHashes` after the merge.
* Refresh only metadata, derivatives, catalog or receipt entries proven stale by those checks (known candidates: `sensor_consumer.py` anchor 196 to 219, `sensor_analysis_store.py` 19 to 21, whole-file hashes of the five bound IoT sources, `text-equivalent.md` locators).
* If a references-only refresh is claimed, prove structure, text, geometry and PNG invariance by comparison; no automatic rebuild or render of the 55 slides when no visual or package input changed.
* Document the current-versus-baseline distinction only outside protected material.
* Excluded: protected QX manifest sentence, runbook numbers, protected financial bytes, any new permission, unrelated documentation or style overhaul, live Azure, model, native, assistive technology, notch, rehearsal, human, professional and financial approvals.

## Phases

* [ ] Phase 1: Integrate pinned main
  * Ordinary `--no-ff` merge of `23e944c1`; record conflicts, if any, and how both intents are preserved.
* [ ] Phase 2: Bounded freshness checks
  * Run generator `--check`, locator and hash checks; record every failure verbatim.
* [ ] Phase 3: Refresh proven-stale outputs only
  * Regenerate only what failed; compare against the pre-refresh tree for structure, text, geometry and PNG invariance; decide on deck inputs from the comparison.
* [ ] Phase 4: Documentation and records
  * Qualified doc edits only where stale; KB index and log entry appended; changes record; state JSON.
* [ ] Phase 5: Targeted validation
  * Re-run the bounded checks to green; Python tests for the main-changed IoT sources only if a source or test in scope changed locally (none expected).
* [ ] Phase 6: Review and freeze
  * One authored review, local commit with trailer, clean tree. No push.

## Acceptance

* Every generator `--check`, locator and hash check passes on the merged tree; each refreshed file is justified by a prior failing check; invariance claims have actual comparisons; C3 contracts are unchanged if any deck input is untouched; all failures retained.

## Stop conditions

* A deck, visual or protected input must change (freeze and name the owner decision); a conflict that cannot preserve both histories; a check failing for a cause not explained by main source changes.
