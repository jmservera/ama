# Changes: issue 157 live re-verification (2026-11-18)

Tier: FOCUSED (documentation and evidence only; no src, SQL, infrastructure or deployment change; no rpi-checks --all).

## Files

* docs/reference/research/issue-157-live-chat-epic-recheck-2026-11-18.md (new)
* docs/reference/research/issue-157-live-2026-11-18/ (probe script, redacted output, screenshot)
* docs/reference/README.md (index row), docs/reference/log.md (entry)
* .copilot-tracking/ artifacts and evidence copy

## Per-criterion table

| Criterion | Proven or unproven | Reason |
| --- | --- | --- |
| Complete the #440 stabilization checkpoint | Unproven | #440 triage filing and owner approvals, and PR with independent review, are human or PR steps; live re-observation of the time status 500 supports D1 |
| Child features accepted | Unproven | #162 and #164 open; granted break-glass needs a deployed setting change; thresholds and task registration need owner approval; screen-reader testing waived for the demo, not evidenced |
| Decision accepted (ticked) | Not re-opened | ADR 0004, 2026-10-15 |
| No memory as controlled-decision evidence (ticked) | Not re-opened | PR #1552 |
| Chat consumption bounded (ticked) | Not re-opened | PRs #1547, #1558 |

## Live results (revision 0000032)

Chat status 200 with warning and 30 days retention; own-thread list only; unknown thread 404; break-glass refused 403 with audit chain intact (2197 to 2198); regulatory usage 403 for non-assigned user; time status 500 persists.

## Validation

No tests apply (no code). Checks run: JSON validity of the state file, Markdown link existence review, secret scan (below). Nothing created on Azure; scratch login state deleted.
