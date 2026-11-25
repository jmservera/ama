# Issue 107 r14 research

Disposition: executed. Planning Readiness: Ready.

Goal: record five release records on the demo API (POST /api/assistants/releases) then run the merged real-AI harness once, hard cap 200k tokens.

Findings (evidence in `evidence/107-live-r14/probe1.json`):

* Live GET /api/assistants (signed-in employee) exposes each assistant's runtime `binding` (13 bound fields), serving model `gpt-4.1-nano-2025-04-14`, deployment `standard`, endpoint `aif-cutover-test-rzsrg`. A release must equal it exactly.
* The live gate (`record` in `assistant_release.py`) needs: role Retrofit Programme Manager, email in `ZF_ASSIST_RELEASE_APPROVERS`, `evidence_class: actual` for live admission, named `approved_by` and `named_approval_id`, approved monitoring thresholds, evaluation summary frozen to the evidence digest, consumption config.
* `src/api/checks/assistant_real_ai_acceptance.py` has no network adapter in its CLI; `run()` takes an injected `call`. `heldout_aoai.make_provider` (az-cli token) is the repository's provider adapter and returns the usage envelope.
* Approval attribution: owner decision 2026-11-18 and 2026-11-25 (all AI approved for the demo). Approver name is the project owner; this is a demo attribution, not OQ-017/018/019 clearance.

Plan: build bodies from `tests/release_support.fixture` with live binding and owner approval, POST five, re-read listing, run harness once via an evidence script (no src change).
