<!-- markdownlint-disable-file -->
# Changes: discovery parent reconciliation (#123), 2026-11-07

Plan: [plan](../../plans/2026-11-07/parent-reconciliation-123-plan.md). Refs #123 #440 #128; no closing keywords.

## Actual changes

* Planning commit `fd78de2f9d850cd3ddaef3434bf8cac86814ec39` (Research, Plan, details, critique, state) preceded every merge.
* Remote refs verified with `git ls-remote` against the pins, then ordinary merge of parent `9bacb87dc04fb51ba747b35ec78061b05af184be` (merge commit `9d8bf1d5`, no conflict).
* Ordinary merge of main `b284d0d3e8ebed24d40bf9eb1e23de1ae9101d01` (merge commit `6f540a08`). One conflict, `docs/architecture/cutover-evidence-pack.md`: both sides appended at the tail. Resolved by keeping the parent checkpoints in full, then main's "Parent #73 topic checkpoint" in full; only conflict markers and one duplicate blank line were removed. Frontmatter `ms.date` is main's 2026-11-07. `docs/reference/log.md` and `docs/reference/README.md` auto-merged.
* The conflict resolution initially dropped main's trailing blank line at end of file; a later check against main found it and it is restored in the implementation commit (no content change).
* No source, test, threshold, approval, requirement or tooling edit by this task; the parent's inherited `paired_equity.py`, its tests and the core README paragraph are unchanged.

## Disclosures

* `docs/reference/README.md` parent-side check reported one row differing (the AI Tokenomics row), which is main's own intentional update of that row, kept as main's. It is not a loss by this task.
* A first link check flagged one anchor (`eighth-stabilization-checkpoint-finance-parent-held-export-manifest-contract-2026-11-05-refs-440-96`); it resolves to an explicit `<a id>` before the parent's "Ninth stabilization checkpoint" heading, inherited from the reviewed parent. Not a defect.
* Ordinary merge commits follow the planning commit by design; ancestry kept: `dec700c7`, parent `9bacb87d` and main `b284d0d3` are all ancestors.

## Scope relative to fresh main `b284d0d3` (before this record)

168 files, 8434 additions, 3 deletions (two inherited one-line replacements in `src/core/README.md` and `paired_equity.py`, plus the end-of-file blank line now restored). Non-tracking paths: the evidence pack, KB index, log, `src/core/README.md`, `paired_equity.py`, `test_paired_equity.py`; all others are dated `.copilot-tracking` records. No infrastructure, SQL, finance, security or deployment implementation. FOCUSED tier unchanged.

## Current light checks actually run (all exit 0)

* Current-source import identity assertions for seven core modules and tests.
* 74 unit tests: paired-equity, journey-register, release, release-invalidation, ranking-publication, cohort-eval.
* Core `ruff check` (no cache), `ruff format --check` (213 files) and configured `mypy` (266 source files) with the declared Ruff 0.17.1 and mypy 2.4.0 from the existing external environment `/tmp/ci764b-venv`.
* 26 changed JSON files parsed; 50 added relative links checked; historical-line preservation of log, README (apart from main's own row) and pack for both sides; `git diff --check` against main.
* Tool versions in `/tmp/ama-96-venv` (0.17.3, 2.4.1) were not used for these results.

## Pending

The focused `tools/rpi-checks.py --changed` gate (selection computed first, see the review), independent exact-head review, hosted checks and the guarded merge.
