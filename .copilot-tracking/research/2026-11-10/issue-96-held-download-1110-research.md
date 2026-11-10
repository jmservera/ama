---
title: Issue 96 served Held draft download consumer research
description: Prospective research for the initial HTTP and funding-screen consumer of the existing Held form export
ms.date: 2026-11-10
---

## Identities and scope

* Worktree `issue-96-held-download-1110`, branch `feat/demo-held-form-download-96-1110`, head and base `fe59ef56a0084dd975fd7e5c342670bb8f788fb0` (tree `9cacc7bddeb88f19eafa0d95cfb41d7735b0daa2`), target `main`. Clean at start. Parent #93 previous integration merged (1345); no active #93 PR to reuse.
* Task: the INITIAL, previously unprovided HTTP and funding-screen consumer of the existing core `form_export.draft_export`. It is not a repair of the core exporter, history or dependency code. Prior r7, r12, r14 and r16 adverse history is preserved and this task claims no correction allowance; the post-review correction balance is UNKNOWN and no fresh-five or source-repair grant is assumed.
* Source of the candidate: Root admission `demo-source-admissions-229-96-97-1110.md` (static, execution-unqualified) and `freshadmission-96-issue-1110.json`. Both are leads, not evidence of current behaviour; this research re-reads the source.
* Synthetic demonstration only. Real templates, actual-data export and operational submission remain unapproved. The owner already decided full history for synthetic data only and regeneration of old copies, so those are not reopened.

## Consumed checkpoint (not fresh execution)

* The merged-wave #440 checkpoint (cutover-evidence-pack.md lines 6067 to 6140, supplied by Root) records finance history and legacy-invalid-and-regenerate R1 core 67 and R2 API 14 as locally observed, with finance independent expansion CONTINUE without live funder acceptance. It is historical and is not treated as a fresh execution on this main. Closure, human and SQL Server gates stay retained. No model or approval authority derives from it.
* Root's source comparison (actual 96afce to current main) reports `forms.py`, `form_review.py`, `form_export.py`, `form_dependencies.py`, `server.py` and `test_form_staging_api.py` unchanged and `role-screens.js` changed only by later operator work, disjoint from the funding hunk. The full `src` tree has moved, so the baseline below is fresh and focused.

## Fresh focused baseline (this head, owned external venv, no source change)

* Venv `venv-96-held-download-1110` under the Root files folder with editable installs of this worktree's `src/core`, `src/api` and `src/agents` (`--no-deps`, system packages). It was needed because the default interpreter resolved `zava_forward` to another checkout. No global or other environment was modified.
* `ZF_DATA` pointed at an owned empty synthetic folder; no private dataset was read.
* Core (unittest discovery per module): `test_form_export` 9, `test_form_dependencies` 10, `test_form_review` 23, `test_form_staging` 17, all OK.
* API: `test_form_staging_api` 14 OK; `test_finance_grants_screens` 19 OK; `test_role_endpoint_inventory` 23 OK; `test_role_screens_conformance` 11 OK.
* One of my own invocations used dotted module names and failed on `import test_form_review`; that is an invocation error, retained as `baseline-core-attempt1-bad-invocation.log`, and not a product failure. Discovery runs all passed.
* Result: no baseline exporter or product failure and no earlier failed same-served-consumer candidate found in the supplied lineage. Proceed; no STOP.
* Logs and exit files are under `ROOT/phase96-held-download-evidence-1110/run/`.

## Source findings

* Exporter: `form_export.draft_export(store, user, case_id, draft_id)` takes `store.lock`, calls `forms._actor` (current Finance view, resident-record view, reason-view and document read rights), `store._case` (KeyError for an unknown case) and `form_review._draft` (KeyError for another case's or unknown draft). Document-unavailable returns `status="Unavailable"`, `reviewed=False`. Success returns the fixed contract: `status="Held"`, `reviewed=False`, `submission="Not submitted"`, `eligibility="Not assessed"`, `content_sha256` over `BODY_KEYS` including `history`. It writes nothing.
* No `form_export` reference exists in `src/api`. `server.py` admits `/api/form-schemas` and exactly four-part `/api/cases/{id}/form-candidates|form-review` for GET (about lines 531 to 537) and `_forms` (about 1116 to 1143) maps `DocumentStoreError` 502, `ConflictError` 409, `PermissionError` 403, `KeyError` 404, `ValueError` 400, other 503 with safe messages. This is the single place to reuse.
* `_send` merges `SECURITY` headers, whose `Cache-Control` is already `no-store`; `extra` can override with `private, no-store`. `do_HEAD` delegates to `do_GET`; HEAD would run the export without a body, which is read-only and acceptable.
* `fundingDraftPanel(draft)` (role-screens.js about 1280) renders a draft, with `draft.status === "Unavailable"` handled first and the readable review gated in the funding screen by `drafts` and `decision_holds`. The existing catalogue CSV link (`/api/form-schemas.csv`, `download` attribute, "Download for Excel") is the in-page precedent for a native anchor download. `draft.input_version` and `draft.draft_id` are present in each `_report`.
* The role endpoint inventory test (`test_role_endpoint_inventory.py`) greps `server.py` for quoted `/api/...` routes and requires each to be in `GET_ENDPOINTS` or `POST_ENDPOINTS`; a new route string needs an explicit entry, not a waiver. Its regex (`[a-z./-]+`) may not see a route built from parts, so an explicit entry for the new path is wanted either way.

## Synthetic and demo guard research

* Existing guards found: `ai_registry.demo_activation_honoured` (`ZF_CHAT_DEMO_ACTIVATION` exact value plus `ZF_DEPLOYMENT_PROFILE=demo`) is specific to the owner's chat decision of 2026-11-03 and carries chat-specific disclaimer and approval text. Reusing that switch would borrow an owner authority that does not cover form export, so it is not reused as the enablement. `ZF_DEPLOYMENT_PROFILE=demo` is a neutral demo-profile signal that Bicep sets on the demo API.
* The store has no dataset provenance marker (no `is_synthetic` for case or draft data), and the existing form-review GET already serves the same history under the same rights with no guard.
* Conclusion: no suitable general synthetic-data guard exists. Plan a minimally scoped, explicit, default-OFF enablement owned by this consumer: the route is served only when `ZF_FORM_HELD_DOWNLOAD` is exactly `synthetic-demo-only` and `ZF_DEPLOYMENT_PROFILE` is `demo`, and never when the provider is `trusted-proxy` (real Entra identities). The environment is read per request so the default is deny. No Bicep, deployment or activation change is made; only owned synthetic fixtures set it in tests.
* Honest limit: the code cannot prove the loaded data is synthetic. The switch is an operator attestation, as for the existing chat demo switch. This is documented in the plan and handoff; it is not a claim of data approval. Actual employee or resident export stays unenabled by default and unauthorised.
* Decision on STOP: current rights, mode and default-OFF can all be enforced inside the server without scope expansion, so there is no contract-gap STOP. Provenance of the data remains a stated limit.

## Design findings

* Route: `GET /api/cases/{case_id}/form-review/{draft_id}/held-export`, six path parts. Dispatch inside `_forms` so error mapping is shared; the path guard admits only that exact shape.
* Disabled state, wrong shape and unknown trailing segment return the existing generic 404; wrong methods reach the existing POST fall-through (verified in tests).
* Snapshot semantics: each GET builds a fresh export under the lock, so the file is the review at download time. The file carries its own `input_version` and `content_sha256`; the screen shows its own `input_version`. The note states the download reflects the review when it is generated, which may differ from the version shown on screen.
* Unavailable export: HTTP 409 JSON error without `Content-Disposition`, never a successful artifact.
* Screen enablement: the server adds `held_download_enabled: true` to the form-review view response only when the route is enabled (key absent otherwise, so existing contracts are unchanged by default). The panel renders the link only when that flag is true, the draft is not Unavailable and has an id.
* Browser proof needs the heavy canonical lock `/tmp/ama-rpi-heavy.lock` with actual-holder admission, no queue.

## Not in scope

* Core exporter, history, dependency changes; schema, SQL, auth, framework; approval, review or submit actions; POST routes; financial state, model or source parsing; Bicep or deployment; shared role, paging, atlas or inventory fixtures; the #153, #130, #131 test areas; parent #149 UX unmerged siblings.

## Planning Readiness

Ready. Research disposition: executed (focused baseline passes; source and guard research complete). No unresolved dependency.
