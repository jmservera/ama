# Details: #215 unblock and visit grounding (Refs #215)

## Phase 1 test design

* API class (real handler via `roles.Matrix`, stand-in model), 3 questions on ZF-4:
  * unparseable draft gives `decision-rules-fallback`, model `workflow-only`, server label, cited `ZF-4/` ids, "No record was changed", "A person decides next steps", no approval, clearance or booking claims;
  * valid cited draft gives `generative-grounded` and "AI suggestion, not approved";
  * a draft claiming "cleared ... booked" is withheld and replaced by cited rules;
  * case record JSON is unchanged across all turns;
  * `unstored-ask` gives `decision-rules`, zero model calls and the human-boundary sentence.
* Deterministic class: synthetic safety-stopped detail; every turn cites reasons and the Safety lead owner; unblock and visit turns state the human route and "cannot book a visit or approve a safety step"; the review turn offers no action.
* Static UI class: `chat.js` attribution labels distinguish decision model and generative model; both "Chat cannot approve" notices present; server origin names match the UI.

## Out of scope

Resident-consent copy in `_unblock` (follow-up). Full gate, Docker, cloud calls.
