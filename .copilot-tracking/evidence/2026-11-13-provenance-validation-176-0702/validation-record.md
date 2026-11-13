---
title: "#176 provenance execution validation (0702): research, plan, critique, validation"
date: 2026-11-13
---

Frozen input `25a7135b1b6046b960e5993e7f7333bfb7055347`, branch `test/demo-provenance-validation-176-0702`. No source, test, helper, fixture, manifest or private-input change. External environment and scripts: `/home/azureuser/ext-validation/demo-provenance-validation-176-0702-0708/` (own venv, not shared). Raw logs: `../../evidence/2026-11-13-provenance-validation-176-0702/`.

## Research (existing evidence read)

* Implementation: three files in 25a7135b1 (`zf_documents.py`, `zf_document_controls.py` emit `generator_revision` via `provenance.source_revision`; importer test adds 3 tests). Prior plan/critique/Review/changes read under `.copilot-tracking/*/2026-11-13-demo-generator-provenance-176-c2-*`.
* Prior gaps carried in: ambient Core resolution unproven, API consumer module failed importing `test_mvp`, historical committed fixtures remain without `generator_revision` (criterion unmet for them).
* Inspection before running: importer tests build from a constructed in-test register and never call `load_register`; generator `--help` exits in argparse before `load_register` runs (parse_args precedes the call); the CLI defaults point at the private register and were never executed.

## Plan

1. Own venv, `pip install -e src/core` (component guide) plus pinned ruff/mypy; capture imported helper path and bytes vs Git25.
2. Run the 8 importer tests from `src/importer`.
3. Generator `--help` only.
4. Consumers: direct bounded calls to existing production code (`privacy.public_issues`, JSON `Store.add_document`) over fresh constructed outputs; existing non-SQL API selector as supplementary.
5. Existing ruff/format/mypy; verify C408 scope against baseline.

## Critique (single, final-candidate, self-applied)

* Risk: a pass on committed fixtures is not new-key proof. Disposition: consumer script uses fresh `build()` output; the API selector result is labelled unchanged-fixture only.
* Risk: ambient checkout. Disposition: venv-local interpreter, `PYTHONPATH` unset, helper path and SHA-256 compared with the Git25 blob.
* Risk: mutating the worktree. Disposition: editable install only wrote the ignored `zava_forward_*.egg-info`; `-B` used; status clean before this commit.
* Not run, by instruction: SQLite-backed `setUp`, SQL, browser, Docker, gate, private input.

## Validation results (exactly as executed)

| Check | Result |
| --- | --- |
| Install `pip install -e src/core ruff==0.17.1 mypy==2.4.0` (build prerequisite setuptools fetched by pip) | exit 0 |
| Imported helper | `/home/azureuser/source/ama-demo-wt/demo-provenance-validation-176-0702/src/core/src/zava_forward/core/synthetic/provenance.py`, sha256 `fe7294aa283bd336648698ca6c3ee7d199f9bc9dba9801af6ea1395d90d81b03`, identical to Git25 blob `f35d3577cc0eae159eb1caf62ffd76a568021f63` bytes (run from `/tmp`, venv python, no PYTHONPATH) |
| `src/importer`: `python -m unittest tests.test_document_form_fixtures -v` | Ran 8, OK, 0 skips, exit 0 |
| `zf_documents.py --help`, `zf_document_controls.py --help` | exit 0, usage only |
| Fresh outputs through `privacy.public_issues` (temp copy of public payloads, both fixtures replaced by fresh outputs carrying `generator_revision`) | baseline issues `[]`, fresh issues `[]`; negative control (label deleted) reports `row-1:missing_synthetic_label` |
| Fresh control output through `Store.add_document` (JSON Store, 120 cases) | 229 clean accepted, 131 refused, classes clean/test-marker/type-mismatch, all documents clean, exit 0 |
| API selector `test_document_controls.ScanTests.test_synthetic_stock_fixtures_scan_as_labelled` | First attempt exit 1: `No module named 'zava_forward.api'` (`06-api-selector-attempt.txt`, kept). After `pip install -e src/agents -e src/api` (exit 0): Ran 1, OK, 65 s, exit 0. Reads the unchanged committed fixture, so it is NOT new-key proof |
| `ruff check` and `ruff format --check` on the importer test (importer config) | pass, exit 0 |
| `mypy tests/test_document_form_fixtures.py` (importer config) | Success, exit 0 |
| C408 | `--isolated --select C408` fails (exit 1) at `zf_documents.py:165:24` on Git25 and at `:161:24` on baseline 472b3261a (same `dict(name=...)` expression, line shift from the added lines). One finding, pre-existing, unchanged, not fixed, not passing |
| Support generators under importer ruff config (ad hoc; no configured support lint exists) | Fail: 32 findings at Git25 vs 31 at baseline, the extra one is an E501 on the added `generator_revision` line in `zf_document_controls.py` (4 over-long lines at baseline, 5 at Git25 per Review's git inspection; the raw log lists only unchanged `zf_documents.py` lines); not fixed |

## Disclosed failed or superseded attempts (raw logs kept)

* `09-importer-lint.txt`: first mypy attempt used a wrong path (no such file, no exit line); passing mypy is the rerun in `10-c408-mypy.txt`.
* `10-c408.txt`: wrong-cwd run (E902 missing files, `fatal: not a git repository`, a false "All checks passed!" on missing files). Superseded by `10-c408-mypy.txt`; ignore its pass.
* C408 scope: only `zf_documents.py` reports C408; `zf_document_controls.py` reports none under `--isolated --select C408`.
* Install side effect: only the ignored `src/*/src/*.egg-info` directories were written; `git status` showed solely this untracked evidence directory (no `.gitignore` check logged beyond `git check-ignore` output for the core egg-info).

## Independent Review (one, read-only code-review agent)

Verdict: not fully conformant on wording only; numbers matched logs. Five findings (extra E501 file attribution, install claim, undisclosed mypy first attempt, undisclosed `10-c408.txt` failures, C408 scope) were corrected above. No re-review per one-pass rule.

## Remaining selected-tier gaps

* Committed document-form and document-control fixtures still lack `generator_revision` (historically Unknown); regeneration needs the unavailable original private register. Issue criterion stays unmet for them.
* Full API `test_document_controls` (including SQLite-backed `SqlRetentionTests`) not run, by instruction; new-key acceptance by API consumers shown only through bounded direct production calls, not the existing test files.
* No configured lint covers `support/` generators; ad hoc ruff shows pre-existing C408 plus E501 findings, one E501 added by the change.
* Complete local gate, hosted CI, human approvals and independent exact-head review of the final commit not performed; no runtime network isolation is claimed.
