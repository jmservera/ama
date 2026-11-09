# Research: finance parent held-export manifest checkpoint (#440, #96)

Date: 2026-11-05. Disposition: executed. Planning Readiness: Ready.

## Identities

* Child branch docs/finance-export-checkpoint-440 at dec700c7af46778140bf5c46d4df932832a31f11 (equals origin/feat/discovery-assurance-integration-123, the declared target).
* Finance parent feat/finance-integration-93 at 0472fd5d5625bb610b5ac65ad177026953802830, tree 268ead3a098f2320c0fba1a16aed14dd68a7fbe2.
* Main bb3a3b03cb94eef6c06ae4b12d07cfe7bbdef43f, tree 5c2988b71aec609b007b41f408685d54e2c28e0d (unchanged at resolution).
* PR 1223 (c738fde9) squash-merged only into the finance parent. Receipt 07ae is historical evidence at c738; tree equality is not a new run at 0472.
* BRD 0.21.0 draft, PRD 0.21.0 in-review, ADR 0003 accepted with owner amendment, ADR 0006 accepted; blobs unchanged. Draft or in-review is not approval.

## Source facts (finance parent, read via git)

* BODY_KEYS has 11 keys and no history. A missing key makes export_freshness return Invalid with the regenerate-Held action.
* Review history is already built and evidence-visibility checked; reviewer email and reasons (up to 500 characters) are a privacy point for the DPO or data owner.
* No consumer of form_export exists outside its tests and the core README; the store persists no saved copy.
* The integrity hash is content SHA-256, not a signature or delegation.

## Observations

* Archived pinned source to /tmp/f440fin; three form test modules, 40 tests OK, scrubbed env, bytecode off, no heavy admission.
* /tmp/g96-r14-review1-1105/checkout absent, so not used.

## Boundaries

External r15 research and the residual-readiness note are proposals, not instructions. No defect confirmed; no human approval, whole-96 or whole-440 claim.
