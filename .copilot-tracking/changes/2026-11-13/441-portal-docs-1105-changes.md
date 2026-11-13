# Changes: 441-portal-docs-1105

Status: implementation complete, tracking-only writes (no `docs/` or `src/` edits). Refs #441. Criterion 9 is NOT claimed complete; Criterion 5 is NOT claimed.

## Evidence

| Item | Value |
| --- | --- |
| Checker | `.copilot-tracking/changes/2026-11-13/441-portal-docs-1105-check.py`, sha256 `a3391d70313f432d05ccebe952ccb3cdf45a06e3e220ae5ea505b8716f279df6` (stdlib, read-only, reads committed blobs via `git show`) |
| Head result | `441-portal-docs-1105-check-head.json`, sha256 `3c5b98e1af36176b0afb99c2fd8c50d6c0911c0b68bd31d51b702368355624dc`, exit 0 |
| Baseline result | `441-portal-docs-1105-check-baseline.json` (rev `9172939c`, parent of `b7d66e42`, last commit touching the four files), sha256 `caca75b9fccf1ce7c6008ea56752e077ac8e4f4df69f934589f872188d439200`, exit 0 |
| Head | `3b05143179f83235c5b4e80e70aad99bdc44d83f` |
| Blobs | BRD `34d88395de861e9799eb9e24121a21c92c7a5adc`; PRD `c788b917bafaede215f326f0efc71e071a687f1c`; ADR 0007 `541e0f72dd2c1b5ae6feb2439a9223331bcdd783`; `docs/architecture/README.md` `1093ef0cdea18ffe15bb19fa942723dac6893e7c` |

Design change during implementation: the first run showed a false OD "open" test, a trace-table offset (0 rows) and a false PRD FR-057 duplicate (trace row); each was fixed in the checker before the recorded run (hash above is the final script).

## Findings (head)

* Links/anchors: BRD 51, ADR 0007 4, architecture README 73 relative links all resolve. PRD: 1 unresolved, `docs/prds/zava-forward-retrofit-programme-demonstrator.md:609` anchor `#agents-in-the-retrofit-process-2026-10-13` missing in `docs/capstone/README.md`. Same result at baseline (inherited, not introduced by recent changes; not repaired here).
* Status markers PASS: BRD status `draft` (line 8), PRD `in-review` and `exercise_status` unsigned (lines 8-9), OD-52..OD-55 defined (BRD 2170-2173) with no closure marker, OD-53 states all AI-drafted resident messages remain individually human-approved (2171), FR-044 per-message named review default with bounded RULE-028 exception and AC-084 "must not fabricate per-message human review" (line 1602), PRD `Not run` rows (30 resident AC rows).
* Numbering/traceability PASS: BRD FR/NFR/RULE definitions unique; BRD FR-053..062 and AC-104..126 present; PRD FR-062..071 and AC-111..140 present; 15 PRD resident upstream trace rows resolve to defined BRD ids (namespaces kept separate).
* Formulas PASS: all 11 BRD capacity measures x low/base/high recompute from inputs within tolerance; F = -1.594/14.74/94.333; break-even slope 35.4, constant -2.96, 8.36%; F(25/50/75%) = 5.89/14.74/23.59; V break-even 29.905% (quoted 29.90%); I/O disjoint-cohort ratio equals D.
* Inherited-diagnostic comparison: head and baseline differ only in ADR 0007 text/link detail, status unchanged; the single FAIL (PRD:609 anchor) is identical.

## Premise mismatch (INFO, unresolved, reported not fixed)

The issue states ADR 0007 was accepted on 2026-11-04 as the resident portal architecture. At this base `docs/adrs/0007-contractor-intake-staff-mediated-proposal.md` is the contractor job-pack ADR with status "Proposed" (line 11), and no resident portal ADR exists in `docs/adrs/`. PRD/BRD carry no resident ADR linkage. The coordinator should confirm which ADR the owner's 2026-11-04 decision refers to; this task does not alter ADRs.

## Outstanding (not performed here)

* Criterion 5: human requirements-owner disposition of FR-044/AC-084 wording; not created or claimed.
* Criterion 9 residuals: hosted CI for the exact publication head, exact integrated-byte independent review of the documents, complete local gate where applicable, push/PR (local freeze: none run).
* Nothing here is live resident acceptance, screen-reader conformance, deployment, spending or final requirements approval.

## Scratch

No venv, no network, no private data. `/tmp/441-*` scratch removed.
