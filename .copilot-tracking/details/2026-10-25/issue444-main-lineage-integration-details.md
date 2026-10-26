# Issue 444 main lineage integration details

Date: 2026-10-25. Plan: ../../plans/2026-10-25/issue444-main-lineage-integration-plan.md.

## Phase 2 merge

* `git fetch origin main`; merge with `git merge --no-ff origin/main`, message `merge: integrate main into resident feedback preview (refs #444)` with the Copilot trailer.
* Expected single conflict: docs/reference/log.md. Keep every entry from both sides in chronological order, add nothing else.
* Commit identity: repo-local noreply from `gh api user` (already configured; re-verify).

## Phase 3 compatibility rule

Edit only resident_preview modules, their fixture, tests, READMEs or docs if a merged-tree failure is directly caused by main drift. Staff server.py, auth.py, identity.py, projection.py and store.py are not edited. A failure that requires such an edit is a blocker reported to the coordinator.

## Phase 4 validation

* Install: pip only, existing venv /tmp/ama444/venv (editable installs follow the worktree).
* Run focused core/api resident tests, then full core and api suites, ruff and mypy.
* Browser: src/api/checks/resident_preview_browser_check.py against a freshly built disposable fixture in a new /tmp/ama444-lineage-* directory on a distinct port, stopped afterwards. Do not touch 8350, 8444, 8445.
* Web edits are not planned. If any arise, fetch current web-interface-guidelines and review; disclose no screen-reader audit and partial Fluent 2, no conformance claim.

## Critique amendments (applied directly, C1-C3)

* C1: the final browser check runs against the final evidence-committed head (after Phase 5 commit), not before it. Record that head SHA in the changes artifact only if it can be done without a further commit; otherwise record it in the PR body and final report. A pre-commit run is labelled as earlier evidence.
* C2: immediately before the gate, `git fetch origin main` and compare to the gate base. If main moved, stop, merge the new main and regenerate evidence.
* C3: evidence manifest committed before the gate: research, plan, details, critique, state JSON, changes, review, and focused/full/browser outcomes. `git status --porcelain --untracked-files=all` must be empty before the gate starts.

## Phase 5 and 6

* Changes artifact, one independent Review, state JSON updates before and after each transition.
* Gate: `python3 -B tools/rpi-checks.py --all --base <current origin/main> --lock-timeout 14400 --out <new external dir>`; then `--verify-receipt <dir>/receipt.json --base <same>`. Clean ignored caches first (git clean -fdX in this worktree only).
* Bounded to two correction cycles; unresolved findings become a human blocker.
* Push the branch (normal push) and open a draft PR with `Refs #444`; no merge, no closing keyword.
