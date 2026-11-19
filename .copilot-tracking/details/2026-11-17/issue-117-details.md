# Plan: issue 117

1. Add `docs/design/document-scan-retention-legal-hold.md` (design, labelled proposals vs built, owner decisions).
2. Add regression test `tools/test_document_controls_design.py`: doc exists with required sections and its quoted constants match `doc_controls.py` (drift guard).
3. Link from `docs/reference/README.md` index and log; run the test, targeted core test, ruff format check.
Critique: single pass, self-applied. Tier FOCUSED (docs plus offline tool test; no SQL/infra/security change).
