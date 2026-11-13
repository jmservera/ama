---
title: "#176 C2 generator revision emission (direct-native retry) changes"
date: 2026-11-13
---

* Source: `zf_documents.py` emits `generator_revision` (own file fingerprint); `zf_document_controls.py` emits it over both files; via `provenance.source_revision` (sha256:64hex, existing convention).
* Committed fixtures untouched (verified `git diff --quiet`); their generator revision is historically unrecorded/Unknown: #176 criterion remains UNMET for them. Not regenerated (private register unavailable, never read).
* Tests (`src/importer/tests/test_document_form_fixtures.py`): fresh revision equals fingerprint, repeats byte-identical, payload/content hashes equal pre-change baseline (`logs/baseline-pre-change-hashes.txt`).
* Evidence: `logs/red-0.txt` (exit 1, 2 KeyError), `logs/final-importer.txt` (8 OK, exit 0), ruff check/format clean on touched test (pre-existing C408 in zf_documents.py untouched). First draft diff kept in `logs/original-draft-test-diff-pre-direct-native-0653.patch`.
* Not run: `src/api/tests/test_document_controls.py` (imports test_mvp, SQLite-backed; ModuleNotFoundError in `logs/consumer-api.txt`); consumers read keys by name, extra key is low risk.
* Incident: an accidental `git stash` was immediately popped; no work lost.
* Residual: generators now need src/core installed (zf_manifest.py precedent); new revision is 64-hex while other support revisions differ (stated non-goal).
