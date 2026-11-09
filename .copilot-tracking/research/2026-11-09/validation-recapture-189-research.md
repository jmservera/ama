<!-- markdownlint-disable-file -->
# Issue 189 validation recapture research (2026-11-09)

Task `validation-recapture-189`; parent `sql-main-integration-189` (head `d985f149590f83a50a6d9db08312f21ecf7bc01b`, tree `b6bab6bd9fd57766417ce6cf1ad719b8da4fa04d`). Refs #189 only. Research disposition: executed (prospective; read-only inspection, no source change).

## Pinned facts

* Branch `feat/demo-simulator-control-189-1109`, worktree clean, HEAD `d985f1495`, repository-local identity `8036360+jmservera@users.noreply.github.com` (matches `gh api user`: id 8036360, login jmservera). Nothing pushed.
* Fetched `origin/main` is `ef28d4da42d83b111d48f14df9b70e3c4932a477` (`chore(rubric): record score 78/100`), one commit after `8d6f029ca`. `git diff --stat 8d6f029ca origin/main` is one file (`.github/rubric/scores/latest.json`, 4+/4-); `src`, `infra` and `tools` are unchanged since the #1308 merge. The previously merged main source is therefore unchanged by main (`main8d` equivalence), and no new merge is made.
* Current source state equals the tested source: `d985f1495` only added `.copilot-tracking` records on top of merge `105ea6cb5`.
* Environment: Python 3.12.3 in the worktree `.venv`; Playwright with Chromium 1248 under `~/.cache/ms-playwright`; axe 4.10.3 assets `/tmp/axe-4.10.3.min.js` and `/tmp/axepk/package/axe.min.js` both hash to `880970c081707360e64f34cea25ff91892f5bc95675b0776925b9709dd8a68bb` (the pin in the browser check). No `ZF_*` variable is set in the environment.
* The browser check binds `ThreadingHTTPServer(("127.0.0.1", 0))` (ephemeral loopback port owned by the run) and launches one headless Chromium it closes itself; no fixed port and no shared service.

## Adverse loss retained (not reconstructed)

The prior handoff `handoff-189-sql-main-integration.md` states that its owned raw logs were REMOVED after the run ("logs removed afterwards, not committed"). That loss is an adverse fact: the earlier per-module counts (27, 34, 36, 41, 18, 8, 5, 31 API; 142/65 and 256/93 core; 0 axe violations) are recorded only as summaries in the committed changes record and have no surviving raw producer stdout, stderr or exit files. They are not treated as current evidence and are not rebuilt. This recapture is a fresh, separate observation of the same selections.

Also retained unchanged: the wrong `--out` browser invocation (exit 2, usage error), the first merge command failure on `-F -`, the original independent Functional review and adverse findings, C1 records, source-level approve 0 on `8ab64519c`, historical F3 cause UNKNOWN, and the whole-API capture 2105 tests / 365 skips producer 0 (not rerun).

## Cycle state

C1 is one of five total scoped cycles spent, four remain. This validation edits no productive source, so it neither spends nor resets a cycle. A confirmed new defect would be recorded with scope and count and stop for authorization; no fix is authorized here.

## Planning Readiness

Ready. Remaining unknowns are the capture outcomes, recorded prospectively as P3.
