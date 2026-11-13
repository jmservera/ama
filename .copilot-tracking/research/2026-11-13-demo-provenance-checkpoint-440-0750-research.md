<!-- markdownlint-disable-file -->
# Research: metadata-provenance checkpoint after PR 1507 (Refs #440, #176)

Date 2026-11-13. Native single-agent loop. Research disposition: executed (bounded). Planning Readiness: Ready.

## Identities read in this worktree (not inferred)

* Worktree HEAD equals `origin/main` equals `5cedff3f468b5f8d56c86107f791e0311765b5cd` (subject "docs(demo): package #176 provenance source child compactly (Refs #176) (#1507)"); parent `a17d5fe57a98e8672ffcd8d40d6bd6b8e0b15186`.
* Main tree `425ba043788ca6e51ad884d51f840183ceb3465f` equals the tree of `294da8ee0129576a50020c10adba9b86d4cd496e` (`git rev-parse <sha>^{tree}`).
* `src` tree `d6a78d52e9e3`, `support` tree `ebf79c452e97`, `tools` tree `432a4e8f7d74` are identical at main `5cedff3f4` and local validation commit `1ea31c689`.
* `gh pr view 1507`: MERGED 2026-11-13T07:49:44Z, base main, head `294da8ee0129`, merge commit `5cedff3f4`, no closing issue references.
* #440 and #176 OPEN. #176 criterion "Output manifests record seed, version and generator revision" is unticked.

## Evidence read

* Merged diff names: two support generators, importer test, validation evidence, original RPI records, KB index/log row.
* `.copilot-tracking/evidence/2026-11-13-provenance-validation-176-0702/validation-record.md` (14 blobs, validated at source `25a7135b1`, commit `1ea31c689`).
* External root assessment `assessment-176-publication-0726.md` and independent `review-176-final-294da8-0719/specialist-return.md` (approve_with_comments, 0 blocker/major, 5 minor, 5 note).
* Public PR comments 6846951285 and 6846951730.
* Existing pack tail (post-1504 checkpoint and clarification) for section style; #440 criteria (checkpoint records covered issues, PRs, main SHA, scoped breadth, continue/fix/pivot).

## Open-issue owner check

Open issue search by title for provenance, fingerprint, revision and refresh finds only #176 (the existing owner) and the unrelated #144. No new issue is justified.

## Gaps and limits

* No runtime was executed in this task; validation results are historical, source-qualified.
* Deployed build identity, Core `source_revision` in any live environment and private-input refresh are unobserved.
