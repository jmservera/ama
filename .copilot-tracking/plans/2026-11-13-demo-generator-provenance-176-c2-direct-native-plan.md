---
title: "#176 C2 direct-native revised plan (generator-emission only)"
date: 2026-11-13
---

Supersedes, without erasing, the first-attempt plan (header stamping of committed fixtures), which the prior critique found infeasible without the private register.

Scope:
* `zf_documents.py` and `zf_document_controls.py` `build()` emit `generator_revision` = `provenance.source_revision(...)` (documents: its own file; controls: both files, since it imports `zf_documents`).
* Committed fixtures `document_form_fixtures.json` and `document_control_fixtures.json` stay byte-identical. Their generator revision is historically unrecorded (Unknown); criterion remains unmet for them.
* Tests: in `src/importer/tests/test_document_form_fixtures.py`: fresh build revision equals the source fingerprint, repeated builds byte-identical, `content_sha256`/families/cases unchanged versus the pre-change output, committed fixtures still lack the key and still load. The first draft's committed-header equality assertions are preserved in `changes/...-logs/original-draft-test-diff-pre-direct-native-0653.patch` as an unperformed future requirement.
* Validation: targeted unittest of the importer file, plus non-SQLite consumer reads; ruff on touched files. Own venv `.venv-176c2` (untracked, not committed).
* Non-goals: no 64-hex change elsewhere, no fixture regeneration, no private register.
* Docs: note in generator docstrings and the `docs/reference/log.md` entry; data dictionary left as is unless it lists headers.
