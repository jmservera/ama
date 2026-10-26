<!-- markdownlint-disable-file -->
---
title: Issue 350 rehearsal evidence alignment research
description: Current main, issue, PR and old-review evidence before aligning the local rehearsal record and lineage
ms.date: 2026-10-25
---

## Research Brief

Continuation of the same #350 workstream (draft PR #436, branch `test/deployed-feedback-harness-350`). Unpublished candidate bfb7f4b0 holds the 2026-10-24 local rehearsal evidence. This is new maintenance: documentation/evidence alignment and lineage integration only. Earlier dated artifacts, including the original non-conformant review, are historical and are not edited.

Research disposition: executed (focused, internal, read-only plus `git fetch`). Planning Readiness: Ready.

## Evidence

* Branch: worktree clean at bfb7f4b0; remote `origin/test/deployed-feedback-harness-350` is 6ac8e029 and is an ancestor of HEAD (no remote-only commits). PR #436 is OPEN and draft; its body names the old head, old base 140d8f49 and a receipt that is historical.
* Main is 36996d70: PR449 (7d4e89bb, Entra-authoritative staff access, `ApplicationAdmin`), PR450 (5d79aaee, ledger-safe SQL column migration), PR453 (grant CLI fix), plus docs and rubric changes. Merge of main into the branch was clean (merge commit d379fe3a); no conflict.
* Issue #350: OPEN, no acceptance box ticked; last comment 2026-10-24 states the rehearsal is local synthetic and does not replace Entra or real inference.
* Source change in PR449 `src/api/.../auth.py`: the trusted-proxy provider now decides login from validated tenant, object ID and app roles with no staff-row lookup; the staff-record and `ZF_AUTH_EMAIL_FALLBACK` path was removed. `PasswordProvider` is unchanged, so the loopback rehearsal still uses the staff-email plus shared-password path.
* Old record: the 2026-10-24 research said deployed ACs "need ... tenant/staff (#349)" and the changes artifact names a "#349 tenant and staff prerequisite" as smallest blocker. Under PR449 staff-row/database provisioning is no longer the login authority; that diagnosis is historical. The current deployed blocker is not re-diagnosed here (no Azure, Graph, network or role-assignment actions are authorized in this task); it is recorded as unverified pending the #349/#360 loops.
* Old review (2026-10-24): original outcome non-conformant (RV-001 source-change claim versus `git diff origin/main`, RV-002 SQL claims lacked transcript, RV-003 browser overclaim). Corrections were record-only and not independently re-verified. They are disclosed as corrected accuracy findings, not relabelled as conformant.
* `src/api/README.md` lines 2257 and 2282 still list `ZF_AUTH_EMAIL_FALLBACK`, which PR449 removed from code. This is pre-existing drift on main, outside this scope; recorded as a follow-up, not changed here.
* Running services (must stay untouched): tmux `ama-350-feedback` on 127.0.0.1:8350 (venv2 snapshot of bfb7f4b0 `src`, outside the worktree), `ama-444-resident` 8444 and 8445, container `ama-350-feedback-sql`. The 8350 server runs pre-PR449/450 code from the snapshot; merging main into the worktree does not alter it.
* Obsolete evidence: receipt `/tmp/rpi-350-local-final2` (bfb7f4b0) and the PR-body receipt for 6ac8e029 are not evidence for the merged head.

## Plan implications

* Rehearsal re-run on merged code is wanted so the claims are not stale, using a separate new disposable SQL container and port 8351, not the owner services.
* Only RPI artifacts and the PR body change; no source, auth or README change.
* Claims stay separate: local SQL/template rehearsal versus live Entra, real AI and the 60,000-home or 980-case baselines.
