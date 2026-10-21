<!-- markdownlint-disable-file -->

# Phase Details: issue-223-human-review-protocol

## P01 Author protocol section

* P01-T01 Insert "Meaningful human-review protocol (#223; proposed, Not run)" after "Priority repetition accounting (#108, 2026-10-18)" and before "## Validation record" in src/agents/README.md. Evidence: research C6, C9.
* P01-T02 Content: status block; dependencies; case classes table (ID, class, example, expected disposition, blocks gate); controls; automation-bias design; retention fields mapped to existing review record (C7); OQ-017 evidence table; denominators; effort model; comparators; outcome rules; non-claims.
* Completion: every threshold/sample/role carries PROPOSED or UNFILLED; no named person.

## P02 Index and log

* P02-T01 Add one row to docs/reference/README.md near other issue inspection rows; P02-T02 append dated log entry at end of docs/reference/log.md without touching earlier entries.

## P03 Focused validation and commit

* P03-T01 git diff review, link check of new anchors, ASCII/em-dash grep; run focused existing agents ai_eval tests to confirm unaffected (docs only).
* P03-T02 Resolve gh api user, set local email, commit with Conventional Commit plus trailer. No amend, push, gate.
* Test ownership: none added; removals none; generated targets none.

## C01 Corrective lockfile reuse

* Files: src/core, src/api, src/importer, src/orchestrator requirements.txt only; byte-identical to a3257c71 (git diff --cached against that commit empty per file). Tracking files of that commit deliberately not imported.
