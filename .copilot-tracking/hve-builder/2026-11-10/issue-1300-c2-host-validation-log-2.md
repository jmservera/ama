# Host mechanical validation log 2: issue 1300 C2 (2026-11-10)

Log 1 is preserved unchanged. Validator: generic Low profile, non-mutating, requested gpt-6-luna (the canonical Low first model is GPT-5.6 Luna; a different requested id was used, so no canonical-profile claim). Head eef054c78835e292ddadbdbd2c229ed19a3bd724.

| Check | Result |
| --- | --- |
| git diff --check a61bebe6b HEAD | Pass, exit 0 |
| 31 unit tests | Pass |
| ruff check, ruff format --check on the two tool files | Pass |
| helper --help | Pass, exit 0 |
| Agent frontmatter bytes identical to a61bebe6b | Pass (opaque comparison only) |
| Agent diff in step 5 only | Changed ranges 582-599 and 703-717, inside step 5 (574-725) by lead inspection; the validator did not verify scope |
| Referenced helper exists, blob 3e8f21c5 | Pass |
| Unexpected mutation | Pass: status identical before and after (baseline /tmp snapshot taken after the author-owned commits, so author-owned changes are excluded by construction) |

Erratum to log 1 Check 7: that Deferred was caused by the author's own visible state update, not a validator mutation, and is not a Pass. This log's Check 7 ran against a pre-run snapshot and is the first real mutation check.
Not performed: YAML or schema lint, plugin/collection wiring (N/A, repository-specific artifact, no distribution added), hosted CI (pending after publication).
