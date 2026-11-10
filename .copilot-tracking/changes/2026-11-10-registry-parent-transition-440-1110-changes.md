# Changes: Registry observation parent transition (2026-11-10, Refs #440 #185)

Status: PROSPECTIVE declaration, written before `implement-start`; the Implementation record is completed after the edits.

## Planned changes (docs only)

* Ordinary `--no-ff` merge of `origin/main` `eff05737e8eaed584f3c269754d45bc5e44d0168` into the topic (parent order: `ffb3e4158`, then `eff05737`).
* Resolve append-only conflicts in `docs/architecture/cutover-evidence-pack.md` and `docs/reference/README.md`, keeping main's text and the Registry additions.
* Update dependency wording in the Registry section, README paragraph and log entry.
* Add this task's own dated RPI records and state.

## Not changed

No source, test, config, workflow or infrastructure file; no older observation, refusal chain or archive.

## Implementation record

Completed. Ordinary no-ff merge of `origin/main` `eff05737e8eaed584f3c269754d45bc5e44d0168` is staged and committed with the records. Two append-at-end-of-file conflicts (pack, README) were resolved by removing the marker lines only, so both sides are kept; main's text is unchanged. Wording edits: pack intro sentence, README paragraph, log entry. Result against `origin/main`: 3 docs files, 86 insertions, 0 deletions; no non-docs, non-tracking file differs from main. Divergence: none from plan.
