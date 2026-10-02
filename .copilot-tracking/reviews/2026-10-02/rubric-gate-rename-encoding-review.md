<!-- markdownlint-disable-file -->

# Plan, Changes and Review: rubric-gate-rename-encoding

* Task ID: 2026-10-02-rubric-gate-rename-encoding (child of 2026-10-02-rubric-gate-hardening)
* Evidence: .copilot-tracking/reviews/2026-10-02/rubric-gate-hardening-review.md (RH-001, RH-002)

## Plan and changes

* [x] RH-002 `write_context` reduces to a stat line only the removed paths that still exist on disk (oversize, symlink); deleted and rename-source paths go back into the content diff, so renames show as renames and deletions as headers only (`-D`).
* [x] RH-001 `fingerprint_files` encodes paths with `surrogateescape`; both scripts catch `UnicodeError`.
* [x] Tests: deletion diff has no content; rename within scope shows `rename from`; grown file is stat-only; non-UTF-8 path fingerprints (self-skips where the file system rejects the name).
* Critique: not dispatched (stated fixes).

## Validation

* 50 passed, 1 skipped (symlink), minimal pytest stub. Workflow unchanged; no recompile.

## Review (one pass, inline)

* Outcome: Conformant.
* RH-002 closed: the rename test would fail on the previous code, which listed the target as a new file.
* RH-001 closed for fingerprinting; context JSON with surrogate paths would still fail `json.dumps` encoding on write as UTF-8 and is caught as `UnicodeError` (fail closed with a message).
* Carry-over: RS-002 real pytest run; RH-003 to RH-009 remain open.
