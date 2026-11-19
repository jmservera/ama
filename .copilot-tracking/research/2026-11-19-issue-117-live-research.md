# Issue 117 live research (2026-11-19)

Task: issue-117-live. Disposition: executed. Planning Readiness: Ready (evidence note only).

* One unticked criterion: "Uploads are scanned before availability".
* Source already implements it: `Store.add_document` stores the blob, calls `scan_new_document`, deletes the blob and refuses on infected or mismatch, and `is_available_case_document`/`require_clean` hide any document whose scan is not clean (fail closed on missing or malformed scan).
* Existing tests cover local EICAR refusal, pending Defender scan blocking until clean, and rescan. No source gap exists for the demo.
* Real malware engine (Defender for Storage) is a subscription-level change; outside "no production changes".
