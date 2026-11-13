---
title: Issue 96 saved export check amendment changes
description: Changes record for the corrections made under the independently critiqued amendment plan
ms.date: 2026-11-12
---

## Relationship to the earlier candidate

Commit `bbe80e563` and its self-review artifacts are unchanged prior candidate evidence. The corrections below were made after the independent critique (`...-amendment-2255-critique.md`) of committed plan `656581e7a`, in the order plan, critique, change.

## Changes

* `src/api/src/zava_forward/api/server.py`: the check route catches `TypeError` from the core comparison (a self-consistent forged copy with mixed field id types reproduced a 503 before this change) and answers the core `Invalid` result for an unusable copy. No core change.
* `src/api/tests/test_form_held_download_api.py`: three tests. Forged copies (mixed id types answer Invalid; an extra fabricated field with a recomputed digest is compared as supplied and stays Current, documenting that the digest is not provenance; no state change). Binding (existing other case and missing draft with matching ids answer Unavailable with no field details; path/body mismatch 400; no state change). Anonymous 401, empty body 400 with `no-store`, role revocation after a successful check.
* `src/api/README.md`: states the digest is not provenance and `Current` is conditional on the supplied copy, gives the actual precedence, and qualifies the no-write wording for shared sign-in identity linkage.

## Critique dispositions applied

CR-1 to CR-4 applied as described. CR-5: shared CSRF, view-only and sign-in suites (`test_auth`, `test_entra_authoritative`) and `test_keepalive` run; error responses on this route carry `no-store` (asserted for the 400 case).

## Divergences

* The critique asked for anonymous, revocation and CSRF/view-only evidence on this route. The trusted-proxy CSRF and administrator view-only paths are shared gates ahead of routing and are not re-tested on this route; their shared suites were run instead. Recorded as a limit, not a new proof.
* The extra-fabricated-field outcome (Current) is existing core behaviour and is documented and tested, not changed.

## Validation (owner demo focused tier; log `files/rpi-96-api-replan-2255-evidence/focused-run.log`)

API `test_form_held_download_api` 14, `test_form_staging_api` 14, `test_role_endpoint_inventory` 24, `test_keepalive` 4, `test_finance_grants_screens` 20, `test_role_screens_conformance` 11, `test_auth` 41, `test_entra_authoritative` 36; core `test_form_export` 11, `test_form_dependencies` 10; ruff check and format, mypy strict on the changed test module, `git diff --check`. All passed, using the owned pip venv with editable installs, no uv, no source-package PYTHONPATH. Not run: SQL Server, browser, hosted CI, axe, full or `--changed` gate, any cloud or model call.
