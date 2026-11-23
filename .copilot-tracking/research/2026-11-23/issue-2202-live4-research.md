# Research: issue 2202 live4 (2026-11-23)

Disposition: executed.

* Issue 2202 has four unticked criteria. Prior passes (live3 and earlier) left unproven: image source commit for simulator and receiver, rollback note, and a repeatable deployment receipt.
* Live read-only probe 2026-11-23: all three apps and both live jobs carry ZF_CONTAINER_HARDENING=enforced; no ZF_BUILD_COMMIT in the template env; simulator image digest 295164ca..., receiver 541068a6..., API 0000055 Healthy.
* tools/demo_preflight.py checks revisions, jobs, health and counts but not image digests or hardening, so criteria 1, 2 and 4 depend on hand-run az commands.
* Plan: extend demo_preflight with a read-only deployment check (image digest, hardening value, agents app) plus tests; run it live for the receipt.

Planning Readiness: Ready.
