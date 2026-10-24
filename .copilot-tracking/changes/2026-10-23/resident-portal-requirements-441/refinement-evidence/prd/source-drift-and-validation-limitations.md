# Source drift and validation limitations

## Immutable input remains controlling

The PRD candidate is derived from the supplied immutable snapshot pinned by
the caller to `4017b214bb021244b06264629953d84f29003c53`, not from the remote
PR head or the primary checkout.

At 2026-10-23 22:40 UTC the coordinator reported that remote PR #442 had
advanced to `d8b416a3f13e3e4a5b018f0853285ced972c1c8a`. The only reported
change from the pinned head is `.github/rubric/scores/latest.json`, with 22
added and 21 removed lines. The source snapshot and PRD candidate were not
changed to incorporate this remote movement. The candidate and patch remain
bound to the pinned snapshot; no remote fetch or Git verification is claimed.

## Hosted review limitation for #441 evidence

The coordinator reported that a 2026-10-23 22:38:50 hosted Copilot review
identified a medium reproducibility defect in the tracked
`.copilot-tracking/changes/2026-10-23/resident-portal-requirements-441/validate-integration.py:273`.
Its scope assertion rejects committed `.copilot-tracking` and generated-score
paths before it can generate the focused report. The stated correction belongs
to native RPI integration after the current heavy gate completes, not this
authoring task. Canonical documentation comparisons must treat newly added
files as having an empty `BASE`, while continuing to reject numbered ADR
changes.

Accordingly:

* The inherited focused report is retained as historical source evidence but
  was **not reproduced in this task** and is not claimed as a current,
  independently regenerated report.
* No authoring check here fixes or executes the tracked validator against the
  live worktree.
* The active #441 gate, reported running as PID `3616364`, must finish
  undisturbed. No validator/worktree edit, gate interruption, publication,
  commit, push or merge was performed.
* The remote head, diff summary, hosted review timestamp and gate PID are
  coordinator-reported context, not independently fetched or verified by this
  package.

These limitations do not change the immutable PRD source, exact pinned-base
patch reconstruction, or authoring hashes. They do preclude claiming that this
package reproduces #441's focused integration report or active gate result.
