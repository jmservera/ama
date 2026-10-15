# Plan: durable erasure register

* [x] Phase 1: add `list_ids` to Local and Azure Blob document stores (paged XML listing).
* [x] Phase 2: recovery.py stores one write-once entry per erasure under `_erasures` in `store.docstore`; write entry before redaction; backend errors raise.
* [x] Phase 3: tests (blob register, ordering, crash, unreadable register); README unverified items.
* Critique (single pass): compatible findings applied: unique entry names (uuid) so same-second repeats do not 409; validate case exists before writing the entry.
