<!-- markdownlint-disable-file -->
---
title: Issue 350 rehearsal alignment changes
description: Dated addendum aligning the local rehearsal record with current main; no source change
ms.date: 2026-10-25
---

## Scope

Documentation/evidence alignment and lineage integration only. No source, auth, README or issue-acceptance change. The 2026-10-24 artifacts (research, plan, details, critique, changes, review, state) are unchanged and remain the historical record. This is local synthetic SQL/template engineering evidence, not live Entra sign-in, real AI inference, 60,000-home stock or 980-case programme acceptance, and not #350 closure.

## Lineage

* Remote `origin/test/deployed-feedback-harness-350` (6ac8e029) is an ancestor of the local branch: no remote-only commits.
* `origin/main` 36996d70 merged with a merge commit (d379fe3a), no conflicts; published history and the earlier merge preserved. No reset, amend or rewrite.
* Main now includes PR449 (Entra-authoritative staff access), PR450 (ledger-safe SQL migration) and PR453 (grant CLI fix).

## Corrections to the 2026-10-24 record (disclosed, not relabelled)

* The old statement that the smallest deployed blocker is the "#349 tenant and staff prerequisite" (and that sign-in needs staff rows) is historical. Under PR449 the trusted-proxy provider decides access from validated tenant, object ID and app roles, with no staff-row lookup. The current deployed blocker is not re-diagnosed here (no Azure, Graph or network action is authorized); it is unverified until the #349 and #360 loops report.
* The original review outcome stays **non-conformant**. RV-001 (source-change claim versus `git diff origin/main`), RV-002 (SQL claims without transcript) and RV-003 (browser overclaim) were corrected in the record only; that closure was never independently re-verified. They remain corrected accuracy findings.
* Receipt `/tmp/rpi-350-local-final2` (bfb7f4b0) and the PR-body receipt for 6ac8e029 are obsolete for the merged head and are not used as evidence.

## Merged-main re-rehearsal (new evidence, 2026-10-25)

Merged-head sources were installed with pip from a `git archive` snapshot into a throw-away venv and run against a new helper container `ama-350-merged-sql` (loopback, own port), 127.0.0.1:8351, with the same constructed fixture (6 cases, 5 staff; `PasswordProvider`, unchanged by PR449). Transcripts: `/home/azureuser/rehearsal-350/merged/{exercise-run,persist,sql-evidence}.txt`.

| Check | Result |
| --- | --- |
| Merged code starts and serves on `ZF_STORE=mssql` with `ZF_SQL_AUTH=password` | Yes, against a fresh database (SQL tables were populated); the PR450 migration step itself is not separately evidenced |
| Anonymous, wrong password, unknown email, forged headers and cookie | 401 in each case |
| Roles liaison, manager, coordinator | 200; 6 cases |
| Contractors | `con@` ZF-1..ZF-5, ZF-6 404, POST 403; `other@` ZF-6 only, ZF-1 404 |
| One call logged on ZF-1, reload | Contact shown |
| App restart, same SQL | Contact persists; anonymous `/api/me` 401 |
| SQL | 6 cases, 5 staff, 8 audit rows (3 `log_contact`, `ai_run_*`, `ai_record`) |
| AI, no endpoint (`AI_ENDPOINT` unset in `run.sh`) | 200 `source: template`, `model: null`, audit `source=template`; no model is configured, outbound calls were not separately traced |

Not repeated: SQL-container restart durability and the browser pass (only the 2026-10-24 results exist, on the pre-PR449/450 snapshot); the observation that any signed-in staff role could log a call on a visible case (ZF-5) was reproduced and still not adjudicated.

## Owner services (untouched)

* `ama-350-feedback` (127.0.0.1:8350) and `ama-350-feedback-sql` were not restarted or changed; 8350 still runs the bfb7f4b0-era snapshot (pre-PR449/450), so it is not evidence about merged main. It still returns 401 anonymously.
* `ama-444-resident` ports 8444 and 8445 were not touched.
* The helper container, tmux session, venv and snapshot for 8351 were removed afterwards.

## Known unrelated drift

`src/api/README.md` lines 2257 and 2282 still mention `ZF_AUTH_EMAIL_FALLBACK`, removed from code by PR449. Pre-existing on main; routed as a follow-up, not changed here.
