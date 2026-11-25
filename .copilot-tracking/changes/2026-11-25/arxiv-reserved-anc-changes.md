---
description: Archive-only fix for arXiv's reserved anc directory
ms.date: 2026-11-25
---

# RPI Changes: arXiv reserved anc directory

## Execution Status

Complete: P03 and P03-T01. No remaining active-plan marker.
The correction is validated, but no new independent Review ran.

## Completed Work

The packaging step now maps anc compilation inputs to tex-inputs within
archives and rewrites only their literal file arguments. Original source
bytes still govern the unchanged publication revision checks. Shared
offset-preserving parsing masks comments and literal environments, allowing
the rewrite to leave those contents alone. Collisions fail explicitly.

Two focused regressions cover remapping and preservation, plus collision
refusal. Existing archive assertions now reject reserved anc members.
The README explains the original defect and clean re-upload procedure.

## Validation

* Passed: 24 tests in one unittest runner (13 packaging and 11 existing
  PaperCheckerTests).
* Passed: Ruff check, isolated 100-column format check, strict mypy and
  git diff --check.
* Passed: actual 22-file archive extraction and two PDFLaTeX passes with
  shell escape disabled.
* Passed: ZIP and tar.gz member/byte equality, no root anc path, expected
  tex-inputs members, and verified SHA256SUMS.
* Passed: undoing only tex-inputs-to-anc path-prefix changes in packaged TeX
  exactly restores original source bytes. All prompt and image bytes match.
* Passed: git diff lists no modified .tex source. The read-only attachment
  was inspected but not edited.
* One test-fixture lint finding was corrected before the final passing run.
* Live arXiv processing, GitHub publication, full publication gate, hosted
  exact-head CI and independent review were not run.

Corrected ZIP SHA-256:
`a2bc3c3c6021db764e3768ac8d1aa322dc7e448d52a4c7e030c39b943f2e2d88`

Corrected tar.gz SHA-256:
`cd30ed87af04dfe45dbd2f5f87edde4b71f6470dfcec8aa85c3c8ffe266a60d3`

Current manuscript SHA-256:
`ce33c8552e95a28cb8cfcd266d3833063cf77f7dcf65ced18fcaa99358e34530`

Corrected outputs are in the conversation session's files/arxiv-fixed-anc
directory. They supersede the earlier archive layout; earlier validation
records are historical and do not establish arXiv compatibility.
No release or branch was pushed by this correction. The owner must clear
the old arXiv upload and upload one corrected archive.
