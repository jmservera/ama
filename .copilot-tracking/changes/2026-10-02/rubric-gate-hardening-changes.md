<!-- markdownlint-disable-file -->

# Plan and Changes: rubric-gate-hardening

* Task ID: 2026-10-02-rubric-gate-hardening (child of 2026-10-02-rubric-gate-context-artifact)
* Evidence: .copilot-tracking/reviews/2026-10-02/rubric-score-gate-review.md (RV-005, RV-006, RV-009, RV-010); .copilot-tracking/reviews/2026-10-02/rubric-gate-change-detection-review.md (RG-002, RG-009, RG-010)

## Plan

* [x] RV-005 `clean_text` neutralises links, images, URLs, mentions, `#123` references and control characters, idempotently; `sanitize` adds table escaping; latest.json stores cleaned rationale and evidence; prompt marks baseline rationale and evidence as untrusted data.
* [x] RV-006 `evidence_path` normalises backslashes, workspace prefix, leading slash, `#L` and `:L` anchors and `normpath`.
* [x] RV-009 gate checkout uses `persist-credentials: false`; the token is passed only to the push command. Fail-closed when scripts are missing on `main` outside setup: not changed (the loader already fails when the PR also lacks them; recorded as accepted).
* [x] RV-010 (a) conclusion comment only when scoring was due and the gate job was skipped; (b) `decide` failure sets `rubric/score` failure; (c) distinct description for push failure; (d) sticky comment filtered by `github-actions[bot]`; (e) skip path dismisses prior bot REQUEST_CHANGES reviews (`rubric_prepare` gains `pull-requests: write`).
* [x] RG-002 non-PR range uses the scores commit's first parent when the tip itself wrote the scores.
* [x] RG-009 git output decoded with `surrogateescape`; `UnicodeDecodeError` handled in both scripts.
* [x] RG-010 content diff excludes removed files; a `--stat` section lists them first.
* [x] RV-008 remainder: PPTX extraction skipped when the uncompressed size exceeds 200 MB.
* Critique: not dispatched (each item restates a reviewed fix).

## Validation

* 47 passed, 1 skipped (symlink), minimal pytest stub. New tests: link cleaning idempotence, six evidence path variants, tip-writes-scores deletion on push, removed-file diff stat.
* `gh aw compile rubric-score`: 0 warnings.
* Not yet run on GitHub.
