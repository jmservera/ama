# Research: local implementation slice for issue 462 after PR 455 merged

Written 2026-10-25T21:3xZ, before the revised plan, details, critique and any implementation. Research disposition: executed (read of merged main code, local tooling and the existing issue text). The original research, preflight extension, errata and the disclosed ungated planning push `5963fa3f` are preserved unchanged and are not relabelled.

## Lifecycle and integration

* Dependency delivered: PR 455 merged as `c8d16059c0c0a22c4ffba88c6b65ac068f64accc` (coordinator statement, confirmed as an ancestor of `origin/main`). Issue 444 stays open for low UI follow-ups.
* Branch `feat/resident-azure-showcase-462` was clean. Main was merged without rewriting history (merge commit `abd16893`, parent `b605933d`). No push, PR, cloud call or secret access occurred.
* Authority in this continuation: local implementation, local tests, a local SQL Server container owned by this task, one local commit. Not authorised: push, PR, heavy full gate, any Azure/Graph/M365/live SQL call, secret read/list/generation, job start, deployment. Live budget headroom stays UNKNOWN and the deleted raw cost JSON is not relied on as proof.

## What merged main provides (read from the worktree)

* `core/resident_preview.py`: `Grant`, strict `_parse`, `resolve_grant`, `resident_view`, `safe_start` with loopback and forbidden-environment guard, `BANNER`, `HELP`, `UNAVAILABLE`, `STAGE_TEXT`. `resident_view` needs a full `Store` (`store.cases`, `store.data`, `appointment_status`), which is a JSON file store with staff data. It is not suitable for a SQL-only showcase and must not be edited.
* `api/resident_preview/app.py`: loopback-only server that chooses one subject at start-up. Its Host check and `safe_start` are the 444 guard and are not touched.
* Reusable without change: public constants `BANNER`, `HELP`, `UNAVAILABLE`, `STAGE_TEXT`, `STAGE_ORDER` (read-only import) and the web asset conventions (Fluent 2 tokens, skip link, live regions, focus ring, reduced motion).
* Staff store: `MssqlStore` creates schema and audits on open, so it is not used. `mssqlstore.TABLES["cases"]` gives the real `cases` DDL for a local SQL Server fixture; `connection_string` gives the ODBC pattern with `ZF_SQL_AUTH=msi|password`.

## Existing issue acceptance criteria (issue 462 body, read with `gh`)

The issue asks for an isolated synthetic resident showcase in resource group `ama`, linked to the current homes database, username a fake email, one shared complex demo password, no production claim. The owner added constraints in the briefs (synthetic-only positive-allowlist SQL view and dedicated read-only principal, at most 25 allowlisted mappings, vault `kv-cutovertest-rzsrg`, expiry 2026-10-26T12:00Z, cloud gated). No extra product scope is added.

## Which gaps block local implementation and which do not

| Gap | Needs live preflight | Can be parameterised and tested locally now |
| --- | --- | --- |
| G1 budget headroom | Yes, before any cloud spend | Not relevant to local code; deployment config refuses to start without finite expiry |
| G2 live email equality | Yes (counts-only private probe) | Mapping builder, view and fail-closed rules are tested on constructed synthetic rows; the allowlist table starts empty so production fails closed |
| G3 principal and view creation | Yes (private job, budget gated) | View and principal T-SQL are generated and tested against a local SQL Server |
| G4 owner retrieval route | Yes (role and private client approval) | Not testable; app only reads a verifier by named config reference |

None of the four blocks writing and testing the pure local code. All four still block cloud steps.

## Verified local tooling

* Docker works. A SQL Server 2022 image is present locally. An existing container named `ama-350-feedback-sql` belongs to another worktree and is not touched; this task starts its own loopback-bound container and removes only that.
* `mssql-python` 1.15.0 is installed globally. `zava_forward` was not importable, so an external virtual environment `/home/azureuser/.venvs/ama462` was created (outside the repository) and the distributions were installed editable with pip (the missing-dependency failure justified it; no uv, no `PYTHONPATH=mvp`).
* Playwright 1.64.0 and chromium 1248 are available for the browser check.
* Web guidelines: `.github/skills/web-design-guidelines/SKILL.md` and `.agents/skills/redesign-existing-projects/SKILL.md` were read; the current guideline source `https://raw.githubusercontent.com/vercel-labs/web-interface-guidelines/main/command.md` was fetched in full at this step. Fluent 2, plain-language and WCAG baselines take precedence over generic aesthetics; no conformance is claimed.

## Provenance rule (no invented customer facts)

The live `cases` rows carry no per-case synthetic flag (earlier finding, seed-level flag only). The view therefore does not infer synthetic status from the row. A row is admitted only when it is in the database-owned allowlist table `resident_showcase.allowed_case`, populated only by an owner-approved step with a provenance reference, AND its normalised email is on a reserved synthetic domain (`example.com`), AND that normalised email is unique across all `cases`. The allowlist table ships empty, so nothing is shown until the owner approves rows.

## Open items carried forward

Live equality of `retrofit` to the seed, remaining-headroom proof, secret retrieval route and role, private job for view and principal creation, the ungated `5963fa3f` push disposition, and the complete full gate (not run here).
