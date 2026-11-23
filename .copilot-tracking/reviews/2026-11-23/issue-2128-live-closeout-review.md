# Issue 2128 review (2026-11-23, executed once)

Outcome: conformant for scope; open items routed as follow-ups, none reopened here.

* Diff read: `device_provision.py`, tests, pyproject extra, README, research note, index, log. Default behaviour is unchanged (in-memory store); the vault path is opt-in, validated, keyless and fixed-code. A review finding during this pass (vault backend failure at store construction escaped `main` as a traceback) was fixed with a test before closeout.
* Evidence honesty: Key Vault write is stated unproven; stand-in backend labelled; the derived-key limit stated; no criterion ticked.
* Checks: 103 device tests and 12 live-provisioning tests OK, mypy and ruff clean in a clean dev venv. FULL tier gate, hosted CI and independent exact-head review are not done by this worker.
* Cleanup verified: no throwaway hub, vault (purged) or role assignment remains; no secrets in evidence files.
* Follow-ups: Key Vault proof from an in-network runner; bridge `SIM-` and `SYN-` stacks.
