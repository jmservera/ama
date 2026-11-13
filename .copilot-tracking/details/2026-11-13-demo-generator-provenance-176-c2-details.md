---
title: "#176 C2 document-generator provenance details (original)"
date: 2026-11-13
---

* Env: venv `/tmp/zf176c2-venv` with `pip install -e src/core -e src/importer` (isolated, created for this task).
* Selected tests (by name, no SQLite): importer `tests.test_document_form_fixtures` (class `DocumentFormFixtureTests`) in cwd `src/importer`; a new controls test placed in `src/importer/tests/test_document_form_fixtures.py` is not appropriate (core fixture); place the controls tests in `src/core/tests/test_synthetic_determinism.py` only if it does not start SQLite, otherwise a test class in the importer file reading the core fixture by path. Chosen: importer test file, class `DocumentControlFixtureProvenanceTests`, to avoid new files and SQLite.
* Header-only update uses json.load then key insertion then `json.dump(indent=1, sort_keys=True)` plus newline, matching the generator.
