<!-- markdownlint-disable-file -->

# Phase Details: demo-transport-blob-360

Plan: .copilot-tracking/plans/2026-10-22/demo-transport-blob-360-plan.md. Research: .copilot-tracking/research/2026-10-22/demo-transport-blob-360-research.md.

## P01 Blob transport module and wiring

* P01-T01 Add `infra/scripts/staff_blob.py`: constants (`CONTAINER = "staff-results"`, `PAGE_BYTES = 64 KiB` of plaintext items, `MAX_PAGES = 64`, `TTL = 900 s`), `encode_pages(request, result, now)`, `PageStore` (write via injected container client, `put` with overwrite False), `read_result(container, request, now)`. Reuses `StaffJobError` from `staff_azure` via late import to avoid a cycle: define `StaffJobError` in `staff_blob` and re-export from `staff_azure`. Evidence C1.
* P01-T02 Wire controller: `staff_azure.execute` obtains a reader through an injectable `blob_factory(account_url, credential)`; the default builds `ContainerClient` with `DefaultAzureCredential`. After execution `Succeeded`, read; unreachable raises explicit error. Remove tag code and relay capacity gate. Evidence C1, C2.
* P01-T03 Wire worker: replace `publish_result` with Blob write using `ManagedIdentityCredential(client_id)`; request carries `blob` account URL and `container`; keep ARM `Management.call` for restart. Evidence C4.
* P01-T04 Discovery: from the API app env `ZF_BLOB_ACCOUNT_URL`, derive the account, verify via ARM account properties and container, bind `blob_url`. Evidence C2, C3.
* Done when: unit tests for P01 pass.

## P02 Bicep, tests, retirement

* P02-T01 `storage.bicep`: add container `staff-results`, lifecycle rule (delete after 1 day, prefix `staff-results/`). Keep array index references stable (append at end).
* P02-T02 `staff-initializer-rbac.bicep`: replace tag role with Storage Blob Data Contributor assignment scoped to the container; param `includeResultBlob`. Update text-contract tests.
* P02-T03 Rewrite `test_staff_azure.py` relay fake to a fake container; delete tag tests; add new boundary tests.
* P02-T04 Update `cutover-proof.Dockerfile` copy list if modules change.
* Done when: `python3 -m unittest` for infra tests passes.

## P03 Docs

* P03-T01 Add "Private Blob Result Transport (2026-10-22)" section to `infra/README.md` superseding T1 with decisions, trust statement, live prerequisites and the DN4 role-assignment statement; mark T1 superseded without rewriting earlier evidence. Update the in-VNet prerequisites text that mentions result tags.
* P03-T02 Update `docs/architecture/cutover-evidence-pack.md` status line, `docs/reference/log.md` append, README index touch if needed.

## P04 Validation

* P04-T01 ruff, focused tests, full `tools/rpi-checks.py --all` with external out dir, verify receipt, commit, lease push, PR update.
