# Plan: #441 Criterion 9 local documentation checks

Task `441-portal-docs-1105`. Focused tier, tracking-only writes. Details: `.copilot-tracking/details/2026-11-13/441-portal-docs-1105-details.md`.

## Phases

1. Research (done): issue body/comments, target files, premise mismatch on ADR 0007.
2. Plan and critique (this): one independent critique before any script run.
3. Implement: store checker at `.copilot-tracking/changes/2026-11-13/441-portal-docs-1105-check.py`, run it read-only, record source sha256, blob SHAs, exit code, findings in the changes file. No edits to `docs/` or `src/`.
4. Review: independent `code-review`, review file written, state updated.
5. Commit `Refs #441` with Co-authored-by trailer; record `commit-complete`.

## Success criteria

* Relative links and heading anchors in BRD, PRD, ADR 0007, `docs/architecture/README.md` (portal sections) resolve, or each miss is listed as inherited/new.
* Visible-status markers: BRD status draft, PRD unsigned, ADR 0007 Proposed status as actually written, OD-52..OD-55 open, `Not run` present, FR-044/AC-084 per-message default text.
* Numbering: BRD FR/AC/RULE/OD ids unique per file; BRD FR-053..062 and AC-104..126 present; PRD FR-062..071 and AC-111..140 present; namespaces kept separate.
* Formulas: recompute BRD capacity table (W,B,G,H,J,N,O,F) from stated table values and PRD/addendum quoted figures (-1.594/14.74/94.333; 48; 8.36%).
* No claim of Criterion 5 approval; premise mismatch (ADR 0007 is contractor intake, Proposed) reported as a finding, not fixed.
* Exit codes captured directly; no venv, no network, no private data.

## Amendments from critique (PC-001..PC-006)

See the critique disposition table. Criterion 9 stays unticked in any statement: publication gates (hosted CI, exact-head independent review of integrated bytes, complete local gate) are listed as outstanding. Criterion 5 remains human-owned.
