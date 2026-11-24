# Issue 116 live r14 plan and critique (2026-11-24)

1. In heldout_aoai `call`, run core `approved_payload(system, prompt)` first; on InputRefused return `outcome=failed` with no HTTP request.
2. Test: oversize prompt and non-string system make no opener call and return failed; normal request unchanged.
3. Run agents tests, ruff, mypy; write r14 evidence note, index and log.

Critique (executed once): empty system is currently allowed ("" omitted), approved_payload accepts "" so compatible. Reusing the core allowlist avoids a parallel validator. Accepted, no conflicts with decisions. Tier FULL (src); rpi-checks --all not run.
