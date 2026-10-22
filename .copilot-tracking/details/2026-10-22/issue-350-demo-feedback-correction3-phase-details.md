<!-- markdownlint-disable-file -->
# Phase Details: Correction 3

## P01-T01
`check_case_write` uses `CONTACT_CAP = 40`, newest-first `contacts[0]`, length rule `min(len(before)+1, 40)`, and `write[1:] == before[:len(write)-1]`.

## P01-T02
`json.loads(..., parse_constant=reject_constant)` blocks non-standard constants; `latency_ms` must be a finite non-negative non-bool number.

## P02-T01
Fixtures are newest-first with two earlier contacts; add oldest-first rejection, older-contact tamper, 40-cap, NaN/Infinity loader and in-memory latency tests.

## P03-T01
Commit; one uniquely named full gate against current origin/main; verify receipt; push same branch; update PR 436.
