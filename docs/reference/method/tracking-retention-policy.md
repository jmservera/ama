---
title: Tracking Retention Policy
description: Explicit preservation, durable source ownership and reversible generated-output cleanup
ms.date: 2026-10-24
ms.topic: reference
---

## Ownership and Boundaries

Keep active research, plans, details, changes and original critique/Review
evidence in dated tracking locations. Unknown-active RPI records and adverse
findings stay intact. Completion, age, duplication or an unreferenced path alone
does not authorize deletion. Preserve original RPI evidence and the
[complete local publication gate](../../../src/README.md#local-rpi-gate),
independent review, hosted checks and human approval requirements.

Promote reusable builders to `tools/` and durable evidence to the appropriate
`docs/` area. Keep editable sources and pinned input baselines distinct from
regenerable outputs. Final deck delivery locations remain unchanged. For new
runs, put heavy generated previews, candidate packages, exports and transient
validation output in explicit external scratch or an approved artifact store
by default; retain dated tracking records of commands, inputs and outcomes.
This does not authorize moving or deleting existing records automatically.

## Explicit Cleanup Contract

Each cleanup needs an approved finite per-run path manifest, not an age rule,
glob or automatic historical sweep. Archive the entire existing tracking
snapshot outside the checkout, including untracked files and opaque symlink
identities without following their targets. Record member types, sizes and
SHA-256 values; refuse unsafe paths, changing or unreadable inputs.

Verify full archive readback and restore every selected member into new empty
external scratch before pruning. Compare restored hashes and check all selected
and protected source bytes before removal. Refuse drift or changed selection;
do not weaken the guard. Journal pending/actual removals and verify protected
bytes again afterward. Stop and inspect any interruption before using explicit
recovery. An archive is preservation evidence, not permission to prune more.

## PR 438 Local Archive

The [compact manifest](../resources/tracking-retention-manifest.json) binds
exactly 115 historical generated files / 26,219,104 logical bytes to archive
member names and SHA-256 values. The
[promotion receipt](../resources/tracking-retention-promotion.json) records
copy identities, validation and actual prune accounting. The local archive is:

```text
~/.local/share/ama/tracking-archives/2026-10-24-pr438-hex6oe57/tracking.tar.gz
SHA-256: 06e9c007eaad0d3c9d30eb885176ceae87902cda51ec14130550c7be5a9a5f05
```

Its full inventory is `receipt.json` beside the archive; actual deletion events
are in `prune-journal.jsonl`. All 115 members were restored to `restore-selected/`
and checked against `restore-selected/restore-proof.json` before removal.
The owner-only local archive is not a public artifact or a guarantee of
availability on another machine or in perpetuity. Transfer and verify the
archive and receipt through an approved store before relying on them elsewhere.
The repository manifest alone cannot restore bytes.

Historical handover/review links to the selected previews and two duplicate
decks are now archive-backed, not live-local links. Use the exact manifest
member path to locate the preserved version, including adverse render images;
rendering the corrected deck does not recreate those original findings.
All unselected tracking entries, the current 89-file native build, its original
PDF, current previews and mentor YAML remain in place. Both current duplicate
delivery outputs remain. This reduces checkout files, not Git history or total
storage including the external archive.

From the repository root, verify and restore the exact selection to a new,
nonexistent external directory:

```bash
PYTHONDONTWRITEBYTECODE=1 .venv/bin/python tools/tracking_retention.py verify --repo .
PYTHONDONTWRITEBYTECODE=1 .venv/bin/python tools/tracking_retention.py restore --repo . --output "$HOME/.local/share/ama/tracking-archives/pr438-restore-new"
PYTHONDONTWRITEBYTECODE=1 .venv/bin/python tools/tracking_retention.py check-protected --repo .
```

Restore refuses an existing destination, traversal, link escape and overwrite.
Inspect the isolated restored files before any separately authorized copy back
into a checkout. Old tooling expecting a pruned working-output path requires
that explicit restoration; do not rewrite historical validation as a new run.
The full-snapshot protected check is specific to the unchanged PR 438 snapshot:
later legitimate tracking edits require their own preservation contract, not
a bypass or a false claim that this historical check still passes.

## Durable Reproduction and Evidence

Use the [current capstone source guide](../../capstone/source/README.md)
for the complete 54-slide native/JSON build, retained media and external-output
commands. The [historical native recovery guide](../../capstone/history/cowork-main-presentation/native-recovery/README.md)
describes the earlier six-slide recovery, not the current authoring route.
The [29 October restore map](../../capstone/history/README.md#archive-and-restore)
records the owner's separate finite selection of 15 obsolete capstone exports,
full snapshot readback, selected restoration and protected-byte checks. It does
not expand deletion authority or change the prior PR 438 archive contract.
The [dated build narrative](../../capstone/history/cowork-generated/native-recovery-build-2026-10-24.md)
is a byte-preserved historical copy, including its original paths and commands;
the current source guide supplies the new reproduction commands. The original remains for
append-only log compatibility.

Exactly 12 byte-preserved assurance/PRD files are grouped under
[reports](../research/reports/). Their siblings, original FAIL/Blocked outcomes,
anchors, source dates and embedded original paths are unchanged. Originals
remain in tracking. Promotion is not independent regrading, remediation closure,
current-price research, Finance approval or operational acceptance.
