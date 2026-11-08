---
title: AI and employee chat main stabilization 440 correction1 details
ms.date: 2026-11-08
---

## Phase details

### Phase 1: pack corrections (docs/architecture/cutover-evidence-pack.md, c96a section at lines 3092-3182)

* Row `Source observed` / `Excluded` (lines 3098, 3102): keep the 608c observation; scope "Excluded" to the pin: PR 1278 and PR 1243 were open at launch and were then absent from 608c main. Link the new currency subsection.
* #1275 bullet (line 3120): replace "still fails with 504 and has no supported override" by a dated history: the 504 on the AWF checksum retrieval was observed before recovery; the rootless checksums-and-bundle installer passed in run `42472167065` on #1275 head `4db31928` (2026-11-08T10:38Z, safe coordinator log); the coordinator reports later exact-head scorer retries and the #1278 scorer passed. #1274 permanent resilience is unimplemented, which is remediation not recovery.
* Review row (line 3132 and the assistants row at 3128): "independent role review" becomes: current role and scope, explicit human source verification, accept only by the same verifier, extra independence from evidence submitters, recorders and fixers for `quality-evidence`; no general requester separation (`assistants.py` 1106-1173).
* Classification line (3181): "Deferred: F1 clean-up" becomes "Proposed (pending triage, unowned, unfiled): F1 refactor"; "Blocked: ... AWF checksum retrieval (#1274)" becomes "Open (not implemented): permanent AWF resilience (#1274); the installer outage itself was recovered".
* Findings bullet F1 (3168) and recommendation (3182): F1 stays an observation pending triage; "F1 may be picked up under #162" becomes a suggestion for triage, not a lane assignment.
* Add subsection "Correction 1 and currency (2026-11-08T12:00Z)" with: what changed and why (assessment `review-440-c96a`), current identities table, source-identity proof, amended reading statement, residual gates. It supersedes only the named earlier statements.

### Phase 2: reading amendment

State plainly in the new subsection that the original research claim of reading the addendum and component guides before planning is unsupported, link the new research record, and list honest ranges.

### Phase 3: index and log

* README paragraph: append one sentence pointing to the new subsection and stating AWF recovery vs remediation and that exclusions are scoped to the 608c pin.
* Log: new entry `## [2026-11-08] update | Issue 440 AI and employee chat checkpoint correction 1 and currency (Refs #440, #157, #159, #104, #107)`; earlier entries unchanged.

### Phase 4: validation commands (existing checks only)

* `git diff --check`; ASCII check of added lines (`grep -nP '[^\x00-\x7F]'`); em dash check; heading slug check for the pack anchor and new subsection anchor; relative link existence for added links; `git diff --name-only HEAD` scope guard.
* Source identity: `sha256sum` of installed venv modules against `git show origin/main:<path>` (already recorded in research) and `git diff --name-only 608c98e6 origin/main` over the audited modules and selected tests (zero). Re-run once at the end after a final `git fetch`.
* No Docker, SQL, browser, package suite or full gate. `tools/rpi-checks.py --changed` is not run: owner CI-first tier and the user instruction exclude broad execution; hosted CI remains required.

### Phase 5: close-out

Changes record, one author Review (outcome and adverse items preserved), state completed in Follow-up, repo-local privacy-safe noreply identity from `gh api user`, Conventional Commit `docs(arch): correct 440 AI checkpoint evidence qualifications` with the Copilot trailer. Final `git fetch origin main` to record movement without rebase.
