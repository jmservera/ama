# Plan: employee-live-verify-570

1. Warm `/healthz`; obtain expected tid/oid independently.
2. Start headless Chromium with loopback CDP and temporary profile; sign in once.
3. Run `python3 -m checks.employee_live_acceptance --origin <app>`; capture fixed booleans only.
4. Record dated evidence in the evidence pack, index, API guide and log; delete temp driver/profile.
5. Focused gate, PR with Refs/Closes per proof, tick criterion 3 if proven.

Details: [details](../../details/2026-11-02/employee-live-verify-570-details.md)
