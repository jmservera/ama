<!-- markdownlint-disable-file -->
# Research, plan, details and critique: C2 fingerprint label correction (task 440-m2-c2-fingerprint)

Written 2026-11-10T01:21Z (`date -u` 01:20:23Z at start). Source: frozen candidate `8403cabfde08fdb08f7fab019f4fabacfd4bb721`, main pin `32221a845` unchanged; no main merge, rebase or push. Correction cycle C2 of 5 (C1 was the PR 1341 row wording); three remain; no other counter is reset (#1288 E counter untouched).

## Research (executed, read-only)

* The coordinator's defect was verified in the raw VM-local `h2.json` (read, not executed; harness and wrapper not run): `first.binding_sha`, `B.binding_sha` and `C.binding_sha` are all `b4791e0c22b1f1be`; `raw0.task_body_sha`, `raw_B.task_body_sha` and `raw_C.task_body_sha` are all `cfc0f0a9922fd69f`.
* Harness meaning (`harness_h2_matching_context.py`): `task_body_sha` is a fingerprint of the stored task body (line 55); `binding_sha` is a fingerprint of the JSON-serialised release or flag binding object read in the observation (line 95), compared first-versus-B/C (line 126 and 150). They are distinct quantities.
* The evidence-pack H2 values paragraph (section "Quality M2 current-main qualification") wrote "the same task state and body digest `b4791e0c22b1f1be`". That mislabels the binding fingerprint as the body digest. The equality result is unchanged: both fingerprints are equal across first, B and C. No source, persistence or runtime defect is inferred. Neither value is cryptographic byte identity (truncated 16-hex fingerprints).
* The same value appears in the original research record `2026-11-10-quality-m2-record-440-research.md` (equality table). That original record is preserved; this erratum supersedes its label. The index paragraph and log entry do not repeat the mislabel.
* Wording check requested by the coordinator: actual-model, IoT Hub, Azure SQL and OS or VM restart are NOT RUN or blocked or admission-pending, never an owner-approved deferral. The section's evidence-class sentence says "deferred is the actual-model walkthrough, IoT Hub, Azure SQL and OS restart" and the requirements table says "deferred and gated"; "deferred" can read as an approved requirement deferral. These are in scope as the same class of wording accuracy and are corrected to "not run, admission pending".

Planning Readiness: Ready.

## Plan and details

* Phase 1: this record, state, then commit before editing.
* Phase 2: edit only (a) the H2 values paragraph (state both fingerprints), (b) the deferred wording in the evidence-class sentence and the gaps table row, (c) add a short erratum bullet to the section's errata list. Earlier sections, original records, README paragraph and log entry unchanged (they do not repeat the mislabel).
* Phase 3: pure-docs validation (links, anchors, ASCII, allowlist diff). No runtime.
* Phase 4: changes and review records, final state, local commit, handoff.
* No nested agents (owner direction), so the single critique and single review are performed inline by me, recorded below.

## Critique (one pass, inline)

* Scope creep risk: the deferred wording edit is justified by the explicit owner request that these stay NOT RUN or blocked; limit it to those phrases.
* Risk of rewriting H2 observation or the prior Conformant review: avoided; the C1 review record stays as is, with the erratum recorded in the C2 changes and review records.
* Verdict: proceed; findings applied directly, none conflicts with an owner decision.
