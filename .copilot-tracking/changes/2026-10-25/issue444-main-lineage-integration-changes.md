# Issue 444 lineage integration changes

Date: 2026-10-25. Plan: ../../plans/2026-10-25/issue444-main-lineage-integration-plan.md. Parent: 2026-10-24 issue444 artifacts (unchanged).

## Lineage

* Pre-merge candidate a3e527fd5a8bfe73a10826ed4e316b98464a0782 (base f1e2d830). Pre-merge evidence commit 173e9ffc (research, plan, details, critique, state).
* Merge commit 2049b3b2 merged origin/main 36996d70a3f6dbee9df4d16400afd07c3614e69e with `--no-ff`. No reset, amend, rebase or force-push.
* One textual conflict, docs/reference/log.md: both sides kept; the #444 entry was moved after main's entries (append order). No earlier entry rewritten.
* No source change was needed. After the merge, `git diff origin/main` shows no change to server.py, auth.py, identity.py, projection.py or store.py.

## Validation on the merged tree (before the evidence commit)

* Resident core tests 31 OK; resident api tests 14 OK (real local server).
* Full core suite 1274 tests OK (167 skipped); full api suite 1027 tests OK (306 skipped).
* ruff and mypy clean for src/core (70 files) and src/api (69 files).
* Browser check: run on the final evidence-committed head (see PR body and final report), on a disposable fixture and free loopback port; it does not touch 8350, 8444, 8445 or /tmp/ama-444-preview-data.

## Retained limitations

* The original 2026-10-24 gate receipt is historical (old base). The original browser check pre-dated the Review fix; the full gate covered it.
* No human screen-reader audit; accessibility harness not run (needs uv/npx); Fluent 2 is partial; no conformance claim.
* Live Azure, SQL and real-AI acceptance remain separate gates; #444 stays open (Refs only).

## Services

Employee 8350 and residents 8444/8445 returned HTTP 200 before edits and are not restarted. They are snapshot-based (they run the pre-merge code); restarting onto the merged code is a later owner decision.
