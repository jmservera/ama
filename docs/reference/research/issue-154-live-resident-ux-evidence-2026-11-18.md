---
title: Resident and Representative UX on the Live Demo (Issue 154)
description: Per-criterion record for #154 on the synthetic demo; no live resident contact is observed on the resident showcase, while usability-programme validation and the representative view cannot be proven for the demo
author: AMA programme
ms.date: 2026-11-18
ms.topic: reference
---

## Scope and authority

Owner decisions of 2026-11-18: this is the synthetic demo, desktop only. Live Azure is authorised (resource group `ama`, cap USD 700, no drills, no Key Vault rotation, no production change). Azure billing reconciliation, DPO and Legal approval and person-run assistive-technology testing are not needed for the demo. No Azure resource was created or changed, so nothing needed deleting, and no source code changed.

The resident sign-in and the employee test sign-in were read from the owner's files at run time inside the scripts and never printed or written to an artifact. Screenshots mask email addresses. Readings are observations on one date, not an accessibility acceptance or a usability result.

## Evidence gathered

Scripts and outputs are under `.copilot-tracking/evidence/2026-11-18/issue-154-live/`: `live_proof.py`, `rep_probe.py`, `live-proof.json`, `rep-probe.json` and three 1366 by 900 desktop screenshots.

### Resident showcase (`ca-resident-demo`)

* The signed-out page and the signed-in page both carry the banner "Synthetic showcase - not a live resident service ... Do not use this for real resident data or decisions" and the note that Legal and DPO review is outstanding ([01-resident-signed-out.png](../../../.copilot-tracking/evidence/2026-11-18/issue-154-live/01-resident-signed-out.png), [02-resident-signed-in.png](../../../.copilot-tracking/evidence/2026-11-18/issue-154-live/02-resident-signed-in.png)). First load after scale-to-zero needed a wait of up to a few minutes.
* After sign-in the page said that the records are read-only, that "Synthetic callback booking is not connected in this showcase environment. Nobody will call you", and, for the paused-contact case, "We will not contact you until the pause is lifted. You can ask for help below."
* The "Help and other ways to reach us" panel gave non-digital routes only: speak to your housing officer, write to or visit the local office, or ask someone you trust to contact us for you. It also said the preview shows no phone numbers or addresses and promises no response times.
* The "Not available in this showcase" panel listed Messages, Uploads, Downloads, Operational appointments ("You cannot change live works appointments here"), Consent and decisions ("You cannot give or change consent here") and Synthetic callbacks as unavailable.
* DOM scan of the signed-in page: zero `mailto:`, `tel:` and `sms:` links; the only form is the sign-in form (action `/demo/login`); the visible controls are the summary and panel buttons and one opt-in checkbox for the optional case-record AI summary, with no free-text or send control.
* Funding text says residents are not asked to pay or approve funding on the page, and the document list shows generated placeholders marked as not presented documents.
* POST probes to six plausible messaging, appointment, callback and consent paths returned 404. A nonexistent control path also returned 404, so these probes show only that no such route answers and are not counted as proof of absence.

### Employee workbench (`ca-cutover-test-demo-api`)

* Entra sign-in as the test employee succeeded; `/api/me` reported role `Retrofit Programme Manager`, identity source `entra`. `/api/cases` listed 16 cases and each case detail returned 200.
* The workbench landing page text mentions residents but contains no representative, interpreter or non-digital string ([03-workbench-signed-in.png](../../../.copilot-tracking/evidence/2026-11-18/issue-154-live/03-workbench-signed-in.png)).
* None of the 16 listed cases has a representative set (`resident.representative` empty) or any entry in `nomination_permissions.representative_authorities`. `GET /api/cases/{id}/representative-view` returned 404 "Case not found." for the three cases tried, which matches the service code path for a case without a representative reference.

### Local supporting evidence

* From `src/api`: `PYTHONPATH=src:tests:../core/src:../agents/src:../core/tests:../agents/tests python3 -m unittest tests.test_representative_expiry_api tests.test_resident_demo_api -q`: 53 tests, OK (one logged "request failed: RuntimeError" line from a negative test).
* `src/core/tests/test_funding_automation_boundary.py` lists `smtplib`, `http.client`, `requests`, `httpx`, `socket` and `aiohttp` as modules the funding boundary must not import. A search of `src/` and `infra/` for `smtplib`, SendGrid, Twilio, Azure Communication Services and GOV.UK Notify found only that test file, so no outbound messaging client is present in the demonstrator code.
* The usability programme gate recorded in [issue-155-live-usability-programme-evidence-2026-11-18.md](issue-155-live-usability-programme-evidence-2026-11-18.md): `validate_audit_use_agreement()` refuses while the staff audit-use statement is unagreed, so no usability measures can be recorded.

## Per-criterion status

| Criterion | State | Basis |
|-----------|-------|-------|
| 1. Resident journey designs cover choice per measure, pause or withdrawal, appointment options, update commitments, handover and complaint or remedy status | Ticked in the issue; not re-proven live | The live showcase is a read-only subset. It shows the paused-contact stage and states that consent, appointments and messaging are unavailable; it does not demonstrate choice per measure, withdrawal, handover or complaint status. The page text contains no "complaint" string |
| 2. Each has an accessible non-digital alternative and supports language, literacy and adjustment needs without inferring incapacity | Ticked; partly observed live | Non-digital routes (housing officer, write or visit, trusted person) are on the live page. Language and adjustment support is not exposed in the showcase |
| 3. Representative views show only task-limited authority and expire as recorded | Ticked; not provable live | No live case has a representative, so the view returns 404. Expiry behaviour is covered by the local `test_representative_expiry_api` run (53 tests with the resident demo suite, OK) |
| 4. Offers are visibly distinct from confirmed commitments | Ticked; not re-proven live | The showcase makes no offers and no commitments ("promises no response times"), so the distinction cannot be seen on it |
| 5a. No live resident contact | Proven for the demo, observed 2026-11-18 | Banner and read-only statements, zero contact links, no send controls, messaging, uploads, appointments, consent and callbacks disabled, no outbound client library in `src/` or `infra/`. Limit: this covers the deployed showcase and the code search, not an exhaustive network trace or the employee workbench |
| 5b. Designs validated through the usability programme before any use | Not proven; cannot be for the demo | Needs moderated sessions with participants and staff agreement (SA-010), which the demo does not have and the owner has not asked for. The code gate refuses to record measures until staff agree. The criterion stays unticked |

## Residual items

* Seeding a synthetic representative and a representative-bearing case in the live store would allow a live check of criterion 3. That would change demo data, which this run did not do.
* The workbench has no representative or interpreter string on its landing page; whether a case-level screen exposes the representative view in the UI was not checked beyond the API.
