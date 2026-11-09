# Research: issue 144 queue request-date correction C1 (2026-11-09)

Disposition: executed. Planning readiness: Ready.

* Trigger: independent functional review (request_changes, one High) of frozen head `2619f050fd2cd2eebd649babd45bd07752ba1a6d`, tree `6243ef02e20cb40cf7b134e36c4c324cb415d02f`, base `b46a9ad9a9619db535368d1b2cbbddec8110e122`. Originals preserved byte-for-byte (sha256 `76d5bdf7...eda`, `9fd230dd...418`) under `.copilot-tracking/reviews/2026-11-09/issue-144-independent-functional-review/`. No qualified-human approval exists or is claimed.
* Contract: Microsoft Learn Get Messages, Request headers, fetched 2026-11-09 (page updated 2023-06-27): "Date or x-ms-date | Required. Specifies the Coordinated Universal Time (UTC) for the request." https://learn.microsoft.com/en-us/rest/api/storageservices/get-messages
* Authorize with Microsoft Entra ID (https://learn.microsoft.com/en-us/rest/api/storageservices/authorize-with-azure-active-directory, last updated 2025-04-04, fetched 2026-11-09): the retrieved text shows the Bearer Authorization scheme and an `x-ms-version` example but no statement that lifts the per-operation date requirement. Per-operation documentation is therefore treated as authoritative; the date header is supplied on every call.
* Format: RFC 1123 UTC (for example `Wed, 06 Mar 2019 21:50:50 GMT`), as produced by `email.utils.formatdate(usegmt=True)` in the standard library. `urllib` adds no Date header; current `_call` sends Authorization, x-ms-version and Content-Type only.
* Scope: all operations (receive GET, poison POST, ack DELETE, release PUT) go through `AzureTaskQueue._call`, so a single change covers them. Date is generated per call, like the bearer token.
* Not claimed: live Azure reproduction or acceptance; identity/worker hosting wiring; unrelated review wishlist tests (count boundaries, fresh-token tests) are out of scope by owner direction.
