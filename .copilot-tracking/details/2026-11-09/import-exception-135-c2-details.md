---
title: Issue 135 C2 phase details
description: Design details for the C2 corrections; the shared-hook contract is unchanged
ms.date: 2026-11-09
---

* Shared-hook contract: unchanged from `import-exception-135-details.md` (Contract, items 1 to 5), still paused under #132 serialisation.

## F1 and F2

* `mapping.preview_bytes(source_name, data, structure)` hashes, scans, reads and previews the given bytes; `preview_file` keeps its size and change checks and delegates.
* `_capture(path)`: stat before; over the limit gives a hashless refusal; read at most limit plus one byte; stat after; a changed stat gives a hashless "source changed" refusal; otherwise the digest is of the bytes actually read and those bytes are previewed. No second read exists.
* Identity: digest known gives `file:<sha256>`. Otherwise `source:src-<hash of resolved path, dev, ino, size, mtime_ns>`, or `source:attempt-<random>` when stat or read fails. The source name column keeps the basename.
* Adapter: a hashless refusal reaches the feed with an empty digest and `source_name` of `<basename> (unverified source <identity>)`, so feed refs stay distinct; the queue item shows no digest. `Routing.structures` keys use the feed ref.

## F3

* `stage` and `exceptions`: connect inside the try, catch `sqlite3.Error`, close only an opened connection, print one concise stderr line, return 2, no refusal or success line. Schema detection uses `sqlite_master`, not error text. Viewer stays `mode=ro`.

## Tests

* Different directories same basename (oversized and unreadable); replaced oversized file; same-state resubmission dedupes; equal-content two names still one row.
* Replacement between failure and fallback: patch the preview to fail after the read and replace the file; the refusal carries the original snapshot digest, never the replacement's; source-changed path is hashless.
* Feed distinctness through `route`: two hashless items, digest None.
* CLI: connection failure and write failure for stage (exit 2, empty stdout, no traceback), viewer on a non-database file and on a failing connection.
