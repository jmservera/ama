<!-- markdownlint-disable-file -->
# Plan: discovery parent reconciliation (#123, Refs #440 #128), 2026-11-07

Research: [research](../../research/2026-11-07/parent-reconciliation-123-research.md). Details: [details](../../details/2026-11-07/parent-reconciliation-123-details.md). Critique: [critique](parent-reconciliation-123-critique.md).

Tier: FOCUSED (admitted). Bounded constructed paired-equity diagnostic tooling, coupled core tests and documentation; not documentation only. Any full-tier category in the final main-relative diff stops the work before heavy steps.

## Phases

* [ ] Phase 1: Commit this prospective Research, Plan, details, critique and state (planning commit) before any merge. Fresh `gh api user` identity, repository-local email check, Conventional Commit and Copilot trailer.
* Preflight pins; compare `git ls-remote` of both remote refs with the pins immediately before each merge; ordinary merge of `9bacb87d` into the topic (expected clean; both tips ancestors afterwards).
* [ ] Phase 3: Preflight pins; ordinary merge of `b284d0d3`. Resolve the evidence-pack tail conflict by keeping both sides in full and in order (parent checkpoint sections, then main's dated section; `ms.date` the later value 2026-11-07), never picking one side. Verify log and README keep every line from both sides.
* [ ] Phase 4: Recompute the final main-relative scope; confirm no main-side deletions, no path outside the bounded set; re-confirm FOCUSED.
* [ ] Phase 5: Current relevant checks (light, external caches, bytecode off, explicit current-source imports): paired-equity, journey-register, release and invalidation, ranking-publication and cohort-eval unit tests; core Ruff check, Ruff format check and configured mypy including tests with declared tool versions; JSON parse of changed JSON; changed Markdown relative links and anchors; historical-line preservation; `git diff --check`.
* [ ] Phase 6: Changes record, author Review (one pass), final state; commit implementation and original dated RPI records. Freeze; verify clean tracked, untracked and ignored.
* [ ] Phase 7: Before running anything, compute the actual `--changed` selection for the final candidate by read-only use of the tool's own selection logic (no group executed). Critique PC-001: the inherited core source change may select all projects, images and `logo-0600`; if any excluded group (SQL, browser, scanner, image build, full) is selected, do not run the gate and return the exact blocker. Only if selection is bounded run `python3 tools/rpi-checks.py --changed --jobs 2 --lock-timeout 0 --base <b284d0d3> --out <new root-filesystem dir> < /dev/null`, non-queued; if the lock is held or owned elsewhere, record and stop without waiting. Verify any receipt with `--verify-receipt ... --required-scope partial --base <b284d0d3>` and compare its groups with the planned tests. Receipt and log stay outside the repository and no commit follows them.

## Stop conditions

* Remote or main differs from the pinned SHAs; a conflict with unestablishable intent; any non-bounded path in the final scope; focused selection needing SQL, browser, scanner, image or full groups; lock held. Report the exact blocker; no skip token, fabricated success or cloud fallback.

## Boundaries

* No source, threshold, approval or requirement edits; `fairness_evidence=False` and `activation_allowed=False` unchanged. No push, PR, issue or acceptance mutation; no cleanup; #1231 R35 receipt and images, root ranking and main are protected.
* Refs only; no closing keyword.
