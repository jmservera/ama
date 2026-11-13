---
title: "#176 provenance publication parent changes and manifest"
date: 2026-11-13
---

## Adoption and equivalence

* Source input: frozen LOCAL commit `25a7135b1b6046b960e5993e7f7333bfb7055347`. It was never published; this parent does not claim it was, and the parent tree does not equal the child tree (two snapshots omitted, `docs/reference/log.md` extended).
* The three source/test blobs in this parent equal the child's blobs exactly. No source fix, schema, behavior or provenance-claim change. Source equivalence here is a blob comparison, not a new runtime result.
* New capability emits `generator_revision` only for newly constructed outputs. Legacy fixtures stay unchanged and unrecorded, original private inputs are absent, and whole #176 remains open.
* The original failed first-wrapper route, the stash incident, the non-conformant 0638 diagnostic Review and the source implementation Review are carried byte-unchanged in the copied records and are not upgraded.

## Omitted duplicates (not deletion authorization, not an archive assertion)

| Original child path (untouched, still present) | Child blob | Public main33 path | Main33 blob | SHA-256 | Bytes |
| --- | --- | --- | --- | --- | --- |
| `.copilot-tracking/changes/2026-11-13-demo-generator-provenance-176-c2-logs/before-document_form_fixtures.json` | `e39d618e788de65a32503d226f6ce8f8f76d2e51` | `src/importer/evals/document_form_fixtures.json` | `e39d618e788de65a32503d226f6ce8f8f76d2e51` | `c96bcf395f1720f34e775261498afe03d0ecf5f683f50e8fb5d3d33815e231d1` | 484,017 |
| `.copilot-tracking/changes/2026-11-13-demo-generator-provenance-176-c2-logs/before-document_control_fixtures.json` | `360dc62a2dad9ce95d8cb7014dad0c933956469e` | `src/core/evals/document_control_fixtures.json` | `360dc62a2dad9ce95d8cb7014dad0c933956469e` | `08b8c2dea2eb820136c8a78785aeb96764d015e6312f4441df0ad5cc1bcf7cdb` | 72,189 |

Restoration pointer: `git show 25a7135b1b6046b960e5993e7f7333bfb7055347:<child path>` in the untouched child worktree `demo-document-provenance-176-0649` (branch `fix/demo-document-provenance-176-0649`), or `git show 33c261a63:<public path>`; both return identical bytes. The child's untracked `.venv-176c2` is not published and is untouched.

## Selected files (34), copied as exact child blobs

| Path | Blob |
| --- | --- |
| `src/importer/tests/test_document_form_fixtures.py` | `dca1aad7a887b9860526d20b69ba6716feb4feb0` |
| `support/synthetic-data/retrofit-flow/zava-forward-year-one/generator/zf_document_controls.py` | `8f5a8df3808a72279be759ac35d2db8ba90107cc` |
| `support/synthetic-data/retrofit-flow/zava-forward-year-one/generator/zf_documents.py` | `2f8681743c95750ce39648728473fb48b4e0220f` |
| `docs/reference/log.md` (child blob; this parent then appends one entry) | `cd310e6c299dcbe3ed07af400dda7d106790c59c` |
| `.copilot-tracking/changes/2026-11-13-demo-generator-determinism-176-0638-changes.md` | `0a14e617e5f9aeca201289e4ff5f2752ce652661` |
| `.copilot-tracking/changes/2026-11-13-demo-generator-provenance-176-c2-changes.md` | `27da56034d8c983ef6260d9fd1bafdd909914f40` |
| `.copilot-tracking/changes/2026-11-13-demo-generator-provenance-176-c2-logs/absence-check.txt` | `9307035a930ed51f1988b0e59480e338f6a1c460` |
| `.copilot-tracking/changes/2026-11-13-demo-generator-provenance-176-c2-logs/baseline-pre-change-hashes.txt` | `ec87fe01e9f1a280bcf404c0a1c464501071c290` |
| `.copilot-tracking/changes/2026-11-13-demo-generator-provenance-176-c2-logs/before-sha256.txt` | `88ccc14e3f19e9784f90a33f4bc7f8a5201f4768` |
| `.copilot-tracking/changes/2026-11-13-demo-generator-provenance-176-c2-logs/consumer-api.txt` | `68d23b89dc41b3e46412232b672394559355ddeb` |
| `.copilot-tracking/changes/2026-11-13-demo-generator-provenance-176-c2-logs/final-importer.txt` | `55de9106ca4e9b4ecdf228f6dfdb91d39b1f4645` |
| `.copilot-tracking/changes/2026-11-13-demo-generator-provenance-176-c2-logs/lint.txt` | `a952944938a7a03cf761e315dc0b93c711626309` |
| `.copilot-tracking/changes/2026-11-13-demo-generator-provenance-176-c2-logs/original-draft-test-diff-pre-direct-native-0653.patch` | `236db27f743dfbb6b4182a2133934d8d832d8289` |
| `.copilot-tracking/changes/2026-11-13-demo-generator-provenance-176-c2-logs/red-0.txt` | `6db4e8a756b8f3a2fd3f32924cd58c35a5910d53` |
| `.copilot-tracking/changes/2026-11-13-demo-generator-provenance-176-c2-logs/source-identity.txt` | `c893459d437adb75b7a1455c49b6eac3137b1ce7` |
| `.copilot-tracking/changes/logs/2026-11-13-demo-generator-determinism-176-0638/c2-gap-observation.txt` | `ca8ade278672547f2ea260f5756caa78841a928c` |
| `.copilot-tracking/changes/logs/2026-11-13-demo-generator-determinism-176-0638/exits.txt` | `3924888492cb5f30581d94967c77bbef0d76df4f` |
| `.copilot-tracking/changes/logs/2026-11-13-demo-generator-determinism-176-0638/t1.err` | `79b1d67429c59a3866a0744a4b4ee19278ae9ffd` |
| `.copilot-tracking/changes/logs/2026-11-13-demo-generator-determinism-176-0638/t2.err` | `3903869d035b82947d58f5046f4ebcc47e21539a` |
| `.copilot-tracking/changes/logs/2026-11-13-demo-generator-determinism-176-0638/t3.err` | `4b4cf87e9f7c434a7f047a9c39a2d716c06d6043` |
| `.copilot-tracking/changes/logs/2026-11-13-demo-generator-determinism-176-0638/t4.err` | `18e9eb2e0ef18a744e01941aafa7937abd298641` |
| `.copilot-tracking/changes/logs/2026-11-13-demo-generator-determinism-176-0638/t5.err` | `fdb3406d0b74a3c0c54142ed975e5eadf572f77a` |
| `.copilot-tracking/changes/logs/2026-11-13-demo-generator-determinism-176-0638/t6.out` | `0b052415d71122308c8a1b53f9019799a3242179` |
| `.copilot-tracking/details/2026-11-13-demo-generator-provenance-176-c2-details.md` | `c34d59d24e20e623577e73739937333a80adcf3f` |
| `.copilot-tracking/plans/2026-11-13-demo-generator-determinism-176-0638-plan.md` | `d15b24fabba80f1df5bdf95f4f744b095b38732f` |
| `.copilot-tracking/plans/2026-11-13-demo-generator-provenance-176-c2-critique.md` | `fb8bdee884146b384bf74a273b566140d80e87ac` |
| `.copilot-tracking/plans/2026-11-13-demo-generator-provenance-176-c2-direct-native-critique.md` | `478568fc24ef30115c74c0ffe0fc19edc7a0438b` |
| `.copilot-tracking/plans/2026-11-13-demo-generator-provenance-176-c2-direct-native-plan.md` | `6e334da46f624e6124a93116f3317b94163ab7e9` |
| `.copilot-tracking/plans/2026-11-13-demo-generator-provenance-176-c2-plan.md` | `35ebd1b14c9152d9e0b06a9832cb57a439e71dcd` |
| `.copilot-tracking/research/2026-11-13-demo-generator-determinism-176-0638-research.md` | `8734298934f8d2117531766917566e265c24cad8` |
| `.copilot-tracking/research/2026-11-13-demo-generator-provenance-176-c2-research.md` | `903b0ba74accf3fdf1015dfd09c41c7e1479a71c` |
| `.copilot-tracking/reviews/2026-11-13-demo-generator-determinism-176-0638-review.md` | `ca4d4c6348528a2a90ba14c44789dd268c4b843f` |
| `.copilot-tracking/reviews/2026-11-13-demo-generator-provenance-176-c2-review.md` | `11d120be66210938889399bddd017facced22b55` |
| `.copilot-tracking/rpi-sessions/2026-11-13/demo-generator-provenance-176-c2-state.json` | `311fa57e8030565e071509c4b6536345f1d5e777` |

## Review qualifications carried forward

* 0638 diagnostic Review: original outcome non-conformant (documentation accuracy), preserved.
* C2 source Review: Conformant with minor notes (baseline hashes evidenced only by logs; generators need `src/core` installed; API consumer test not run because the SQLite-backed `test_mvp` import was out of bounds). Committed fixtures are not regenerated.

## Ordering and conflict

Docs checkpoint PR1506 also appends `docs/reference/log.md` and merged after this base. This parent does not refresh or rebase. On explicit later reconciliation keep both entries.

## Pending before publication (root)

* Frozen-source validation worker results: imported-Core identity and fresh non-SQL consumer proof, not duplicated here.
* Base refresh and exact-head independent assessment, hosted CI and human approval; selected-tier local gate per the repository policy. None run here.
* No unit, gate, SQL, browser, install or remote action was performed in this packaging; only `git diff --check` style hygiene (the preserved `.patch` record has trailing whitespace by design) and blob comparisons.
