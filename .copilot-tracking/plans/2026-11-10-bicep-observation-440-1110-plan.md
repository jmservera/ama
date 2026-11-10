<!-- markdownlint-disable-file -->
# Plan: Bicep public-simulation current-main observation (#440, 2026-11-10)

Research: [research](../research/2026-11-10-bicep-observation-440-1110-research.md). Details: [details](../details/2026-11-10-bicep-observation-440-1110-details.md). Critique: [critique](critiques/2026-11-10-bicep-observation-440-1110-plan-critique.md).

## Objective

Append one dated, scoped, draft, local-only section to `docs/architecture/cutover-evidence-pack.md`, one index paragraph to `docs/reference/README.md` and one append-only entry to `docs/reference/log.md` for PR 1380 on `main` `0a6dc0b3f`. Documentation only: no source change, no check run, no new issue, no push. The NomUX section for `65c2ab9d9` stays unchanged and historical.

## Phases

* [ ] Phase 1: pack section (identities, evidence classes, consumed Root evidence, Bicep contract trace, findings and owners, gates, recommendation, limits).
* [ ] Phase 2: index paragraph and log entry, append only.
* [ ] Phase 3: review, commit, remaining witness events and `verify`.

## Constraints

* No command is claimed on `0a6dc0b3f`; observations are source-qualified local runs on `b9bae9f2` plus tree-id equivalence for the pin; Azure observed none; no live SQL, auth, resident or model acceptance.
* No approval of draft, in-review or proposed documents; whole #136, #1288 and #440 unmet; no #132 or #133 budget; no requirement relaxation.
* Excluded: #89 aftercare parent and #133 as main content (local candidate named only), held #132 and contractor identities, #1384 and #1388 fixes, old C6, the CSV-learning record.
* Process: separate preflight call returning 0 before every marker; jq state updates; patch tools for docs.

## Amendments from the single critique (applied directly)

* B1 PR-head 19 checks are metadata, not a result on the merge commit.
* B2 the two lock-busy image attempts and the old `d6d6` image are stated as adverse or non-proof.
* B3 the three baseline policy mypy errors are unwaived; no all-infra typing claim.
* B4 the image id is the manifest identity, not the config digest.
* B5 restart with a retained valid key and store does not revoke seals; replacement or loss does; no cross-restart seal runtime test is claimed.
* B6 the local #89 candidate is not main and the NomUX gate stays separate from the Bicep wave gate.
