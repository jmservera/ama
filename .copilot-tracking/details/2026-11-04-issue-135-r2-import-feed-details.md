# Details: issue 135 round 2

* `feed_failed_imports(queue, batches, owner, refusals=())`: batches are mappings of importer `BatchRecord`; only `status == "rejected"` raised, ref `batch:<id>`. Refusals carry source_name, source_sha256, reason, at; ref `file:<hash or name>`.
* The importer package is not imported by core, so the dependency rule is untouched. Nothing calls the feed yet.
* Never retries, approves or edits an import.
