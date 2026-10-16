---
title: One-Off Zava North Homes and Zava Forward Migration
description: Dry-run-first local branding migration, presentation handling and explicit Azure redeployment follow-up
ms.date: 2026-10-16
ms.topic: how-to
---

## Scope

Company: Zava North Homes. Programme: Zava Forward. This temporary script
implements the name selected by the owner on 2026-10-11. It generates a JSON
inventory and can apply local changes; it never deletes resources, changes
Entra registrations, deploys Azure, commits, pushes or rewrites Git history.

Use a clean, dedicated topic worktree. The original checkout currently has
untracked local MCP settings and a private `.env`; the script will refuse to
apply there. Untracked files and secrets are not migration inputs.

## Run

Install the two dependencies with pip in your chosen virtual environment:

```bash
python3 -m pip install -r tools/rename-zava-requirements.txt
```

Download the owner-supplied public logo locally, outside the repository.
The script never fetches URLs or accepts credentials:

```bash
curl --fail --proto '=https' --proto-redir '=https' \
  https://zava-corp-online.azurewebsites.net/images/logo.png \
  -o /tmp/zava-logo.png
python3 tools/rename-zava.py --root . --logo /tmp/zava-logo.png \
  --report /tmp/zava-rename-plan.json
```

Review the planned changes and preservation list. Apply explicitly:

```bash
python3 tools/rename-zava.py --root . --logo /tmp/zava-logo.png \
  --report /tmp/zava-rename-result.json --apply
python3 tools/rename-zava-tests.py
git diff --check
```

The report must be outside the worktree, because it records old names.
Exit 0 means the local stage completed or was planned; it does not mean the
whole migration is complete. Exit 1 means per-file failures are recorded
(partial migration); exit 2 means preflight/configuration stopped the run.
Do not rerun on the resulting dirty tree: inspect the report, address failed
files, and stage/commit the intended results before a new dry run.

## Automatic coverage

* Known display-name variants, slugs and module names: `Proper North Homes`,
  `Proper Warm`, `ProperWarm`, `properwarm`, hyphen/underscore variants.
* Runtime contracts move together: `PW_` environment names, `pw_` symbols and
  cookie, `X-PW-` CSRF header, Python imports, Docker paths, tests and CI.
* Tracked active filenames and directories move with their content references.
  Preflight rejects collisions, existing destinations and symlinks.
* Infrastructure workload defaults change from `warm` to `forward`; resource
  prefix examples and Entra app-role names change with source code. These are
  source changes only, not migration of live identities.
* PPTX text across runs, groups, tables, notes, masters, layouts and metadata
  changes without replacing whole paragraphs. A PNG logo with white backing is
  added to every slide, and matching elements/assets are added to slide YAML.
  Python deck authoring scripts are active inputs too; research, review and
  validation records beside them remain historical.
* The MVP website gets the same locally served PNG with accessible alternate
  text and a contrasting background. No remote logo dependency or CSP change.
  Live targets are `src/api/src/zava_forward/api/web/` and the hash-checked
  ranking policy under `src/core/src/zava_forward/core/policies/`; applying
  branding never recreates `mvp/web/`. Historical old-name assertions and
  pinned/datetime records remain exact, not a request to rename Python packages.
* Files are replaced atomically and existing permissions are retained. Newly
  created public assets use mode 0644; the MVP image also makes packaged web
  assets readable by its non-root runtime.

## Deliberate exceptions and edge cases

* Original case study, regulatory snapshots, append-only log, owner memory
  historical rubric score snapshots and historical tracking records stay
  unchanged. Slide authoring sources and PPTX binaries under tracking are
  active migration inputs.
* External URLs remain exact, including pinned GitHub evidence and previous
  deployment URLs. Historical references are allowed by owner direction.
  Relative references to preserved tracked artifacts retain their old paths.
  When an immutable historical record links to a renamed active Markdown
  document, the old path retains an exact original snapshot; a history
  manifest records these exceptions so subsequent scans preserve them.
* This is not a blind replacement of the word `warm`: official Warm Homes
  funding names, warmth descriptions and third-party terminology stay intact.
* PDF exports, raster screenshots, slide previews, narrated audio, old logos
  burned into images and diagram renderings require inspection/re-export.
  The report enumerates binary assets rather than pretending to modify them.
* Charts, SmartArt, embedded spreadsheets/objects, media, hyperlinks and
  XML-only identifiers may need additional treatment. Render every changed
  deck and inspect notes, links, clipping, contrast and logo overlap. Binary
  mutation is not visual validation; do not publish an unvalidated deck.
* Check renamed Markdown heading fragments and local links, generated workflow
  lock files, private dataset/generator paths and mounted filenames. The
  script does not rewrite local untracked datasets, user-global configuration,
  copied external snapshots or files on other branches.
* Existing tokens, resource IDs, role assignments, redirects, secrets, SQL
  grants, SharePoint permissions and webhooks cannot be fixed by string
  replacement. Capture dependencies and recreate the exercise integration.
  Observed Markdown deployment IDs (`warm-test`, `warm-dev`, `warm-dev2`)
  and the historical `ca-properwarm-mvp` app/revision remain exact evidence.
  Wrapped display names are matched across whitespace; technical IDs and
  external URLs are not a reason to rewrite historical deployment facts.
* The document-workbench logo rule belongs in its served stylesheet, not an
  inline style element blocked by the existing `style-src 'self'` policy.
  Its server must allow the PNG route and preserve binary bytes with
  `image/png`; the logo's flex item must not shrink below its 114x40 CSS-pixel
  box. Migration/HTTP/browser checks retain CSP instead of relaxing it.
* Ranking-policy display metadata is covered by its content hash. The script
  recomputes that hash after the rename without changing rule order or logic.
* A partial report lists the failed files. Other files may already be changed;
  the operation is atomic per file, not a transaction across the repository.

## Azure reset and acceptance

The owner permits discarding this AMA exercise deployment and regenerating
synthetic data. This is not a production design rule. Before any deletion,
identify the subscription and exact `ama` resource-group contents, locks,
soft-deleted resource constraints and external identity/M365 dependencies;
confirm that the inventory is the intended destructive scope. The local script
intentionally has no destructive Azure flag.

The owner authorised deletion of resources inside `ama` and accepted downtime
on 2026-10-11. That does not authorise deleting the resource group itself or
shared tenant/M365 registrations. The deployment identity and M365 CLI
session initially returned `Insufficient privileges` when reading the existing API
app registration. Resource-group access does not grant Microsoft Graph
application-management access. Infrastructure and the protected API can be
rebuilt using a securely retained existing client credential. Interactive
sign-in and the tenant naming/role transition need authorised tenant action and
real-user acceptance. The owner repaired the callback on 2026-10-12, then
completed an isolated authorised provisioning login. The repeatable initializer
subsequently verified it in check-only mode without broadening the deployment
identity's permissions.
Do not disable authentication or substitute a shared password.

Use the renamed Bicep and existing provisioning tools rather than a second
deployment implementation. Explicitly pass `workload=forward`, `uksouth`,
the development profile, SQL Entra administrator, real application image,
Entra client ID and map tile URL/attribution. Build the renamed package image,
retain and initialize the existing registration or explicitly provision a new
one when required, create SQL contained
users for the new workload identities, and seed the retained generated-data
snapshot. Check Key Vault soft deletion, name uniqueness, SQL/model regional
availability and identity permissions before assuming recreation succeeds.
Placeholder images and an empty database do not satisfy acceptance.

Complete migration requires:

* Entra ID login, with no second shared-password prompt.
* My cases and All cases populated with generated synthetic records and
  443 open cases overall; My cases remains scoped to the signed-in identity.
* Overview case locations and map tiles visible.
* Zava Forward/Zava North Homes and the supplied logo visible on the website
  and updated presentation binaries.
* Working active links; historical old-name references are permitted.

Report unmet behaviours, deployment errors and presentation rendering gaps as
partial, not as completed migration.

## Recorded local migration

On 2026-10-11 the topic branch was migrated, leaving the original checkout's
untracked data, `.env` and MCP settings untouched. The initial application pass
reported 178 changes and zero per-file failures. Subsequent generated deck/logo
adjustments keep logos above the existing title band and make the wider website
brand wrap safely with authenticated navigation.

* Migration regressions: 20 pass.
* MVP: 270 tests run, 26 existing skips; prototype: 15 tests pass.
* Bicep build and browser JavaScript syntax checks pass.
* All 40 slide sources pass the shared pipeline dry-run. Four PPTX files render
  successfully; logo/text bounding boxes do not intersect. The published
  mentor deck and its validated working copy have identical hashes.
* Markdown targets have no new failures against the baseline. Ten existing
  placeholder/relative-link defects remain. Historical snapshots are explicitly
  listed in `.copilot-tracking/renames/zava-forward-history.json`.
* Local browser smoke check uses a rebranded copy of the retained 980-case
  synthetic fixture: All cases has 443 open cases, the test manager has 133 My
  cases, Overview has 443 points with loaded tiles, and the supplied logo loads.
  Header elements remain contained at 1280, 800 and 375 CSS pixels.

These are rename/local checks, not live acceptance or evidence of new AI model
inference. Entra application provisioning, Azure recreation and Azure SQL
restoration remain uncompleted. Historic raster previews and embedded/SmartArt
limitations remain the explicit exceptions above; rendering did not redesign
the decks' pre-existing dense layouts.

Publication also integrated the owner's concurrent merge of the new executive
capstone deck from #61, without rebasing or force-pushing. Its 21 slides and
Python authoring sources were migrated and checked too: the final coverage is
61 slide sources and five PPTX files. The rubric conflict retained the remote
workflow's recorded score unchanged. Historical score snapshots are now explicit
exceptions, not branding inputs. A 21st regression ensures identical working
and published deck inputs reuse the same output bytes.

## Recorded Azure rebuild on 2026-10-12

Deleted all active resources inside `ama`, including the four recreatable
workload identities and the separately indexed `budget-warm-test`. Verified
empty generic ARM and budget indexes before deploying. Kept the group, its
external operator and shared tenant/M365 resources. Service-retained
soft-deleted artifacts are not active resources and were not claimed purged.

Both renamed deployments succeeded; rebuilt the versioned real image and
restored the continuing fixture to Azure SQL. The new API is:

`https://ca-forward-test-api.salmonplant-3b962c5f.uksouth.azurecontainerapps.io`

Health is 200, unauthenticated API requests receive 401 and a browser is
redirected to Entra. Checks inside the API workload confirmed 980 cases / 443
open, managed-identity SQL reads/writes and actual `source=ai` results from both
`standard` and `capable`. Audit writes survived a real revision restart. The
deployed HTML contains the new company/programme names. These operator checks
do not substitute for signed-in browser acceptance.

The owner reports adding the callback for client
`8a0a196a-d5e8-4aa6-8a9d-cdd28af5c235`:

`https://ca-forward-test-api.salmonplant-3b962c5f.uksouth.azurecontainerapps.io/.auth/login/aad/callback`

Preserve existing redirects and assignments. The registration still issues
`ProperWarm.*` roles; an explicit deployment-only map preserves their workbench
meaning until the owner migrates them to `ZavaForward.*`. Complete the tenant
name/role transition before claiming all active identity names are migrated.
The first-time provisioning script can create a new `zava-forward-api` registration, but
that requires user assignments, a new vault credential and redeployment with
the returned client ID; it is not an in-place update by client ID.

The [from-empty infrastructure recipe](../infra/README.md#from-empty-rebuild-observed-on-2026-10-12)
records deletion ordering, separate budget enumeration, staged deployment,
identity/model configuration, seeding and live checks. At that rebuild
checkpoint, live Entra login, scoped lists, map rendering and tiles were not
yet verified. Later owner-reported sign-in and staff initialization are recorded
in the [current handover](../infra/README.md#current-exercise-handover-2026-10-13);
complete browser/map acceptance and retained tenant naming remain separate.
Use the
[callback-only initializer](../infra/README.md#post-deployment-api-authentication-initialization)
after future rebuilds rather than replacing the retained registration:

```bash
python3 infra/scripts/initialize-api-auth.py \
  -g ama -n ca-forward-test-api --login
```

Subsequent runs omit `--login`; `--check` verifies without a Graph patch.
Placeholder workers remain placeholders, not delivered agent services.

## Missing-logo repair on 2026-10-12

The owner reported the live logo missing. The API traceback showed permission
denied reading the packaged PNG: a newly generated asset had inherited mode
0600 and root ownership in the image, while the server runs as UID 10001.
The migration now makes new public assets 0644 and image packaging normalizes
web readability. Existing target permissions and the non-root runtime remain
intact; no remote logo or authentication exception was added.

Rebuilt and deployed `zava-forward-mvp:logo-20261012-permissions`. The running
server now returns the exact source PNG, 14325 bytes at 644 x 225, with status
200 and `image/png`; its packaged mode is 0644. The image build was deliberately
performed with the source still at 0600. CI repeats that input and checks the
PNG from the read-only, capability-free container. The MVP suite runs 273 tests
with 26 existing skips; 22 migration regressions pass. Public health and
authentication responses are preserved. This asset check is not a substitute
for signed-in list/map or tenant name/role acceptance.

## Subsequent identity and account learning (2026-10-13)

Public welcome, protected entry and own-account photo transport were deployed
after the logo repair. A narrow `img-src blob:` CSP correction enables the
browser's binary-photo success path; it does not prove a person's photo or
consent. Tenant onboarding then demonstrated that a valid app role still needs
the explicit SQL staff binding and startup-cache restart. Private reconciliation
preserved stable work codes, supplier scopes and historical actors.

The deployed account-switch image requests `select_account` directly; ordinary
Sign out remains platform logout. Constant flow events use the existing
centralized logs, not general callback/query logging. Actual replacement in an
already-authenticated browser remains owner acceptance. See
[ADR identity learning](../docs/adrs/0002-pilot-readiness-architecture.md#observed-exercise-identity-and-session-learning-2026-10-13),
[product learning](../docs/prds/zava-forward-retrofit-programme-demonstrator.md#review-learning-disposition)
and [dated observations](../docs/case_study_48_addendum.md#observed-deployment-and-identity-learning-2026-10-1213).
Historical test counts/images above are pinned observations, not current totals.
