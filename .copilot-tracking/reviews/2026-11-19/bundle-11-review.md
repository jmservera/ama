---
title: Bundle 11 independent exact-head review
description: Local diff review of docs demo evidence bundle 11 against origin/main
ms.date: 2026-11-19
---

Scope: `git diff origin/main..f837e39f1` (108 commits, 268 files, docs and tracking only).

Checks run

* Path check: every changed file is under `docs/` or `.copilot-tracking/`. Pass.
* Conflict markers in added lines: none. Pass.
* Secret patterns (tokens, private keys, JWT, SAS signatures, password assignments) in added lines: none. Pass.
* Closing keywords (close/fix/resolve plus issue number) in commit messages: none. Pass.
* Relative links in added or modified Markdown: no new broken links; 17 broken links in `docs/reference/log.md` exist on origin/main and are not touched.
* Evidence claims: "proven" statements carry a basis column, test count or retained note. Rows marked "Proven (ticked)" with "Not re-audited" restate issue ticks, not new evidence.

Verdict: approve for owner merge, advisory only.

Advisories

* Tracking files for repeated runs of one issue take the latest worker version; earlier run detail is in the worker worktrees, not here.
* Several research notes are separate reruns of the same topic and may overlap.
* No hosted CI applies; owner and human approval gates remain.
