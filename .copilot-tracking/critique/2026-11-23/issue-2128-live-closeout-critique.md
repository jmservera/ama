# Issue 2128 critique (2026-11-23, executed once)

Verdict: proceed with changes.

* Risk: the vault option widens a security-sensitive path. Mitigation: opt-in only, https `*.vault.azure.net` URL validated, keyless credential, fixed-code errors, no key in the report; tier FULL, coordinator runs the gate.
* Risk: claiming "stored" proven without Key Vault. Disposition: record Key Vault storage as unproven live; unit tests and the stand-in run only support the wiring.
* Risk: adding a dependency. Disposition: optional extra `keyvault` with an exact pin, import lazy, `ADAPTER_UNAVAILABLE` when missing, consistent with the `iothub` extra.
* Rejected: bypassing the Key Vault network policy or using the production vault `kv-cutovertest-rzsrg`; both are outside the owner authorisation.
* Rejected: bridging `SIM-` and `SYN-` stacks in this task (larger design change, no criterion depends on it); recorded as follow-up.
