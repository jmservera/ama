<!-- markdownlint-disable-file -->
# Details: Issue #104 controlled-record non-mutation proof

* Plan: [104-controlled-nomutate-0230-plan.md](../../plans/2026-11-14/104-controlled-nomutate-0230-plan.md)

## P1 Fixture

* Subclass `test_assistants.Base` (SQLite `SqlStore`, five assistants, release fixtures). Provider gets `consumption = None` and an endpoint so chat runs; a mode switch returns chat JSON or an assistant proposal.
* Patch `chat_admission`; set the three synthetic chat approval variables.
* Seed over HTTP as named roles: technical design and assessment sign-off, resident decision, grant opening, hazard raise with Home hold, ranking publication.

## P2 Snapshot

* Raw SQL: `cases` rows (including body, rowversion, stage, owner, closed, rank key, funding status), `meta.procurement`, `recommendations`, `staff`.
* Field extracts: hazards, decision, technical sign-offs, finance, grants; ranking map and archive file bytes.
* Excludes `meta.seq`, audit, chat and assistant tables.

## P3 Tests

* Chat: adversarial prompts for thread and unstored routes, hostile and supported replies.
* Assistants: invoke, execute, verify, accept, edit-accept, reject for all five; proactive scan; unknown approve/execute routes refused.
* Control: an authorised human hazard action changes the snapshot.
