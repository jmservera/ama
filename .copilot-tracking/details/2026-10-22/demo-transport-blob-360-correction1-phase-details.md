# Phase details: #360 correction1

## P01 Credential binding

* P01-T01 In `staff_azure.py` add `ProfileCredential(cli)` with `get_token(*scopes, **kw)`: map scope `https://storage.azure.com/.default` to resource `https://storage.azure.com/`, call `cli.call(["account","get-access-token","--resource",res])`, accept `expires_on` (epoch) or `expiresOn`; any failure raises generic `StaffJobError` without detail. Done when the adapter returns `AccessToken` and never logs.
* P01-T02 `default_container(url, cli)` passes the adapter plus `connection_timeout=5, read_timeout=15, retry_total=2`; `execute` passes `cli`.

## P02 Operation budget

* P02-T01 `staff_blob._bounded(fn, deadline)` runs fn in a daemon thread and joins with remaining time; timeout raises `StaffJobError` (unverified wording).
* P02-T02 `preflight(container, request, deadline=None)` and `read_result(..., deadline=None)` wrap list and each download+readall in `_bounded` with defaults PREFLIGHT_BUDGET=45 s and READ_BUDGET=45 s from call start, never beyond a supplied deadline.
* P02-T03 `execute` passes `min(job deadline, now+budget)` for reads; cleanup block unchanged.

## P03 Tests, docs, validation

* P03-T01 Tests in `infra/tests/test_staff_azure.py` per AC1/AC2 (real ContainerClient construction; no network).
* P03-T02 Update `infra/README.md` private-Blob section, evidence pack, `docs/reference/log.md` (append), `ms.date` where the file frontmatter requires.
* P03-T03 Run infra tests, ruff, mypy; commit; one gate `run6-correction1`; verify; push.
