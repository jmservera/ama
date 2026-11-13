---
title: "#176 C2 document-generator provenance plan (original)"
date: 2026-11-13
---

Details: `../details/2026-11-13-demo-generator-provenance-176-c2-details.md`.

1. Failing-first tests (before source edits), run and logged:
   * importer `tests.test_document_form_fixtures`: new test asserting `build(...)["generator_revision"] == provenance.source_revision([zf_documents.py])`, stable across two builds, header-only (content_sha256 unchanged), and committed fixture equals that revision.
   * core (or importer) test for controls: same for `zf_document_controls.build` over a constructed register, including a missing-control replay: reverting the key is detected by the committed-fixture check.
2. Source edit: add `revision_sources()` and the `generator_revision` key to both generators.
3. Header-only update of the two committed fixtures; compare before/after JSON excluding `generator_revision` for equality; confirm content_sha256 values unchanged.
4. Run selected tests by name, ruff/mypy on changed test files where configured.
5. Independent Review (exactly one), then commit with noreply email. No push, PR, issue write.

Non-goals: 64-hex upgrade of support revisions, version policy, live_readings, #184, fixture content changes, full gate.

Rollback: revert the commit.
