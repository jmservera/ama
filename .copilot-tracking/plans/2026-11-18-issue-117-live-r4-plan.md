# Plan: EICAR detection in the local scanner (Refs #117)
1. doc_controls.py: add EICAR_SIGNATURE (standard 68-byte test string, built from parts) and return "infected" in LocalSignatureScanner.
2. src/api/tests/test_document_controls.py: tests that an upload carrying EICAR is refused and not stored; clean text still passes.
3. Run api tests, core doc tests, mypy (core, api), ruff format check. FOCUSED plus src change; no --all.
