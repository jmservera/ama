# Plan: issue 225 constructed field draft in browser (2026-11-03, r2)

Research: .copilot-tracking/research/2026-11-03-issue-225-finance-draft-browser-research.md

## Phases

1. Add `DRAFT_REVIEW`, `DRAFT_PHRASES` and a fifth SCREENS element (optional routed review) plus a fourth story for the Grants and Evidence Officer.
2. Update `src/api/README.md` and append a `docs/reference/log.md` entry.
3. Focused validation: the check with pinned axe 4.10.3, finance unit tests, ruff, mypy.

## Details

* Route `**/form-review` with `page.route`; the guard for non-GET requests stays on (route fulfilment is not a network write).
* State plainly the draft is constructed, not server-built.

## Critique (inline, executed once)

* Risk: reader mistakes routed JSON for real server evidence. Mitigation: README and PR say constructed. Accepted.
* Risk: stale fixture drift from the view shape. Mitigation: shape copied from the unit test REVIEW and core view. Accepted.
* Verdict: proceed; no conflict with confirmed decisions.
