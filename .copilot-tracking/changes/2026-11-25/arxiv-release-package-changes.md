---
description: Implementation and local validation of arXiv packaging
ms.date: 2026-11-25
---

# RPI Changes: arXiv release package

## Execution Status

Complete local implementation: P01, P01-T01, P02 and P02-T01. No remaining
active-plan marker. Combined new/existing tests: 22 passed. Parent-owned
Review completed with no substantive local-tool findings. Remote publication
and its separate gates were not run.

## Scope

Full plan `arxiv-release-package`, P01-T01 and P02-T01. Original branch
`docs/presentation-author-voice`, as explicitly directed by the owner.
No release execution, commit or push authorized.

## Completed Work

### P01-T01: Source-only archives and opt-in release

Implemented paper-local `anc/package_arxiv.py`. It follows literal input
dependencies, preserves source bytes in deterministic ZIP/tar.gz archives,
builds the extracted ZIP with PDFLaTeX twice and emits checksums plus a local
preview. Explicit `--publish --tag` binds inputs to a clean HEAD, creates a new
remote ref, uploads to a draft and only then publishes. Existing records are
never overwritten or deleted. PC-001 is implemented through HEAD-blob checks
before and after packaging.

### P02-T01: Focused regressions and usage guidance

Added eleven focused unittest methods and the existing README's local-use
section. All eleven pass; GitHub commands are mocked. Strict mypy, Ruff lint,
Ruff format check and git diff --check pass. Initial lint/format findings were
corrected as one mechanical correction batch before Review.

The initial actual 22-file archive compiled, but the live manuscript changed
concurrently before source-byte comparison. Only main.tex differed in that
comparison; other TeX inputs also appeared modified in Git status. No edits
were reverted. The owner selected freeze-current in the clarification form,
authorizing a fresh snapshot and validation against the current files.

## Validation

Actual extracted-paper builds passed for both snapshots. The first source-byte
comparison detected concurrent changes, not a package-format failure.
After the owner paused manuscript edits, fresh ZIP and tar.gz member/byte
comparisons match all 22 current inputs: eight TeX, three TXT and eleven PNG.
Both checksums and the fresh preview's PDF header pass.

Final archive hashes:

* ZIP: `51f8722ecf48aabc70b8b4bad549d89cdf2ea0e4ab7f8e76636f9d5ed2e658f9`
* tar.gz: `b11966ac8ef400a6c604466b25550b7e25ada01d5439d9f0f4d3fd15735fe6c5`
* Current main.tex: `ce33c8552e95a28cb8cfcd266d3833063cf77f7dcf65ced18fcaa99358e34530`

Final local outputs are in the conversation session's files/arxiv-current
directory, not the repository. No manuscript file was edited by this task.
Source revisions from the simultaneous document work remain untouched.
Publication-impact classification: full tier for actual publication, because
the tool creates externally visible tags and releases. Full publication gate,
hosted exact-head CI and independent exact-head review have not run. These
are pre-publication requirements, not claimed as passed by targeted tests.

Prose detector was unavailable in the installed plugin locations; the new
usage section was reviewed manually. No actual GitHub Release was created.

## Business Alignment

None: this utility does not implement or change demonstrator BRD/PRD/ADR rules.

## Follow-Up Items

None outside delivery gates and human publication approval.
