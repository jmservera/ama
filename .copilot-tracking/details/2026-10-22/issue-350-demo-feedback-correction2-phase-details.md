<!-- markdownlint-disable-file -->
# Phase Details: Correction 2

## P01-T01
In `check_case_write`, validate `request.note` is a string if present, derive `note[:500]`, and compare it with the write-response and reloaded contacts after the outcome/channel checks; held note is blocked.

## P02-T01
Add tests: note mismatch with matching snapshots fails; 600-char note truncated to 500 is accepted as consistent (still blocked for durability) and a non-truncated snapshot fails; held note blocks.

## P03-T01
Commit, run one uniquely named full gate with long lock timeout, verify receipt against current origin/main, then push and open a draft PR with Refs #350. No edits during the gate.
