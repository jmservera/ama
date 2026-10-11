<!-- markdownlint-disable-file -->

# Challenge Session: zava-north-homes-renaming

## Session Details

| Field | Value |
| --- | --- |
| Date | 2026-10-11 |
| Status | Complete |
| Record path | .copilot-tracking/challenges/2026-10-11/zava-north-homes-renaming-challenge.md |
| Scope source | Caller-supplied subject and confirmed scope |
| Focus | Company/project renaming and migration-script boundaries across formats |

## Confirmed Scope

* Subject: Rename Proper North Homes to Zava North Homes, choose a replacement
  for Proper Warm, and examine migration-script requirements and edge cases.
* Boundary: Documentation, application branding/identifiers, slide sources,
  published PPTX files, links and deployed-resource references. This challenge
  does not choose a project name, design the script or change product artifacts.
* Confirmation: User confirmed the proposed scope with the correction
  'make it "Zava North Homes"'.
* Evidence basis: Caller request and confirmed scope; existing repository
  guidance preserves the original case study and historical evidence.
* Working copy: Owner authorised a separate topic worktree, leaving the
  untracked .env in the original worktree untouched.

## Related Artifacts

| Artifact | Relationship to the challenge | Evidence used |
| --- | --- | --- |
| docs/case_study_48_original.md | Historical problem specification | Repository guidance preserves this file unchanged |
| docs/case_study_48_addendum.md | Evolving application/customer design | Current company and programme framing |
| docs/reference/README.md | Knowledge-base index | Documentation and presentation storage conventions |
| docs/presentations/ | Published presentation assets | Binary output requires separate treatment from source text |
| mvp/ | Application surfaces | Branding versus technical identifier boundary remains unresolved |

## Challenge Coverage

| Angle or topic | Material uncertainty examined | Status | Notes |
| --- | --- | --- | --- |
| Scope | Target company name and included surfaces | explored | Zava North Homes confirmed; project name remains undecided |
| Migration outcome | What the rename must accomplish | explored | No visible old-name references, working references and updated presentations; Git history excluded |
| Technical identity | Meaning of a clean end result for live identifiers | explored | Rename all technical names and redeploy; owner allows wiping deployments in principle |
| Redeployment preservation | What must survive replacement of deployments | explored | Nothing for this AMA test reset; synthetic data can be recreated; not a production design rule |
| Project naming | What the replacement name should communicate | explored | Improvement and momentum through agents/generative AI, with safety, responsibility and transparency |
| Historical evidence | Treatment of current-tree logs and prior evidence | explored | Historical references with old names are permitted to preserve references and links |
| Reset boundary | Which resources the script may replace | explored | User scope is anything with the old name; temporary script. Exact resource inventory not yet established |
| Completion evidence | How to establish the requested end result | explored | Updated PPTX, cleared Azure resource group, successful redeployment and working newly branded app |
| Branding asset | Logo source for the renamed application | explored | User supplied logo URL; content, availability and usage rights not assessed |
| Functional acceptance | Meaning of working again after redeployment | explored | Entra login, synthetic case content, 443 open cases, overview map and logo in PPT/website |
| Partial migration | Treatment of unmodifiable or missed surfaces | explored | Partial migration is acceptable with notes documenting failures |

## Q&A Log

### Scope confirmation

Question:

Confirm the company/project rename challenge across docs, application surfaces,
presentation sources/binaries, links and deployed-resource references, with no
product changes during the challenge.

Answer:

Confirm proposed scope, make it "Zava North Homes"

Record note:

The correction supersedes the initial requested name Zava Homes.

### Migration outcome

Question:

What must be different for users and readers after this rename for you to
consider it successful?

Answer:

Nobody will notice that the name was changed, no mention to Proper Homes is
there, all references work, presentations are updated. Git history is ok, we
don't need to change this, just the end result.

Record note:

The user excludes Git history from the migration. "Proper Homes" is preserved
as supplied wording; the old company name in the confirmed scope is Proper
North Homes. Current-tree historical records remain an explicit boundary to
clarify, not an inferred exception.

### Historical records in the current tree

Question:

How should the rename treat historical artifacts still present in the current
repository, including the original case study and recorded deployment evidence,
when they contain the old names?

Answer:

the original case study does not have the name on it, it was decided later,
it may be in the addendum

Record note:

The original case study previously read in this session contains neither
Proper North Homes nor Proper Warm. The addendum does contain both names.
This answers the original-case boundary, not the disposition of other
historical snapshots, logs or deployment evidence. No source artifact changed.

### Technical identity and deployed resources

Question:

What should happen to technical names that still contain the old branding,
such as application URLs, Azure resource names, database names and code
identifiers?

Answer:

Change them all and redeploy after changing, we can wipe out all the
deployments and run them again with the new names

Record note:

The intended scope includes technical identities and redeployment, not only
visible branding. This is design direction in a read-only challenge, not
execution of deletion or an identified-resource deletion approval. Preservation
requirements and the exact resource boundary are still unspecified.

### What survives redeployment

Question:

What must survive wiping and recreating the deployments?

Answer:

Nothing, we are working on synthetic data that can be recreated, no worries
by now, this is not a design rule, it's just the fact that for the AMA we will
do this many times while trying new things. Once in production we are not
supposed to do this, but it's ok by now as we are still testing new things.

Record note:

No deployment state must survive this test reset. Preserve the scope of this
answer: repeated disposable AMA testing, not a production architecture rule
or permission to delete resources outside the identified exercise deployments.

### Project naming purpose

Question:

What should the new project name communicate about the programme?

Answer:

the new name must communicate improvement and momentum gain pivoted by
agents and generative AI, but safe, responsible and transparent.

Record note:

Naming intent is recorded; selection of an actual replacement name remains
open. These are desired associations, not evidence of achieved improvement
or delivered safety.

### Remaining current-tree historical references

Question:

How should the migration handle old names in append-only knowledge-base logs
and saved evidence of earlier deployments that remain in the current tree?

Answer:

references to historical records with old names are permitted to avoid
breaking references and links.

Record note:

This qualifies the earlier clean-end-result expectation: old names are
permitted in references to historical records when needed to preserve links.
Do not interpret this as permission to silently rewrite evidence or break
historical URLs.

### Resource ownership and reset boundary

Question:

What defines the boundary of resources and identities that the migration
script may replace?

Answer:

anything with the old name, the script will be temporary

Record note:

The user gives a name-based boundary and a temporary-script lifetime.
An exact resource inventory and dependencies are still absent. This challenge
does not execute deletion; shared/external references still require explicit
identification before any later destructive action.

### Completion evidence

Question:

What evidence would convince you that the rename is complete across the
application, documents, presentations and working links?

Answer:

When even the pptx have been updated, everything on the Azure resource group
was deleted and a new deployment went through and the app is working again
with the new name and new logo
https://zava-corp-online.azurewebsites.net/images/logo.png

Record note:

Completion now includes PPTX binaries, an Azure resource-group reset and
recreation, and a renamed/rebranded working app. The user-supplied logo has
not been fetched or assessed. The resource-group reset is explicit intended
scope, but an identified inventory and action-specific safeguards remain
required before later execution.

### Functional acceptance after redeployment

Question:

Which application behaviours must be demonstrated after redeployment for
"the app is working again" to be satisfied?

Answer:

App still uses entra id login, my cases and all cases sections show content
from the synthetic data generated 443 open cases, overview shows the cases
on a map, the new logo is visible on the ppt and the website.

Record note:

Explicit acceptance behaviours: Entra ID login; My cases and All cases show
generated synthetic content with 443 open cases; Overview displays case
locations on a map; the supplied new logo is visible in presentations and
the website. The exact user-specific My cases count is not supplied.

### Partial migration and script failure

Question:

What should happen if the script cannot update an artifact or completes only
part of the resource reset and redeployment?

Answer:

partial migration with notes about the failures

Record note:

Partial migration is an acceptable reported outcome, provided failures are
documented. It is not full completion and must not be reported as satisfying
all acceptance behaviours if some remain unverified.

## Unresolved Items

| Item | Why unresolved | Smallest missing evidence or decision | Suggested next owner |
| --- | --- | --- | --- |
| Project name | Replacement requested but not selected | Naming purpose and eventual choice | user |
| Exact reset boundary | Name-based scope has no concrete inventory yet | Inventory of matching resources, identities and dependencies | rpi-research |
| Artifact inventory | No exhaustive inspection performed in this challenge | Inventory of current branding occurrences, formats, paths, embedded content, links and presentation working sources | rpi-research |
| Logo asset | User supplied a URL; no asset inspection | Retrieve and check format, availability and required presentation/web variants | rpi-research |

## Session Outcome

* Coverage summary: Company name is Zava North Homes. Replacement project
  naming must convey improvement and momentum through agents/generative AI,
  with safety, responsibility and transparency. Current application branding,
  technical names, documents and presentations are in scope. Git history
  remains unchanged; historical references may retain old names to preserve
  links. The original case study contains no company/programme name.
* Redeployment: Clear and recreate the exercise Azure resource-group contents;
  no deployment state needs to survive this disposable synthetic-data test.
  This is not a production design rule. No deletion or resource modification
  was performed during the challenge.
* Acceptance: Entra ID login; My cases and All cases populated from the
  generated synthetic data, with 443 open cases; case map in Overview; new
  name and supplied logo in the app, and updated presentation binaries with
  the logo. Partial migration is acceptable with explicit failure notes,
  but remains distinct from full completion.
* Unresolved items: Replacement project name, concrete resource/dependency
  inventory, cross-format artifact inventory and inspected logo asset.
* Advisory next options: `/rpi-research` to inventory rename surfaces,
  presentation sources/binaries, infrastructure/identity dependencies and
  logo asset, and develop naming candidates against the stated intent.
  Do not design or execute the migration script during this challenge.
* Session status: Complete through coverage saturation. This record is a
  requirements/disposition record, not validation or production approval.

## Post-Challenge Naming Decision

On 2026-10-11 the owner selected "Zava Forward" from the proposed project names
and requested continuation of the rename. This resolves the project-name
choice above. The temporary local migration tooling is documented in
[tools/rename-zava.md](../../../../tools/rename-zava.md); deployment and
presentation acceptance remain separate from script generation.
