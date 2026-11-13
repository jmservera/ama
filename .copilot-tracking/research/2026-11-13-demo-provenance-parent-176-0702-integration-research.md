---
title: "#176 provenance integration (main 1506 and validation evidence) research and plan"
date: 2026-11-13
---

## Research (disposition: executed)

* Main `a17d5fe57a98e8672ffcd8d40d6bd6b8e0b15186` differs from main33 outside `docs/` and `.copilot-tracking/` only in `.github/rubric/scores/latest.json`, which the base already carried. It does not touch `src/` or `support/`.
* Validation commit `1ea31c689` (parent `25a7135b1`) adds only the folder `.copilot-tracking/evidence/2026-11-13-provenance-validation-176-0702/` (14 files).
* Target docs: the document fixtures section of the retrofit synthetic-data README and its row in the reference index.
* Planning Readiness: Ready.

## Plan

* [x] Merge pinned main normally; resolve only `docs/reference/log.md` (auto-merge, no conflict).
* [x] Copy the 14 evidence blobs from `1ea31c689` as exact blobs; no merge of its ancestry.
* [x] Add a narrow candidate-capability note and one index-row clause; append one log entry.
* [x] Verify whole `src` and `support` trees equal `25a7135b1` and `1ea31c689`; both legacy fixtures equal `25a7135b1`.
* [x] Diff check and link review only; no runtime run.
