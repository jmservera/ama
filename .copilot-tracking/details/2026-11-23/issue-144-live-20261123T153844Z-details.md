# Details: issue 144 live (2026-11-23)

Phase 2: audit_specs checks ZF_CONTAINER_HARDENING == enforced per container; audit_status parses /proc/1/status for non-root, NoNewPrivs 1, zero CapInh/Prm/Eff/Amb, reports CapBnd and root mount options.
Phase 3: unit tests for passing and failing specs and statuses, rw root reported, CLI exit codes, using the 2026-11-23 live receipt values.
