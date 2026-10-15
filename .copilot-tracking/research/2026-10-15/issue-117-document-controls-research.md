# Research: #117 document malware scanning, retention and legal hold

Disposition: executed. Planning Readiness: Ready.

## Evidence

* Issue #117 (parent #113): uploads scanned before availability; retention job lists records past trigger, needs owner approval; legal hold blocks deletion. (The prompt said to read #105; that is an unrelated AI registry issue, so #117 and #113 were used.)
* `mvp/zavaforward_mvp/documents.py`: DocumentStore (local, Azure Blob) with size/type/role checks, no scan.
* `mvp/zavaforward_mvp/store.py` add_document/get_document/read_document: the three paths that must be gated.
* ADR 0002 decision 2 and open items: scan result before a document is readable; scanner not chosen.
* PRD DH-003; addendum "Data Handling and Retention Baseline": retention from trigger, owner approval, deletion logged without content, legal hold overrides; no numeric periods in the corpus.
* ADR 0005: synthetic-demo fixtures allowed if labelled; no invented legal evidence.
* 60,000-home stock register at `support/synthetic-data/.../stock-geography`, used by `zf_documents.py`.

## Decisions

* Scanner interface: labelled local signature scanner (tests only) and a Defender for Storage tag reader (Azure deployment path, fake transport only).
* Retention periods are synthetic-demo placeholders; real periods, hold delegate, Defender enablement and job schedule are open items.
* Separate fixture generator and file to avoid conflicts with sibling issues.
