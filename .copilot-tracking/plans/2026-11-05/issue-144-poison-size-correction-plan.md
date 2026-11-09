# Plan: issue 144 poison-copy size correction (2026-11-05)

Research: [research](../../research/2026-11-05-issue-144-poison-size-correction-research.md). Details: [details](../../details/2026-11-05/issue-144-poison-size-correction-details.md).

* [ ] Implement: bound the encoded poison text, add boundary regressions that fail before the fix.
* [ ] Review: one self review; FULL gate and independent assessment remain pending.

Validation: FULL tier required, NOT run (233 owns heavy admission). Light only: agents unit tests, ruff, mypy with external cache. Old full-r5 receipt is historical for the previous head.

Critique (single pass): proceed. Applied: bound bytes after UTF-8 (not characters) with a base64 budget well under 65,536 bytes including XML wrapper; keep a diagnostic prefix and prepend an explicit truncation marker with the original size so a truncated copy is never mistaken for complete; cut on a character boundary; keep write-before-delete. Rejected: a new dependency or splitting into several poison messages (larger scope).
