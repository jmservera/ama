---
title: Plan for issue-136-c5-technical-retry-1110
description: Clear selected Ruff, format, mypy and diff-check failures on the modified resident test module
ms.date: 2026-11-10
---

## Objective

Make `infra/tests/test_resident_demo_deploy.py` pass its selected Ruff check, format check and mypy without ignores, casts or weaker tests, and remove the trailing blank line of the C4 changes record after its original bytes are preserved (done externally).

## Phases

* [ ] Phase 1: Edit the test module per the details file.
* [ ] Phase 2: Remove only the C4 changes record trailing blank line; state it as format-only in the retry changes record.
* [ ] Phase 3: Run the selected checks and record raw outputs and exits.
* [ ] Phase 4: Review once, commit with privacy-safe identity and Copilot trailer.

## Selected checks

* Must pass: Ruff check and format for the resident module; mypy with zero errors in the resident module; the failing CI test; the resident module; `test_bicep_policy`; `test_container_contract`; offline Bicep build and lint for main, guard, containerapps and resident-demo; four mutations detected; `git diff --check`.
* Supplemental, unwaived: three baseline mypy errors in `test_bicep_policy.py`.
* Not run: full or `--changed` gate, images, startup tests, SQL, cloud, model.

## Constraints

* Product path only the resident test module; no Bicep, API, Core, Docker or runtime change.
* Image `sha256:d6d6fe32...` and src are historical evidence for unchanged inputs, shown by tree and blob equality only.
* Hold if zero diagnostics is unreachable within scope. No C4 or first-C5 record is rewritten.
