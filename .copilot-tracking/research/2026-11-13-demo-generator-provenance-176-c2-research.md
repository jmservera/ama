---
title: "#176 C2 document-generator provenance research (original)"
date: 2026-11-13
---

Scope: one initial C2 implementation. Not a renewed correction budget. Prior spent history and the original diagnostic Non-conformant Review and later qualifications (see `2026-11-13-demo-generator-determinism-176-0638-changes.md`) are preserved and unchanged. Other #176 gaps (live_readings manifest, 16-hex support revisions, C1 items) remain unmet.

## Verified facts (HEAD 472b3261a, main 33c261a63)

* `generator_revision` count is 0 in both committed fixtures and both generators (`...-logs/absence-check.txt`). No equivalent field (grep for "revision" finds nothing in either fixture).
* Headers: form fixture has is_synthetic, generator_version, seed, stock_register_rows, split_counts, form_schema, families, content_sha256. Control fixture has the same plus as_of, cases. Fixed public seed 20260901; control as_of 2026-10-15 (`AS_OF` constant).
* Generators live at `support/synthetic-data/retrofit-flow/zava-forward-year-one/generator/zf_documents.py` and `zf_document_controls.py`. The controls generator imports `zf_documents` (REGISTER, `_pick_families`, `load_register`), so its logic depends on both files.
* Existing pattern: `zava_forward.core.synthetic.provenance.source_revision(Path iterable)` returns `sha256:` + 64 hex; used by stock_fabric, sensor_backfill, scale_fixture, etc. `zf_manifest.py` already imports `zava_forward.core.synthetic` from this generator directory, so the import is an established dependency of this tool folder.
* Scope: issue #176 criterion "output manifests record seed, version and generator revision" covers generator outputs; the earlier change record names both fixtures as confirmed C2 literal gaps.
* Regeneration blocker: the generators read `stock-geography/private-north-east-stock-register.csv`, a private input that the task forbids reading. Decision: do not read it. Fixtures are updated by a header-only insertion into the committed JSON (same serialisation as the tool: indent=1, sort_keys, trailing newline), and byte-for-byte equality with a tool-format dump is proven. A full register-based regeneration is recorded as not performed (unknown: whether regenerated output equals committed; pre-existing, out of scope).

## Design

* `revision_sources()` in each generator: documents -> `(Path(__file__),)`; controls -> controls file plus `zf_documents.__file__`.
* `build()` adds `generator_revision` = `provenance.source_revision(revision_sources())`. `content_sha256` is computed over cases/families only and is unaffected.
* Tier: focused (metadata-only, no workflow/deps/infra/SQL/security).
