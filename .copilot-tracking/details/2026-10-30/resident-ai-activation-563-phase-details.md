---
title: Resident AI activation 563 phase details
ms.date: 2026-10-30
---

Task 563 / resident-ai-activation-563. Safe-stop branch of owner request,
not authorization to waive private SQL prerequisites. Research C1-C8 applies.

<!-- phase: P01 -->
## P01: Preserve and assess

<!-- task: P01-T01 -->
### P01-T01: Exact private backup

Use the session files area, mode0700 directory and mode0600 raw files.
Capture az containerapp show, revision list, auth-config and job list without
printing raw responses. Hash exact bytes; retain original JSON and protected
configuration for later comparison. az show preserves returned secret metadata
and references, not retrievable values; no secret is changed or needed here.
Existing original revision: ca-resident-demo--res-live-20261030-152028.

Completion: backups exist outside git; record paths, timestamps and hashes.
Failure blocks further operation. No cloud writes permitted.

Execution complete: exact original responses/hashes retained in external
resident-activation-backup, no secret values requested. See changes record.

<!-- task: P01-T02 -->
### P01-T02: Warm and anonymous denial

Use existing app FQDN from backup. Health GET timeout up to180 seconds,
up to three attempts with delay for cold scale-from-zero.
POST /demo/assistant anonymously with a nonsensitive synthetic question and
record-use false, Origin matching site; expect401/403. No resident credentials,
cookies, screenshots or model calls. Record status only, not raw app data.
Health alone cannot establish accounting/model readiness.

Execution complete: final health200/anonymous assistant403, 180s timeouts.

<!-- phase: P02 -->
## P02: Reconcile and hand off

<!-- task: P02-T01 -->
### P02-T01: Preserve and report

Repeat exact reads and compare JSON structures app/auth/jobs. Revision list may
have runtime timestamps; no revision should be added. Verify min0/max1,
two optional variables absent and all eight jobs Manual. Record no cloud write,
no key/role creation, zero sign-in attempts, no paid inference, no rollback needed.
Live consented grounded answer, out-of-scope model-mode fallback and authenticated
unset checks remain Not run. Missing SQL proof remains Unknown, not Missing.

Execution complete: full app/auth/jobs equality; revision configuration equal.
Expected warm runtime replicas0->1 and ScaledToZero->RunningAtMaxScale excluded
only after preserving the original strict assertion failure. No new revision,
min0/max1 unchanged and all jobs Manual. No rollback required without mutation.

<!-- task: P02-T02 -->
### P02-T02: Review and local persistence

Reconcile plan/details/changes/state; execute rpi-review once with independent
assessment. Disposition every finding explicitly: defer activation prerequisites,
and block candidate acceptance for material safe-stop defects. Preserve the
original outcome; no passing/conformant claim while material findings remain.
The RPI wrapper requires any corrections in later user-selected work, not a
return to Implement or a repeated Review in this task. Local persistence of
adverse evidence does not approve the candidate. Configure
repo-local privacy-safe author/committer from gh api user, commit with
Refs #563 and Copilot trailer. Never push or create a PR in this task.
Fetch main read-only, run complete local gate to a fresh external directory
after commit, and report actual outcome; preserve original receipt externally.
Do not claim publication approval, human acceptance or completed issue.
