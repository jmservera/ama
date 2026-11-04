# Issue 185 research (2026-11-04, r3)

* Disposition: executed (delta). Planning Readiness: Ready for a records slice.
* Merged delivery checked: #647 (plan, provision, teardown against fakes), #849 (offline credential rotation with overlap then revoke), #498 and #508 (private keyless transport and bounded streaming; no device management). No open PR for #185.
* Criterion 2 (one identity per stock home) is ticked and proven by tests in `src/core/tests/test_device_identity.py`.
* Criterion 1: decision is proposed; owner confirmation of credential ownership is not recorded.
* Criterion 3: proven only against fakes; live Key Vault issuance and storage need the owner and Azure.
* Criterion 4: proven only against fakes, including after rotation; live teardown needs Azure.
* Another code slice would be live Registry and Key Vault adapters, which touch credentials and Azure and need owner approval. Not a small offline slice.
