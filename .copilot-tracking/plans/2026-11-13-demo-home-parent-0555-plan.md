---
title: Plan, seed demo home parent with ready #74
description: Mechanical integration plan; no functional change
ms.date: 2026-11-13
---

* [x] 1. (Author-reported) Confirm base `15bfee2d7`, clean worktree and privacy-safe repository-local author email.
* [x] 2. Merge `6c86e1dc0` with `--no-ff`; require tree equal to `6c86e1dc0` tree `a09d9ae96aa5fe88ccfd420e7a00a51b15ac9f68`.
* [x] 3. Verify the three source blobs equal `6c86e1dc0` and `f50c5c7fd` blobs, and the only differences from base are the three `src/api` files and 18 added `.copilot-tracking` files.
* [x] 4. Add parent tracking only: research, plan, critique, changes, hold record, review, state JSON. No edit to any input file.
* [x] 5. Run one independent Review of the merge HEAD plus the explicitly identified working-tree records; an exact-committed-head review is still required before publication. Record it as returned.
* [x] 6. Commit the tracking records with a Conventional Commit and trailer. No push, PR, issue or checkbox change.

## Holds and exclusions

* #184 `e904` excluded (not ready: new format FAIL, SQL unrun). It does not block this independent home-scope input.
* Future children target this parent only when ready or declared, never as speculative main PRs.
* No test, SQL, browser, install, provider, `.env` or private dataset use here. The full gate is not claimed and no applicable requirement is waived.

## Future parent validation (not done here)

Tier: this parent touches `app.js`, a browser check and a README in `src/api`; the later publishing change takes the focused tier plus the full tier if combined with infrastructure, SQL or security work. Before any publication: fetch main, re-run the focused checks (node check, Ruff check and format, mypy, the six existing API tests, one bounded browser run with axe if the pinned file is available) on the exact parent head, obtain independent exact-head review, human approvals and applicable hosted CI. Link with `Refs #74`, not a closing keyword.
