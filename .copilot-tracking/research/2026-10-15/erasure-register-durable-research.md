# Research: durable erasure register (issue #114, PR #262)

* Finding: `recovery.register_path` wrote `erasures.jsonl` beside the digest folder, a local file lost with the container. Register was written after redaction and save, so a crash left an unrecorded erasure.
* Existing pattern: `documents.py` DocumentStore (local test backend, AzureBlobDocumentStore selected by `ZF_DOC_STORE=azure-blob`), already on `store.docstore`. The register must be outside the database, so SQL is not suitable (a restore rewinds it).
* Gap: no listing operation on DocumentStore.
* Planning readiness: Ready.
