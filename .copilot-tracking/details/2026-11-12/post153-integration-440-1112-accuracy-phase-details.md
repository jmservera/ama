<!-- markdownlint-disable-file -->
# Phase details: accuracy follow-up for the post-153 checkpoint (2026-11-12)

Task `post153-integration-440-1112-accuracy`. Evidence: the accuracy research file under .copilot-tracking/research/2026-11-12/ and raw files in the external folder `/home/azureuser/.copilot/session-state/d351ddc0-f4e6-4e5f-ae56-db0937d3ad2b/files/checkpoint-440-post153-1112-accuracy/`.

## P01: Correct the pack section

* Target: `docs/architecture/cutover-evidence-pack.md`, section "Post-153 integration checkpoint (2026-11-12, ...)" only. Edit by replacing only the named sentences; do not touch the counts, pin table or other sections.
* P01-T01: the sentence "No other public tracked file mentions the five ids." becomes a statement of boundary: the static script read `runbook.md` and web source; `git grep` over tracked files at `8bfd52729` finds the five ids in the pack, `runbook.md` and one tracked historical record `five-home-script-134-1112-research.md`; that record and its generator replay were not reproduced or read here; nothing about deployed membership or absence. Done when the old sentence is gone and the boundary text is present.
* P01-T02: the opening says the inputs were "later-merged" after "the previous checkpoint (PR 1478 ...)". Qualify: merged before the PR 1478 publication, after the tested pin `bbb1d20cc`. Append a subsection "Accuracy note (2026-11-12)" after F3 listing: C3 times; C2 counts (20 and 7; original 16 and 19 wrong; PC-007 not fully applied); C1; C4; that the original research, critique and review are preserved unchanged and carry these errors; and that counts 145/92, the pin and the partial requirement coverage are unchanged. Done when each item is present with the observed values.
* P01-T03: F1 text: remove "ARIA 1.2 prohibits naming a role-less element"; state the observed attributes and the unverified question about implicit generic role; no fetched standard, no web review, no assistive-technology observation, no conformance or confirmed defect claim; not fixed.

## P02: Log, index, verification

* P02-T01: append one entry at the end of `docs/reference/log.md`; do not alter earlier entries. Index: `docs/reference/README.md` already points to the section; leave it unchanged unless its text repeats a corrected claim (check by grep).
* P02-T02: compare `git ls-files -s` blobs of the seven originals against `original-blobs-before.txt`; `git diff --stat`; check that relative links in the diff resolve; write the changes record.

## P03: Review and commit

* One Review under `.copilot-tracking/reviews/logs/2026-11-12/`; then commit locally with `gh api user` derived local identity and the Copilot trailer. No push, PR, amend or rebase.
