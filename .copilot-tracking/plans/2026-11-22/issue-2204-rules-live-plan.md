# Plan: issue 2204 rule actions live (2026-11-22)

* [x] Phase 1: find 503 cause, enable mssql law store on demo API with az (done in research)
* [x] Phase 2: confirm `/api/law/cards` no longer 503 for PM with and without capability
* [x] Phase 3 (single account): create throwaway Entra user B; assign B ProgrammeManager+RuleAuthor; test account A one at a time: PM+RuleOwner
* [x] Phase 4 (partly): B proposes card naming A as approver (RuleAuthor action, 201); A approves, activates, holds, releases, retires (RuleOwner actions); wrong-role denials (B without RuleAuthor, A without RuleOwner); capability-less PM refused
* [ ] Phase 5: cleanup (delete B, restore A to ProgrammeManager only, confirm), evidence note, index, log, changes record, review, commit
