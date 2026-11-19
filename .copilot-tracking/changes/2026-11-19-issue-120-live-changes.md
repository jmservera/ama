# Issue 120 live changes (2026-11-19)

## Files

* docs/reference/research/issue-120-live-2026-11-19.md (new)
* docs/reference/README.md (index row), docs/reference/log.md (entry)

No source file changed; tier FOCUSED, basis: documentation only.

## Per-criterion proven/unproven

| Criterion | Status |
| --- | --- |
| 1 DPIA reference gate (ticked) | Not re-examined |
| 2 Minimum group size (ticked) | Not re-examined |
| 3 Staff notice approved and enabling action audited | Proven locally (38 tests OK, 5 skipped); unproven on the deployed demo (needs config change, excluded) |

## Validation

* `python3 -m unittest tests.test_timecapture tests.test_timecapture_copy` (src/api): OK
* Markdown link and diff review; mypy, ruff, accessibility baseline not applicable (no source or web change)
* Azure: none used; nothing to delete
