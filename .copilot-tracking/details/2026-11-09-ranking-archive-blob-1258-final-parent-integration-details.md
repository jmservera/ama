# Details: final integrated #1258 parent candidate (2026-11-09)

Refs #1258, #1259, #136. Plan: `.copilot-tracking/plans/2026-11-09-ranking-archive-blob-1258-final-parent-integration-plan.md`.

## Commands (read-only unless stated)

* Prospective commit: `git add .copilot-tracking/...final-parent-integration*` then `git commit`.
* Merge 1: `git merge --no-ff -m "merge: integrate merged 1259 and 136 children (ac41cce5)" ac41cce5b1a7ded6a33fe5c57786affbca4783c0` after `git rev-parse` of both remote refs equals the pinned ids and `git status --short` is empty.
* Merge 2: `git merge --no-ff -m "merge: integrate origin/main 2be660e9 into ranking archive parent" 2be660e9d290f95ff05fc5a56d6539768576732b`.
* Identity: `git rev-parse HEAD HEAD^{tree}`, `git rev-parse HEAD:src HEAD:infra HEAD:tools HEAD:.github/workflows HEAD:src/agents HEAD:src/core/pyproject.toml HEAD:src/api/pyproject.toml`.
* Diffs: `git diff --name-status ac41cce5 HEAD`, `git diff --name-status 2be660e9 HEAD`, `git diff --name-status 99814198 HEAD`, `git diff --diff-filter=MD --name-status <origin> HEAD -- .copilot-tracking`.
* Hygiene: `git diff --check`, `git status --short`, author and committer address.
* Functional reads: `src/core/src/zava_forward/core/ranking_publication.py`, `ranking_publication_runner.py`, `store.py` selection, `ranking_archive_blob.py`, `infra/modules/containerapps.bicep`, `storage.bicep`, `main.bicep`.

## Expected bindings

| Item | Expected |
| --- | --- |
| `HEAD:src` | `f0df7dc4246694b6828f14b352bcaa8ff9ab671a` |
| `HEAD:infra` | `d94040329d5497aee252300972cb3c7497689d25` |
| `HEAD:src/agents` | `237bf28b67cc...` equal to main |
| `HEAD:tools`, `HEAD:.github/workflows` | equal to main and ac41 |
| `HEAD:docs` | equal to main's `1191a55f6229...` |
| Ancestors | `99814198`, `03a7969c`, `cf8dbc28`, `fbf0a0ab`, `ac41cce5`, `2be660e9` |

## Retained logs

Command output of the identity and diff steps is captured outside the repository in an owned directory with SHA-256 and exits (no secrets, no home files). Original raw logs of C6 stay at `/tmp/c6-1258-9Hvy6k/` and the files directory; none removed.

## Focused check (the only one planned)

`cd src/core && python -m unittest tests.test_live_doc_links -v` (or `discover -s tests -p 'test_live_doc_links.py'`) in an owned environment outside the repository, after the second merge and again unaffected by later record commits except tracking (which the test skips). Reason: its input is live Markdown, which main changed. No other test input changed relative to a qualified identity.

## Check selection rule

No test executes unless a binding differs. If one does, name the changed input, the existing smallest check and why, and run it from the relevant project root in an owned environment with pinned ruff 0.17.1 and mypy 2.4.0; never waive a failure.

## Limits to restate in the handoff

Fake Blob contracts are not Azure durability, WORM or live acceptance; the hosted children CI ran on PR heads, not on this parent; no parent CI, SQL, browser or full gate; main's docs are carried, not reviewed for #1258 content; 1288 quality excluded; whole #1258, #1259 and #136 stay open and `Refs` only; human acceptance and approvals untouched.
