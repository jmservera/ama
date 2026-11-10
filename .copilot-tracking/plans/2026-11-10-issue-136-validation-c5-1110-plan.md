---
title: Plan for issue-136-validation-c5-1110
description: Clear the selected Ruff, format, mypy and diff-check failures on the modified resident test module
ms.date: 2026-11-10
---

## Objective

Make the already modified `infra/tests/test_resident_demo_deploy.py` pass its selected Ruff check, Ruff format check and mypy diagnostic without ignores, casts or weaker tests, and remove the new blank line at EOF of the C4 changes record after preserving its original bytes.

## Phases

* [ ] Phase 1: Edit the test module per the details file (line 133 wrap, class attribute annotations, `importlib` import, `compiled()` return type).
* [ ] Phase 2: Preserve C4 original changes bytes externally (done in research: `proof/c4-changes-original-e3.bytes`), then remove only the trailing blank line and add a C5 format-only note in the new C5 changes record.
* [ ] Phase 3: Run the selected checks (Ruff, format, mypy for this module, failing CI test, the module, policy and container-contract tests, offline Bicep build and lint, the four mutations, diff-check) and record raw outputs and exits.
* [ ] Phase 4: Review once, commit with the privacy-safe identity and Copilot trailer.

## Selected checks and baseline context

* Required and must pass: Ruff check and format for the resident module; mypy with zero errors attributed to the resident module; the failing CI test; the resident module; `test_bicep_policy`; `test_container_contract`; offline Bicep build and lint for main, guard, containerapps and resident-demo; four mutations all detected; `git diff --check`.
* Supplemental and unwaived: mypy over `test_bicep_policy.py` still reports its three known baseline errors; this is not a strict pass of all infra.
* Not run: full or `--changed` gate, image rebuild, startup tests, SQL, cloud, model.

## Constraints

* Product path only `infra/tests/test_resident_demo_deploy.py`. No Bicep, API, Core, Docker or runtime change.
* Image `sha256:d6d6fe32...`, `src` tree and `infra/modules` are historical C4 evidence for unchanged inputs; verified by tree and blob equality only, no new startup claim.
* If the module cannot reach zero diagnostics in this scope, hold.
* No C4 outcome, review, event or witness record is rewritten; the C4 `verify` exit 1 and the lost first C4 E501 output stay permanent qualifications.
