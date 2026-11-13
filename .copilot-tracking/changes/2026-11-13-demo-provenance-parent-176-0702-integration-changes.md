---
title: "#176 provenance integration changes and equivalence"
date: 2026-11-13
---

## Identity

* Frozen source input: local commit `25a7135b1b6046b960e5993e7f7333bfb7055347`. Validation head: `1ea31c689` (tree `767b0a02ecf970e4950914733d34bb7314843cf3`, parent `25a7135b1`), run in `demo-provenance-validation-176-0702`; not mutated.
* Merged main: `a17d5fe57a98e8672ffcd8d40d6bd6b8e0b15186` (docs checkpoint 1506), normal merge, no rebase or amend.
* Copied: all 14 files under `.copilot-tracking/evidence/2026-11-13-provenance-validation-176-0702/`; every index blob equals the `1ea31c689` blob. The omitted raw snapshots were not copied.

## Equivalence

* Git trees `src` (`d6a78d52e9e31ce123c0c788c6c8f6ff7cca25a1`) and `support` (`ebf79c452e9779b191619eb82d800bc577fff61b`) in this integration equal both `25a7135b1` and `1ea31c689`; main 1506 changed neither. The three product/test blobs and both legacy fixtures (`e39d618e...`, `360dc62a...`) equal `25a7135b1`.
* Therefore the validation's executable inputs (src and support generators, tests, helpers) are identical. Its results are reused only for those inputs, as measured on the frozen worktree; they are not a rerun in this tree, and `docs/` and `.copilot-tracking/` differences were not run.

## Validation results reused (from the record, qualifications kept)

* Core import resolved to the frozen worktree with helper bytes equal to Git25; 8 importer tests passed, 0 skipped; 2 generator `--help` exits 0.
* Fresh-output privacy check and JSON Store consumers passed with a negative control. One API selector passed after a first failed missing-api attempt; it reads unchanged fixtures and is not new-key proof.
* Importer test Ruff, format and mypy passed. Ad hoc support Ruff shows 32 findings against 31 at baseline, including one new E501 on the added controls revision line; C408 is unchanged. No support Ruff is configured, so this is not a passed check. The root asked the owner for one optional formatting correction; the owner was unavailable, which is not approval. The source line is not changed here and the publication disposition is the root's exact-head decision.
* The validation Review was wording-nonconformant; the corrections were not re-reviewed.

## Documentation

* Narrow candidate note in the document fixtures section of `docs/reference/research/retrofit-synthetic-data/README.md`, one clause in the `docs/reference/README.md` row, one appended log entry after both prior entries (the 1506 entries are intact).
* The capability is described as an unmerged candidate. Legacy fixtures stay unrecorded, private originals unavailable, whole #176 open, human refresh approval unchanged.

## Checks run

Merge status, blob and tree comparisons, `git diff --check` on docs, and link-target existence only. No tests, installs, gates, SQL, browser or remote action.

## Remaining publication requirements

Root exact-head assessment (including the optional E501 finding), selected-tier gate per policy, hosted CI, independent review and human approvals.
