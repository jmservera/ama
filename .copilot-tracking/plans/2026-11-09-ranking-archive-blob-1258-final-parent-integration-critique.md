# Critique: final integrated #1258 parent plan (2026-11-09)

Refs #1258. One independent critique by a separate read-only agent (`rubber-duck`) over the research, plan and details, before any merge or commit of the integration. Executed once; not repeated.

## Verdict

Revise: stated refs, counts and the predicted merge tree verified; three blocking and one non-blocking finding.

## Findings and dispositions (applied directly, no user decision needed)

* 1 Blocking: CI input binding incomplete; `test_live_doc_links.py` scans live Markdown that main changed, and other tests consume docs. Applied: per-check input binding added; doc-reading tests are bound to main's identical `docs` tree; the live link test is the one genuinely changed input and is run once as the smallest existing check.
* 2 Blocking: child CI not fully bound to the final candidate (the #136 head had a different `src` tree, the #1259 head a different `infra` tree; hosted merge ref not observed). Applied: child CI and C6 results are reported as historical child results over their own identities, not as CI of the candidate.
* 3 Blocking: merges used moving refs. Applied: merge by commit id after a pre-merge equality and clean-worktree check; stop on difference.
* 4 Non-blocking: recheck after the final record commit. Applied.
