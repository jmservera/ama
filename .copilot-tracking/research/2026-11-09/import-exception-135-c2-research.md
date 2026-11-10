---
title: Issue 135 C2 import identity research
description: Corrective research for three Medium findings from the independent Functional review of d94b14dd
ms.date: 2026-11-09
---

* Correction C2 of five total (cycle 1 was lint and type fixes). Research recorded 2026-11-09T22:46Z (actual), disposition `executed`. Prior research, plan, critique, changes and Review artifacts and the independent review outputs are preserved unchanged.
* Frozen old head `d94b14ddac3e5234a519f149fe6a8abb575c44f6`, tree `29ce3cc2e936570215f6a81004049ad1e07e1bf3`, base `a04668ae9`.
* Inputs: coordinator `independent-135-import-1109/functional-findings.json` (verdict approve_with_comments, three Medium), `metadata.json`, `read-ledger.json`; code at the old head. Coordinator disposition: fix all three.

## Findings confirmed in code

| Id | Cause | Evidence |
| --- | --- | --- |
| F1 | Ledger ref is `file:{sha or basename}`. Oversized, unreadable and unstable files have no digest, so different directories or a replaced file with the same basename return the first row; the unchanged core feed does the same for refusals via `file:{digest or name}` | `exceptions.py:156-159`, `exception_feeds.py:158` |
| F2 | `preview_file` fails after reading its own bytes, then `_stable_digest(path)` reopens the path; a replacement between the two is hashed and attached to the old failure | `exceptions.py:215-216`, `mapping.preview_file` |
| F3 | `_stage` opens the connection outside its try and catches only `ImportError_`; the viewer opens outside its `sqlite3.Error` handler; exit 1 already means a recorded refusal | `__main__.py:30-40` |

## Design constraints

* Core feed and queue stay unchanged. The feed's refusal ref is `file:{digest or source_name}` and `source_name` is displayed, so a hashless refusal can stay distinct without a core change only if the adapter hands the feed a source name that contains an opaque identity and an empty digest. The queue item then shows no digest (Unknown), not a pretended one.
* One bounded snapshot: the producer must read the bytes once, hash those bytes, and preview those same bytes. This needs a bytes-level preview in `mapping.py` (importer-owned); `preview_file` keeps its behaviour by delegating.
* Hashless identity: a one-way identifier of the resolved path plus device, inode, size and mtime_ns captured before the read, so a replacement or other directory differs and an unchanged re-submission still dedupes. Unreadable (no stat) gets a fresh attempt id. It is a source identity, not a content identity; stat identity can be defeated by deliberately restoring inode and mtime, recorded as a limit.
* Shared store, sqlstore, schema, `exception_register.py`, API and UI hooks stay paused under #132 serialisation; no api dependency on importer.

## Planning Readiness

Ready.
