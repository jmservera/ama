<!-- markdownlint-disable-file -->
# Critique: #185 keyless Azure IoT Hub Registry backend plan (single pass)

Executed once 2026-11-10 (readback `date -u` 02:38Z) by the implementing agent as an adversarial read of the [plan](../2026-11-10-iot-registry-azure-185-1110-plan.md) and [details](../../details/2026-11-10-iot-registry-azure-185-1110-details.md) against the [research](../../research/2026-11-10-iot-registry-azure-185-1110-research.md) and the owner brief. No nested agent was used (brief). Verdict: proceed with amendments. All findings are compatible with confirmed decisions and applied directly; none needs a user decision. The critique is not repeated for this task.

## Findings and dispositions

| # | Finding | Severity | Disposition |
| --- | --- | --- | --- |
| 1 | The conflict code `IDENTITY_EXISTS` is also produced by a 409 whose cause is not proven to be an existing device. | Low | Applied: rename to `IDENTITY_CONFLICT`. |
| 2 | Lazy manager creation is not guarded against concurrent first use; two callers could build two owned managers and leak one. | Medium | Applied: a lock around lazy creation and close. |
| 3 | If the list payload omitted `statusReason` (unobserved), `list_run` would return an empty or short set although run-owned enrolled devices exist, so the teardown post-delete verification and the provision active-run check would falsely pass. | High | Applied: any enrolled ID that is listed without a string `statusReason` is confirmed by one bounded read (at most `MAX_DEVICES` reads); a failed confirmation raises `UNAVAILABLE`. Residual, documented: a non-enrolled marked device hidden by an omitting payload cannot be found. A test with a payload that omits `statusReason` is added. |
| 4 | Create-only protects against overwrite, but a concurrent process creating the same enrolled ID with the same run marker between the active-run check and `create` would be classified owned by `device_identity` and rolled back by this attempt. `device_identity` serialises per process only. | Medium | Not fixable inside the allowed boundary (cannot change `device_identity`). Documented in the README as an open limit: one process per run ID; cross-process same-run contention is not fenced. |
| 5 | An injected pre-built client may already have an initialised HTTP session, so the zero-retry binding may not apply to it. | Low | Accepted and documented: every write is conditional, so a transparent retry cannot overwrite or delete another identity. The bound is guaranteed only for the adapter-built manager. |
| 6 | The import-effects subprocess test needs the in-process `sys.path` to find the worktree source. | Low | Applied: pass `PYTHONPATH` built from `sys.path`. |
| 7 | `disconnect_sync` on a never-opened AMQP client and `protocol.close()` are unverified. | Low | Applied: the owned-cleanup test uses the real manager and asserts the real calls complete and the adapter refuses later calls. |
| 8 | Status classification must not rely on `HttpOperationError` identity (msrest import) nor on exception text. | Low | Already in the design (duck-typed `.response.status_code`); kept, with a test for non-HTTP exceptions. |

## Checks that passed

* Create-only is established by the documented `If-None-Match: *`, not by a prior-absence read; the stop condition (no supported create-only semantics) does not trigger.
* No wildcard or unconditioned destructive path exists in the design; the SDK default ETag `"*"` is never reachable.
* No change to the existing protocol, CLI or any out-of-scope file is required; no scope expansion is needed.
* Dependency additions are an optional extra and a dev pin; `six` is required because it is undeclared by the SDK.
