# Details: issue 130 identity 403 (2026-11-18)

## Phase 1
File `src/core/src/zava_forward/core/resident_decisions.py`: add `_same_signed_in_person(actor, roster_person)` (uses `_identity_value`, keys email, code, oid) and call it in `_operation` in place of `actor != _person(...)`. The PermissionError message is unchanged.

## Phase 2
File `src/core/tests/test_resident_decisions.py`, class `JsonResidentDecisions` (inherited by the SQLite class): helper `roster_bound_principal`, tests `test_intake_entra_principal_matching_roster_identity_is_accepted`, `test_intake_entra_principal_with_other_identity_is_refused_without_mutation`, `test_intake_identity_differing_from_roster_person_is_refused`.

## Phase 3
Commands in the changes record.
