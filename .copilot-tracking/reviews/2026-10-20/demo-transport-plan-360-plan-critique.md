<!-- markdownlint-disable-file -->
# Plan critique: demo-transport-plan-360 (original, one pass)

Executed once by an independent rubber-duck agent on 2026-10-20 against the plan, research and phase details. Verdict: **Revise**. Not repeated. All findings are compatible with confirmed owner decisions and were applied directly (no significant/divergent user decision needed).

| ID | Severity | Finding | Disposition |
| --- | --- | --- | --- |
| C1 | High | AEAD proves possession of the per-run key, not independent worker authentication | Applied: design states hard trust assumption, downgrades claim, adds decision gate DN5 for attestation |
| C2 | High | Image/script/manifest binding is self-asserted; repository hashes do not prove image contents; no job/execution identity binding | Applied: exact job resource ID, execution ID and image digest are controller-held acceptance inputs; image-to-source provenance recorded as unresolved gap until verified build provenance exists |
| C3 | High | No threat model/checklist for principals with tag-write or resource-write authority | Applied: threat table and checklist rows for effective RBAC inventory before/after, DoS acceptance, stop on unexpected writers, evidence preservation |
| C4 | Medium | DN1 too narrow for management-plane disclosure | Applied: DN1 expanded into a privacy/security approval gate listing metadata and surfaces |
| C5 | Medium | Terminal-response contract and concurrent-mutation tests missing | Applied: single accepted snapshot rule, no hidden retry, ambiguous outcome states, extra offline tests |
| C6 | Medium | Checklist not tied to relay-specific evidence/stop conditions | Applied: relay-specific evidence rows with stop outcomes |
| C7 | Low | Not-reachable vs not-viable; in-VNet controller alternative | Applied: option T8 (private-connected controller reading a private store) recorded as out of current scope, costed later |
