# Issue 358 research (2026-11-04)

* AC1 expired-credential guard test: delivered (#374, #583; tests at infra/tests/test_setup_entra.py, test_expired_credential_rotates_without_removing_in_use_old_credential).
* AC3 four-file conflict with #352: delivered (#374, delegating main() kept).
* AC2 Key Vault secret preservation: offline mocks delivered (#374, #583); bounded synthetic round-trip merged in #417. Live populated existing-resource round-trip not run: production apps have configuration.secrets null (issue comment 2026-10-19), so no populated baseline exists.
* Re-checks already merged: #683, #723, #816. A further re-check adds no evidence.
* Local re-run 2026-11-04: test_setup_entra.py, 124 tests OK.
* Planning readiness: Ready for a no-code disposition. Remaining criterion needs an operator-provided authorized populated nonproduction target (cloud write, infrastructure tier).
