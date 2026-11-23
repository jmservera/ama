# Review (2026-11-23), executed once

Outcome: conformant for scope (classifier, tests, evidence note). Boundary: the two new infra files, research note, index and log.

* Tests fail without the tool (module absent) and cover disabled-vs-enabled, missing, string-typed flag, output redaction, Bicep name drift and CLI errors.
* Coverage is never reported as proven; no criterion is ticked.
* No secrets or ids in output or notes; Azure read-only, nothing to delete.

Routed later work: enabling job/IoT/poison rules needs an approval reference and, for poison, a verified signal and drill (owner-gated); workbook render needs private-link access; named alert owners are a human decision.
