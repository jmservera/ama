---
title: One-Off Zava North Homes and Zava Forward Migration
description: Dry-run-first local branding migration, presentation handling and explicit Azure redeployment follow-up
ms.date: 2026-10-11
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
* The MVP website gets the same locally served PNG with accessible alternate
  text and a contrasting background. No remote logo dependency or CSP change.
* Files are replaced atomically and executable permissions are retained.

## Deliberate exceptions and edge cases

* Original case study, regulatory snapshots, append-only log, owner memory
  and historical tracking records stay unchanged. Slide authoring sources and
  PPTX binaries under tracking are active migration inputs.
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
shared tenant/M365 registrations. The current deployment identity and M365 CLI
session both return `Insufficient privileges` when reading the existing API
app registration. Resource-group access does not grant Microsoft Graph
application-management access. Rebuild remains blocked until an authorised
application owner or tenant administrator can provision the registration,
roles, secret and new Container Apps callback URI. Do not disable authentication
or substitute a shared password to work around this dependency.

Use the renamed Bicep and existing provisioning tools rather than a second
deployment implementation. Explicitly pass `workload=forward`, `uksouth`,
the development profile, SQL Entra administrator, real application image,
Entra client ID and map tile URL/attribution. Build the renamed package image,
create the new application roles/redirect URI/secret, create SQL contained
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
