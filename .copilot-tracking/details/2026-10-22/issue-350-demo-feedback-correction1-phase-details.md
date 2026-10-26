<!-- markdownlint-disable-file -->
# Phase Details: Correction 1

## P01-T01

`check_case_write` keeps its input and denial checks. After the contact count checks it compares the last write-response contact to the stored form of the request and to the reloaded contact (all keys), then raises `blocked` instead of returning `pass`. A held outcome in the write response is `blocked`.

## P02-T01

Update the valid-bundle test (durability blocked, other checks pass, overall blocked); replace the valid-write test; add mismatch, any-field and held tests; the fixture's reload no longer aliases the write contacts.

## P03-T01

Run focused unittest and Ruff, commit, run `tools/rpi-checks.py --all` with a new external out directory and long lock timeout, run `--verify-receipt` against current origin/main, then push and open a draft PR with Refs #350.
