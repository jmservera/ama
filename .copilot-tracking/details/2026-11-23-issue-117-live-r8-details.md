# Details, issue 117, 2026-11-23

Phase 1 cases, all with a fake transport on `AzureBlobDocumentStore("https://synthetic.invalid", "docs", sas="SYN", transport=fake)`:

* Tag XML with the Defender key returns the mapping, and the scanner returns `clean` for "No threats found" and `infected` for "Malicious".
* HTTP 403/404 from the tag read makes the scanner return `pending` (fail closed).
* Non-XML body makes the scanner return `pending`.
* `open_scanner(local_store, {"ZF_SCANNER": "defender"})` and `{"ZF_SCANNER": "bogus"}` raise `ValueError`.
